# Global dictionary to store matrices; keys will be names (e.g. "A", "B", "C", etc.)
matrices = {}
# Counter to assign new names (0 -> "A", 1 -> "B", etc.)
matrix_counter = 0

def get_new_matrix_name():
    global matrix_counter
    # Use uppercase letters starting from A. For more than 26 matrices, append a number.
    name = chr(65 + matrix_counter) if matrix_counter < 26 else chr(65 + (matrix_counter % 26)) + str(matrix_counter // 26)
    matrix_counter += 1
    return name

# --- Basic Matrix Operations ---

def add_matrices(mat1, mat2):
    if mat1['rows'] != mat2['rows'] or mat1['cols'] != mat2['cols']:
        raise ValueError("Matrices must have the same dimensions")
    result_data = [[mat1['data'][i][j] + mat2['data'][i][j] for j in range(mat1['cols'])] for i in range(mat1['rows'])]
    return {'rows': mat1['rows'], 'cols': mat1['cols'], 'data': result_data}

def subtract_matrices(mat1, mat2):
    if mat1['rows'] != mat2['rows'] or mat1['cols'] != mat2['cols']:
        raise ValueError("Matrices must have the same dimensions")
    result_data = [[mat1['data'][i][j] - mat2['data'][i][j] for j in range(mat1['cols'])] for i in range(mat1['rows'])]
    return {'rows': mat1['rows'], 'cols': mat1['cols'], 'data': result_data}

def multiply_matrices(mat1, mat2):
    if mat1['cols'] != mat2['rows']:
        raise ValueError("Number of columns of first matrix must equal number of rows of second matrix")
    result_data = [[sum(mat1['data'][i][k] * mat2['data'][k][j] for k in range(mat1['cols']))
                    for j in range(mat2['cols'])] for i in range(mat1['rows'])]
    return {'rows': mat1['rows'], 'cols': mat2['cols'], 'data': result_data}

def transpose_matrix(mat):
    result_data = [[mat['data'][j][i] for j in range(mat['rows'])] for i in range(mat['cols'])]
    return {'rows': mat['cols'], 'cols': mat['rows'], 'data': result_data}

# --- Determinant, Submatrix, Inverse, and Trace ---

def submatrix(mat, row, col):
    new_data = [row_data[:col] + row_data[col+1:] for i, row_data in enumerate(mat['data']) if i != row]
    return {'rows': mat['rows'] - 1, 'cols': mat['cols'] - 1, 'data': new_data}

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

def inverse_matrix(mat):
    if mat['rows'] != mat['cols']:
        raise ValueError("Matrix must be square")
    n = mat['rows']
    det = determinant(mat)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    # Build cofactor matrix
    cofactor = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sign = (-1) ** (i + j)
            sub_mat = submatrix(mat, i, j)
            cofactor[i][j] = sign * determinant(sub_mat)
    # Adjugate (transpose of cofactor matrix)
    adjugate = [list(row) for row in zip(*cofactor)]
    # Inverse is adjugate divided by determinant
    inverse_data = [[elem / det for elem in row] for row in adjugate]
    return {'rows': n, 'cols': n, 'data': inverse_data}

def trace_matrix(mat):
    if mat['rows'] != mat['cols']:
        raise ValueError("Trace is only defined for square matrices")
    return sum(mat['data'][i][i] for i in range(mat['rows']))

# --- I/O Functions for Matrices ---

def new_matrix():
    name = get_new_matrix_name()
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
                        elem = float(input(f"Enter element a{i+1}{j+1}: "))
                        row.append(elem)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            data.append(row)
        matrices[name] = {'rows': rows, 'cols': cols, 'data': data}
        print(f"Matrix {name} has been created.")
    except ValueError:
        print("Invalid input for dimensions. Please enter positive integers.")

def delete_matrix():
    if not matrices:
        print("No matrices to delete.")
        return
    list_matrices()
    name = input("Enter the name of the matrix to delete: ").strip().upper()
    if name in matrices:
        del matrices[name]
        print(f"Matrix {name} has been deleted.")
    else:
        print(f"Matrix {name} does not exist.")

def edit_matrix():
    if not matrices:
        print("No matrices to edit.")
        return
    list_matrices()
    name = input("Enter the name of the matrix to edit: ").strip().upper()
    if name not in matrices:
        print(f"Matrix {name} does not exist.")
        return
    mat = matrices[name]
    rows, cols = mat['rows'], mat['cols']
    print(f"Editing Matrix {name} ({rows}x{cols}):")
    new_data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            while True:
                try:
                    elem = float(input(f"Enter new element a{i+1}{j+1}: "))
                    row.append(elem)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
        new_data.append(row)
    matrices[name]['data'] = new_data
    print(f"Matrix {name} has been updated.")

def list_matrices():
    if not matrices:
        print("No matrices defined yet.")
    else:
        print("Current matrices:")
        for name, mat in matrices.items():
            print(f"Matrix {name} ({mat['rows']}x{mat['cols']})")

def print_matrix(mat):
    if mat is None:
        print("Matrix is not defined.")
        return
    for i in range(mat['rows']):
        for j in range(mat['cols']):
            print(f"a{i+1}{j+1} = {mat['data'][i][j]}", end="\t")
        print()
        
def select_matrix(prompt="Select a matrix by name: "):
    list_matrices()
    name = input(prompt).strip().upper()
    if name in matrices:
        return matrices[name]
    else:
        print(f"Matrix {name} does not exist.")
        return None

# --- Unified Matrix Operations Menu ---

def matrix_operations_menu():
    while True:
        print("\nMatrix Operations Menu:")
        print("1. New Matrix")
        print("2. Delete Matrix")
        print("3. Edit Matrix")
        print("4. List Matrices")
        print("5. Addition")
        print("6. Subtraction")
        print("7. Multiplication")
        print("8. Transpose")
        print("9. Inverse")
        print("10. Determinant")
        print("11. Trace")
        print("12. Back to Main Menu")
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            new_matrix()
        elif choice == '2':
            delete_matrix()
        elif choice == '3':
            edit_matrix()
        elif choice == '4':
            list_matrices()
        elif choice in ['5','6','7']:
            print("Select first matrix:")
            mat1 = select_matrix("Enter first matrix name: ")
            if not mat1: continue
            print("Select second matrix:")
            mat2 = select_matrix("Enter second matrix name: ")
            if not mat2: continue
            try:
                if choice == '5':
                    result = add_matrices(mat1, mat2)
                elif choice == '6':
                    result = subtract_matrices(mat1, mat2)
                elif choice == '7':
                    result = multiply_matrices(mat1, mat2)
                print("Operation successful. Result:")
                print_matrix(result)
                # Optionally, store result as a new matrix:
                store = input("Store result as a new matrix? (y/n): ").strip().lower()
                if store == 'y':
                    name = get_new_matrix_name()
                    matrices[name] = result
                    print(f"Result stored as Matrix {name}.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '8':
            mat = select_matrix("Select a matrix for transpose: ")
            if not mat: continue
            result = transpose_matrix(mat)
            print("Transpose successful. Result:")
            print_matrix(result)
            store = input("Store result as a new matrix? (y/n): ").strip().lower()
            if store == 'y':
                name = get_new_matrix_name()
                matrices[name] = result
                print(f"Result stored as Matrix {name}.")
        elif choice == '9':
            mat = select_matrix("Select a matrix for inverse: ")
            if not mat: continue
            try:
                result = inverse_matrix(mat)
                print("Inverse successful. Result:")
                print_matrix(result)
                store = input("Store result as a new matrix? (y/n): ").strip().lower()
                if store == 'y':
                    name = get_new_matrix_name()
                    matrices[name] = result
                    print(f"Result stored as Matrix {name}.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '10':
            mat = select_matrix("Select a matrix to compute determinant: ")
            if not mat: continue
            try:
                det = determinant(mat)
                print(f"Determinant: {det}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '11':
            mat = select_matrix("Select a matrix to compute trace: ")
            if not mat: continue
            try:
                tr = trace_matrix(mat)
                print(f"Trace: {tr}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '12':
            break
        else:
            print("Invalid choice")

# --- Main Program Loop ---

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Matrix Operations")
        print("2. Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            matrix_operations_menu()
        elif choice == '2':
            print("Exiting program.")
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main_menu()
