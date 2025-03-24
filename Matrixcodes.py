def add_matrices(M1, M2):
    if len(M1) != len(M2) or len(M1[0]) != len(M2[0]):
        raise ValueError("Matrices must have the same dimensions")
    return [[M1[i][j] + M2[i][j] for j in range(len(M1[0]))] for i in range(len(M1))]

def subtract_matrices(M1, M2):
    if len(M1) != len(M2) or len(M1[0]) != len(M2[0]):
        raise ValueError("Matrices must have the same dimensions")
    return [[M1[i][j] - M2[i][j] for j in range(len(M1[0]))] for i in range(len(M1))]

def multiply_matrices(M1, M2):
    if len(M1[0]) != len(M2):
        raise ValueError("Number of columns of M1 must equal number of rows of M2")
    return [[sum(M1[i][k] * M2[k][j] for k in range(len(M2))) for j in range(len(M2[0]))] for i in range(len(M1))]

def transpose_matrix(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def determinant(M):
    if len(M) != len(M[0]):
        raise ValueError("Matrix must be square")
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    det = 0
    for j in range(n):
        cofactor = (-1) ** j * determinant([row[:j] + row[j+1:] for row in (M[1:])])
        det += M[0][j] * cofactor
    return det

def trace_matrix(M):
    if len(M) != len(M[0]):
        raise ValueError("Matrix must be square")
    return sum(M[i][i] for i in range(len(M)))

def inverse_matrix(M):
    if len(M) != len(M[0]):
        raise ValueError("Matrix must be square")
    if len(M) == 2:
        det = determinant(M)
        if det == 0:
            raise ValueError("Matrix is not invertible")
        return [[M[1][1] / det, -M[0][1] / det], [-M[1][0] / det, M[0][0] / det]]
    else:
        raise NotImplementedError("Inverse only implemented for 2x2 matrices")

def set_matrix(name):
    try:
        rows = int(input(f"Enter number of rows for Matrix {name}: "))
        cols = int(input(f"Enter number of columns for Matrix {name}: "))
        print(f"Enter the values for Matrix {name}, row by row (space-separated numbers):")
        matrix = []
        for i in range(rows):
            while True:
                row = list(map(float, input(f"Enter row {i+1}: ").split()))
                if len(row) == cols:
                    matrix.append(row)
                    break
                else:
                    print(f"Please enter exactly {cols} numbers.")
        matrices[name] = matrix
    except ValueError:
        print("Invalid input. Please enter numbers.")

def edit_matrix(name):
    matrix = matrices[name]
    rows = len(matrix)
    cols = len(matrix[0])
    print(f"Editing Matrix {name} ({rows}x{cols}):")
    for i in range(rows):
        while True:
            row = list(map(float, input(f"Enter new row {i+1}: ").split()))
            if len(row) == cols:
                matrix[i] = row
                break
            else:
                print(f"Please enter exactly {cols} numbers.")

def select_matrix():
    while True:
        print("Select matrix:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Answer")
        print("5. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3', '4']:
            matrix_name = ['A', 'B', 'C', 'Answer'][int(choice)-1]
            if matrices[matrix_name] is None:
                print(f"Matrix {matrix_name} is not defined.")
            else:
                return matrices[matrix_name]
        elif choice == '5':
            return None
        else:
            print("Invalid choice")

def dimensions_menu():
    while True:
        print("\nDimensions Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice)-1]
            set_matrix(matrix_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

def edit_menu():
    while True:
        print("\nEdit Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice)-1]
            if matrices[matrix_name] is None:
                print(f"Matrix {matrix_name} is not defined. Please set dimensions first.")
            else:
                edit_matrix(matrix_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

def matrices_menu():
    while True:
        print("\nMatrices Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Inverse")
        print("5. Transpose")
        print("6. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            operation = ['add', 'subtract', 'multiply'][int(choice)-1]
            print("Select first matrix:")
            M1 = select_matrix()
            if M1 is None:
                continue
            print("Select second matrix:")
            M2 = select_matrix()
            if M2 is None:
                continue
            try:
                if operation == 'add':
                    result = add_matrices(M1, M2)
                elif operation == 'subtract':
                    result = subtract_matrices(M1, M2)
                elif operation == 'multiply':
                    result = multiply_matrices(M1, M2)
                matrices['Answer'] = result
                print("Operation successful. Result stored in Answer matrix.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            print("Select matrix for inverse:")
            M = select_matrix()
            if M is None:
                continue
            try:
                result = inverse_matrix(M)
                matrices['Answer'] = result
                print("Operation successful. Result stored in Answer matrix.")
            except (ValueError, NotImplementedError) as e:
                print(f"Error: {e}")
        elif choice == '5':
            print("Select matrix for transpose:")
            M = select_matrix()
            if M is None:
                continue
            result = transpose_matrix(M)
            matrices['Answer'] = result
            print("Operation successful. Result stored in Answer matrix.")
        elif choice == '6':
            break
        else:
            print("Invalid choice")

def determinant_menu():
    while True:
        print("\nDeterminant Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice)-1]
            if matrices[matrix_name] is None:
                print(f"Matrix {matrix_name} is not defined.")
            else:
                try:
                    det = determinant(matrices[matrix_name])
                    print(f"Determinant of Matrix {matrix_name}: {det}")
                except ValueError as e:
                    print(f"Error: {e}")
        elif choice == '4':
            break
        else:
            print("Invalid choice")

def trace_menu():
    while True:
        print("\nTrace Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice)-1]
            if matrices[matrix_name] is None:
                print(f"Matrix {matrix_name} is not defined.")
            else:
                try:
                    tr = trace_matrix(matrices[matrix_name])
                    print(f"Trace of Matrix {matrix_name}: {tr}")
                except ValueError as e:
                    print(f"Error: {e}")
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Main program
matrices = {'A': None, 'B': None, 'C': None, 'Answer': None}

while True:
    print("\nMain Menu:")
    print("1. Dimensions")
    print("2. Edit")
    print("3. Matrices")
    print("4. Determinant")
    print("5. Trace")
    print("6. Exit")
    choice = input("Select an option: ")
    if choice == '1':
        dimensions_menu()
    elif choice == '2':
        edit_menu()
    elif choice == '3':
        matrices_menu()
    elif choice == '4':
        determinant_menu()
    elif choice == '5':
        trace_menu()
    elif choice == '6':
        break
    else:
        print("Invalid choice")