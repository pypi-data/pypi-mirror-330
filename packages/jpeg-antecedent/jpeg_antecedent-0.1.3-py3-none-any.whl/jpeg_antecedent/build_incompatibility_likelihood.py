import multiprocessing
import concurrent.futures
import h5py
import numpy as np
from jpeg_antecedent.block import Block
from jpeg_antecedent.pipeline import IslowPipeline, NaivePipeline
from jpeg_antecedent.jpeg_toolbox import define_quant_table, quality_scaling_law

output_file = r"likelihood.hdf5"
modifications = [0, 63]
purge = True  # if True remove existing data
max_iter = 5000
pipeline_1 = IslowPipeline(define_quant_table(quality_scaling_law(90))) # TODO
pipeline_2 = IslowPipeline(define_quant_table(quality_scaling_law(90))) # TODO
pts_per_modification = 100
max_workers = 12
changes_in_dct = False

def divide_almost_equal(n, m):
    quotient = n // m  # Get the integer division quotient
    remainder = n % m  # Get the remainder
    result = [quotient] * m  # Create a list of m elements, each having quotient as initial value

    # Distribute the remainder among the parts
    for i in range(remainder):
        result[i] += 1

    return result


def handle(n, modification, changes_in_dct, max_iter, pipeline_1, pipeline_2):
    rng = np.random.RandomState()
    if pipeline_2 is not None:
        double_compressed = True
    else:
        double_compressed = False
    results = []
    for i in range(n):
        block = rng.randint(1, 255, size=(8, 8))  # random pixel block
        idx_changes = rng.choice(64, size=modification, replace=False)
        random_changes = np.zeros(64, dtype=np.int32)
        random_changes[idx_changes] = rng.choice([-1, 1], size=modification)
        random_changes = random_changes.reshape((8, 8))

        observed_block = pipeline_1.round_dct(pipeline_1.forward_dct(block)).reshape(8, 8)  # random DCT block
        if changes_in_dct and not double_compressed:  # RJCA
            observed_block += random_changes
            observed_block = Block(observed_block)
        else:  # JCA
            observed_block = pipeline_1.round_pixel(pipeline_1.inverse_dct(observed_block)).reshape(8, 8)
            observed_block += random_changes
            observed_block = Block(observed_block)

        if double_compressed:  # Double compressed
            observed_block = Block(pipeline_2.round_dct(pipeline_2.forward_dct(observed_block.value)).reshape(8, 8))
            antecedent, iteration = observed_block.search_double_antecedent(pipeline_1, pipeline_2, max_iter)
        else:
            antecedent, iteration = observed_block.search_antecedent(pipeline_1, max_iter)

        if antecedent is None:
            results.append(-1)
        else:
            results.append(iteration)

    return modification, results


def main(output_file, modifications, purge, max_iter, pipeline_1, pipeline_2, pts_per_modification, max_workers):
    group_name = str(hash((pipeline_1, pipeline_2, changes_in_dct)))
    with h5py.File(output_file, 'a') as f:
        if group_name in f:
            group = f[group_name]
            modification_present = [m for m in modifications if str(m) in group]
            if modification_present and not purge:
                raise ValueError(f"Some results for the same pipeline and the number of modification \
                {modification_present} are already present in this file. If you want to erase them, set the purge flag \
                to True. Otherwise remove those values from the modifications list.")
            elif modification_present and purge:
                for m in modification_present:
                    del group[str(m)]
        else:
            group = f.create_group(group_name)
        for m in modifications:
            group.create_dataset(str(m), maxshape=(None,), shape=(1,))

    if max_workers is None:
        max_workers = multiprocessing.cpu_count()

    futures = []
    split_points = divide_almost_equal(pts_per_modification, max_workers)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for modification in modifications:
            for points in split_points:

                futures.append(executor.submit(handle,
                                               points,
                                               modification,
                                               changes_in_dct,
                                               max_iter,
                                               pipeline_1,
                                               pipeline_2))

        # Store everything into a hdf5 file:
        # File
        # ├─ pipelines (group): hash(pipeline_1, pipeline_2)
        # │   ├─ modification (dataset): 3
        # │   │   ├─ max_iter (attrs): 10000
        # │   │   ├─ (data): [15, 765, -1, ...]  -1 means no antecedent found after max_iter

        for future in concurrent.futures.as_completed(futures):
            modification, values = future.result()
            print(modification, values)
            print(np.mean(np.array(values) == -1))
            with h5py.File(output_file, 'a') as f:
                group = f[group_name]
                dataset = group[str(modification)]
                current_size = dataset.shape[0]
                dataset.resize(current_size + len(values), axis=0)
                dataset[-len(values):] = values
                dataset.attrs['max_iter'] = max_iter


if __name__ == '__main__':
    main(output_file, modifications, purge, max_iter, pipeline_1, pipeline_2, pts_per_modification, max_workers)
