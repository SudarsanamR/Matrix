# Dictionary to store matrices
matrices = {'A': None, 'B': None, 'C': None, 'Answer': None}

# Function to calculate determinant
def determinant(M):
    if len(M) != len(M[0]):
        raise ValueError("Matrix must be square")
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    det = 0
    # Use cofactor expansion along the first row
    for j in range(n):
        cofactor = (-1) ** j * determinant([row[:j] + row[j+1:] for row in M[1:]])
        det += M[0][j] * cofactor
    return det

# Function to set matrix dimensions and elements
def set_matrix(name):
    try:
        rows = int(input(f"Enter number of rows for Matrix {name}: "))
        cols = int(input(f"Enter number of columns for Matrix {name}: "))
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                while True:
                    try:
                        value = float(input(f"Enter element a{i+1}{j+1}: "))
                        row.append(value)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            matrix.append(row)
        matrices[name] = matrix
    except ValueError:
        print("Invalid input. Please enter integers for dimensions.")

# Function to display a matrix
def display_matrix(M):
    for row in M:
        print(" ".join(map(str, row)))

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
            matrix_name = ['A', 'B', 'C'][int(choice)-1]
            set_matrix(matrix_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Main menu
while True:
    print("\nMain Menu:")
    print("1. Dimensions")
    print("2. Determinant")
    print("3. Exit")
    choice = input("Select an option: ")
    if choice == '1':
        dimensions_menu()
    elif choice == '2':
        determinant_menu()
    elif choice == '3':
        break
    else:
        print("Invalid choice")