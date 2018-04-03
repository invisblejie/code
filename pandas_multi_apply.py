import multiprocessing
import pandas as pd
import numpy as np

def square(x, number):
    return x ** 2 + number

def test_func(data, number):
    data["square"] = data["col"].apply(square, args=(number,))
    return data

if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    df = pd.DataFrame({'col': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]})
    df_split = np.array_split(df, num_cores)
    with multiprocessing.Pool(processes=num_cores) as pool:
        pool_results = pool.starmap(test_func, zip(df_split, [5]*num_cores))
    result = pd.concat(pool_results)
    print(result)
