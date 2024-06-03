import numpy as np
import time

def main():
    print("Start Program B")
    start_time = time.time()

    matrix_size = 3000
    A = np.random.rand(matrix_size, matrix_size)
    B = np.random.rand(matrix_size, matrix_size)

    for _ in range(10):
        np.dot(A, B)
    end_time = time.time()
    print("End Program B")
    print(f"Execution time - program_b : {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
