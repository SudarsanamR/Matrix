import numpy as np

def get_matrices():
    matrices = []
    num = int(input("Enter the number of matrices (1-3): "))
    if num < 1 or num > 3:
        print("Invalid number of matrices. Exiting.")
        return None
    
    for i in range(num):
        rows = int(input(f"Enter number of rows for matrix {i+1}: "))
        cols = int(input(f"Enter number of columns for matrix {i+1}: "))
        print(f"Enter elements for matrix {i+1} row-wise:")
        matrix = []
        for _ in range(rows):
            matrix.append(list(map(float, input().split())))
        matrices.append(np.array(matrix))
    
    return matrices

def find_determinant(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        print("Determinant is only defined for square matrices.")
        return None
    return np.linalg.det(matrix)

def multiply_matrices(matrices):
    if len(matrices) < 2:
        print("Need at least two matrices for multiplication.")
        return None
    
    result = matrices[0]
    for i in range(1, len(matrices)):
        if result.shape[1] != matrices[i].shape[0]:
            print("Matrix multiplication not possible due to dimension mismatch.")
            return None
        result = np.dot(result, matrices[i])
    
    return result

if __name__ == "__main__":
    matrices = get_matrices()
    if matrices:
        for i, matrix in enumerate(matrices):
            print(f"Matrix {i+1}:\n", matrix)
            det = find_determinant(matrix)
            if det is not None:
                print(f"Determinant of Matrix {i+1}: {det}\n")
        
        result = multiply_matrices(matrices)
        if result is not None:
            print("Product of Matrices:\n", result)
