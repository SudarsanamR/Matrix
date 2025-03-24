# Global dictionary to store matrices
matrices = {'A': None, 'B': None, 'C': None, 'Answer': None}

# Function to add two matrices
def add_matrices(mat1, mat2):
    if mat1['rows'] != mat2['rows'] or mat1['cols'] != mat2['cols']:
        raise ValueError("Matrices must have the same dimensions")
    result_data = [[mat1['data'][i][j] + mat2['data'][i][j] for j in range(mat1['cols'])] for i in range(mat1['rows'])]
    return {'rows': mat1['rows'], 'cols': mat1['cols'], 'data': result_data}

# Function to subtract two matrices
def subtract_matrices(mat1, mat2):
    if mat1['rows'] != mat2['rows'] or mat1['cols'] != mat2['cols']:
        raise ValueError("Matrices must have the same dimensions")
    result_data = [[mat1['data'][i][j] - mat2['data'][i][j] for j in range(mat1['cols'])] for i in range(mat1['rows'])]
    return {'rows': mat1['rows'], 'cols': mat1['cols'], 'data': result_data}

# Function to multiply two matrices
def multiply_matrices(mat1, mat2):
    if mat1['cols'] != mat2['rows']:
        raise ValueError("Number of columns of first matrix must equal number of rows of second matrix")
    result_data = [[sum(mat1['data'][i][k] * mat2['data'][k][j] for k in range(mat1['cols'])) for j in range(mat2['cols'])] for i in range(mat1['rows'])]
    return {'rows': mat1['rows'], 'cols': mat2['cols'], 'data': result_data}

# Function to compute the transpose of a matrix
def transpose_matrix(mat):
    result_data = [[mat['data'][j][i] for j in range(mat['rows'])] for i in range(mat['cols'])]
    return {'rows': mat['cols'], 'cols': mat['rows'], 'data': result_data}

# Function to compute the inverse of a 2x2 or 3x3 matrix
def inverse_matrix(mat):
    if mat['rows'] != mat['cols']:
        raise ValueError("Matrix must be square")
    n = mat['rows']
    
    if n == 2:
        a, b = mat['data'][0]
        c, d = mat['data'][1]
        det = a * d - b * c
        if det == 0:
            raise ValueError("Matrix is not invertible")
        inv_det = 1 / det
        result_data = [[d * inv_det, -b * inv_det], [-c * inv_det, a * inv_det]]
        return {'rows': 2, 'cols': 2, 'data': result_data}
    
    elif n == 3:
        det = determinant(mat)
        if det == 0:
            raise ValueError("Matrix is not invertible")
        
        # Compute cofactor matrix
        cofactor = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                sign = (-1) ** (i + j)
                sub_mat = submatrix(mat, i, j)
                det_sub = determinant(sub_mat)
                cofactor[i][j] = sign * det_sub
        
        # Compute adjugate (transpose of cofactor matrix)
        adj_data = [list(row) for row in zip(*cofactor)]
        
        # Compute inverse by scaling adjugate by 1/det
        inverse_data = [[elem / det for elem in row] for row in adj_data]
        return {'rows': 3, 'cols': 3, 'data': inverse_data}
    
    else:
        raise ValueError("Inverse only implemented for 2x2 and 3x3 matrices")

# Function to get submatrix for determinant and inverse calculations
def submatrix(mat, i, j):
    new_data = [row[:j] + row[j+1:] for row in (mat['data'][:i] + mat['data'][i+1:])]
    return {'rows': mat['rows'] - 1, 'cols': mat['cols'] - 1, 'data': new_data}

# Function to compute the determinant of a square matrix
def determinant(mat):
    if mat['rows'] != mat['cols']:
        raise ValueError("Matrix must be square")
    n = mat['rows']
    if n == 1:
        return mat['data'][0][0]
    elif n == 2:
        a, b = mat['data'][0]
        c, d = mat['data'][1]
        return a * d - b * c
    else:
        det = 0
        for j in range(n):
            sign = (-1) ** j
            sub_mat = submatrix(mat, 0, j)
            det += sign * mat['data'][0][j] * determinant(sub_mat)
        return det

# Function to set matrix dimensions and values
def set_matrix(name):
    try:
        rows = int(input(f"Enter number of rows for Matrix {name}: "))
        cols = int(input(f"Enter number of columns for Matrix {name}: "))
        if rows <= 0 or cols <= 0:
            print("Dimensions must be positive integers.")
            return
        data = []
        for i in range(rows):
            row = []
            for j in range(cols):
                while True:
                    try:
                        elem = float(input(f"Enter a{i+1}{j+1}: "))
                        row.append(elem)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            data.append(row)
        matrices[name] = {'rows': rows, 'cols': cols, 'data': data}
        print(f"Matrix {name} has been set.")
    except ValueError:
        print("Invalid input for dimensions. Please enter positive integers.")

# Function to edit an existing matrix
def edit_matrix(name):
    mat = matrices[name]
    rows = mat['rows']
    cols = mat['cols']
    print(f"Editing Matrix {name} ({rows}x{cols}):")
    data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            while True:
                try:
                    elem = float(input(f"Enter new a{i+1}{j+1}: "))
                    row.append(elem)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
        data.append(row)
    mat['data'] = data
    print(f"Matrix {name} has been updated.")

# Function to print a matrix
def print_matrix(mat):
    if mat is None:
        print("Matrix is not defined.")
        return
    for row in mat['data']:
        print(' '.join(map(str, row)))

# Function to select a matrix from available options
def select_matrix():
    while True:
        print("\nSelect matrix:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Answer")
        print("5. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3', '4']:
            matrix_name = ['A', 'B', 'C', 'Answer'][int(choice) - 1]
            if matrices[matrix_name] is None:
                print(f"Matrix {matrix_name} is not defined.")
            else:
                return matrices[matrix_name]
        elif choice == '5':
            return None
        else:
            print("Invalid choice")

# Dimensions menu
def dimensions_menu():
    while True:
        print("\nDimensions Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice) - 1]
            set_matrix(matrix_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Edit menu
def edit_menu():
    while True:
        print("\nEdit Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice) - 1]
            if matrices[matrix_name] is None:
                print(f"Matrix {matrix_name} is not defined. Please set dimensions first.")
            else:
                edit_matrix(matrix_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Matrices menu for operations
def matrices_menu():
    while True:
        print("\nMatrices Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Transpose")
        print("5. Inverse")
        print("6. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            operation = ['add', 'subtract', 'multiply'][int(choice) - 1]
            print("Select first matrix:")
            mat1 = select_matrix()
            if mat1 is None:
                continue
            print("Select second matrix:")
            mat2 = select_matrix()
            if mat2 is None:
                continue
            try:
                if operation == 'add':
                    result = add_matrices(mat1, mat2)
                elif operation == 'subtract':
                    result = subtract_matrices(mat1, mat2)
                elif operation == 'multiply':
                    result = multiply_matrices(mat1, mat2)
                matrices['Answer'] = result
                print("Operation successful. Result stored in Answer matrix.")
                print("Resultant Matrix:")
                print_matrix(matrices['Answer'])
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            print("Select matrix for transpose:")
            mat = select_matrix()
            if mat is None:
                continue
            result = transpose_matrix(mat)
            matrices['Answer'] = result
            print("Transpose successful. Result stored in Answer matrix.")
            print("Resultant Matrix:")
            print_matrix(matrices['Answer'])
        elif choice == '5':
            print("Select matrix for inverse:")
            mat = select_matrix()
            if mat is None:
                continue
            try:
                result = inverse_matrix(mat)
                matrices['Answer'] = result
                print("Inverse successful. Result stored in Answer matrix.")
                print("Resultant Matrix:")
                print_matrix(matrices['Answer'])
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '6':
            break
        else:
            print("Invalid choice")

# Determinant menu
def determinant_menu():
    while True:
        print("\nDeterminant Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice) - 1]
            mat = matrices[matrix_name]
            if mat is None:
                print(f"Matrix {matrix_name} is not defined.")
            elif mat['rows'] != mat['cols']:
                print("Determinant is only defined for square matrices.")
            else:
                det = determinant(mat)
                print(f"Determinant of Matrix {matrix_name}: {det}")
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Trace menu
def trace_menu():
    while True:
        print("\nTrace Menu:")
        print("1. Matrix A")
        print("2. Matrix B")
        print("3. Matrix C")
        print("4. Back")
        choice = input("Select an option: ")
        if choice in ['1', '2', '3']:
            matrix_name = ['A', 'B', 'C'][int(choice) - 1]
            mat = matrices[matrix_name]
            if mat is None:
                print(f"Matrix {matrix_name} is not defined.")
            elif mat['rows'] != mat['cols']:
                print("Trace is only defined for square matrices.")
            else:
                tr = sum(mat['data'][i][i] for i in range(mat['rows']))
                print(f"Trace of Matrix {matrix_name}: {tr}")
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Main program loop
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
        print("Exiting program.")
        break
    else:
        print("Invalid choice")