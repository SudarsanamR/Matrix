import copy
import math
import numpy as np
import sympy as sp

# -----------------------------
# Matrix Class
# -----------------------------
class Matrix:
    def __init__(self, data):
        """
        data is expected to be a 2D list.
        Each entry is converted to a sympy expression so that the matrix
        can include complex numbers and symbolic functions.
        """
        if not data or not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Data must be a non-empty 2D list with equal row lengths.")
        # Convert every element using sp.sympify to allow symbolic expressions.
        self.data = [[sp.sympify(elem) for elem in row] for row in data]
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __str__(self):
        # Pretty-print the matrix row by row.
        s = ""
        for i in range(self.rows):
            row_str = "\t".join(f"a{i+1}{j+1} = {sp.pretty(self.data[i][j])}" for j in range(self.cols))
            s += row_str + "\n"
        return s

    def is_square(self):
        return self.rows == self.cols

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Addition requires matrices of the same dimensions.")
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Subtraction requires matrices of the same dimensions.")
        result = [[self.data[i][j] - other.data[i][j] for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("For multiplication, the number of columns in the first matrix must equal the number of rows in the second.")
        result = []
        for i in range(self.rows):
            new_row = []
            for j in range(other.cols):
                s = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                new_row.append(s)
            result.append(new_row)
        return Matrix(result)

    def transpose(self):
        result = [[self.data[j][i] for j in range(self.rows)]
                  for i in range(self.cols)]
        return Matrix(result)

    def trace(self):
        if not self.is_square():
            raise ValueError("Trace is defined only for square matrices.")
        return sum(self.data[i][i] for i in range(self.rows))

    def determinant(self):
        if not self.is_square():
            raise ValueError("Determinant is defined only for square matrices.")
        # Use sympy's built-in determinant computation.
        return sp.Matrix(self.data).det()

    def inverse(self):
        if not self.is_square():
            raise ValueError("Inverse is defined only for square matrices.")
        # Use sympy's matrix inversion.
        try:
            inv = sp.Matrix(self.data).inv()
        except sp.NonInvertibleMatrixError:
            raise ValueError("Matrix is not invertible.")
        return Matrix(inv.tolist())

    def eigenvalues(self, numeric=False):
        """
        Returns the eigenvalues.
        If numeric is True, returns numerical approximations.
        Otherwise, returns symbolic eigenvalues.
        """
        # Use eigenvals() and extract the keys.
        sym_eigs = list(sp.Matrix(self.data).eigenvals().keys())
        if numeric:
            return [sp.N(e) for e in sym_eigs]
        else:
            return sym_eigs


    def characteristic_equation(self):
        """
        Returns the characteristic polynomial (as a sympy expression) defined by:
            det(X*I - A) = 0.
        Uses the symbol X.
        """
        if not self.is_square():
            raise ValueError("Characteristic equation is defined only for square matrices.")
        X = sp.symbols('X')
        A_sym = sp.Matrix(self.data)
        char_poly = sp.expand((X * sp.eye(self.rows) - A_sym).det())
        return char_poly

    def power(self, exponent):
        """
        Raises the matrix to any real number exponent.
        For negative exponents, the matrix must be invertible.
        First, it attempts to diagonalize the matrix. If diagonalization fails,
        it uses the matrix logarithm and exponential.
        """
        if not self.is_square():
            raise ValueError("Power is defined only for square matrices.")
        M = sp.Matrix(self.data)
        # Try diagonalization first.
        try:
            P, D = M.diagonalize()
            # Raise each diagonal entry to the exponent.
            diag_entries = [d**exponent for d in D.diagonal()]
            D_power = sp.diag(*diag_entries)
            M_power = P * D_power * P.inv()
            return Matrix(M_power.tolist())
        except sp.MatrixError:
            # If not diagonalizable, try using logarithm and exponential.
            try:
                M_log = sp.logm(M)
                M_power = sp.exp(M_log * exponent)
                return Matrix(M_power.tolist())
            except Exception as e:
                raise ValueError("Matrix power for real exponent is not defined for this matrix.")

# -----------------------------
# Matrix Manager Class
# -----------------------------
class MatrixManager:
    def __init__(self):
        self.matrices = {}  # maps a name (like "A", "B", etc.) to a Matrix instance
        self.counter = 0   # for assigning names

    def _get_new_name(self):
        # Use uppercase letters; if more than 26, append a number.
        if self.counter < 26:
            name = chr(65 + self.counter)
        else:
            name = chr(65 + (self.counter % 26)) + str(self.counter // 26)
        self.counter += 1
        return name

    def create_matrix(self):
        name = self._get_new_name()
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
                    # Accept expressions (e.g., 2+3j, sin(pi/4), log(2)) as input.
                    while True:
                        expr = input(f"Enter element a{i+1}{j+1}: ")
                        try:
                            row.append(sp.sympify(expr))
                            break
                        except (sp.SympifyError, ValueError):
                            print("Invalid input. Please enter a valid number or expression.")
                data.append(row)
            self.matrices[name] = Matrix(data)
            print(f"Matrix {name} has been created.")
        except ValueError:
            print("Invalid input for dimensions.")

    def delete_matrix(self):
        chosen = self.select_matrix()
        if chosen is None:
            return
        name, _ = chosen
        del self.matrices[name]
        print(f"Matrix {name} has been deleted.")

    def edit_matrix(self):
        chosen = self.select_matrix()
        if chosen is None:
            return
        name, _ = chosen
        try:
            rows = int(input(f"Enter new number of rows for Matrix {name}: "))
            cols = int(input(f"Enter new number of columns for Matrix {name}: "))
            if rows <= 0 or cols <= 0:
                print("Dimensions must be positive integers.")
                return
            new_data = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    while True:
                        expr = input(f"Enter new element a{i+1}{j+1}: ")
                        try:
                            row.append(sp.sympify(expr))
                            break
                        except (sp.SympifyError, ValueError):
                            print("Invalid input. Please enter a valid number or expression.")
                new_data.append(row)
            self.matrices[name] = Matrix(new_data)
            print(f"Matrix {name} has been updated.")
        except ValueError:
            print("Invalid input for dimensions.")

    def list_matrices(self):
        if not self.matrices:
            print("No matrices defined yet.")
            return []
        sorted_names = sorted(self.matrices.keys())
        print("Stored Matrices:")
        numbered = []
        for idx, name in enumerate(sorted_names, start=1):
            mat = self.matrices[name]
            print(f"{idx}. Matrix {name} ({mat.rows}x{mat.cols})")
            numbered.append((name, mat))
        print("0. Back")
        return numbered

    def show_matrix(self):
        numbered = self.list_matrices()
        if not numbered:
            return
        try:
            choice = int(input("Select a matrix number to show (or 0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(numbered):
                name, mat = numbered[choice - 1]
                print(f"Matrix {name}:")
                print(mat)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    def select_matrix(self):
        numbered = self.list_matrices()
        if not numbered:
            return None
        try:
            choice = int(input("Select a matrix by number (or 0 to cancel): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(numbered):
                return numbered[choice - 1]
            else:
                print("Invalid selection.")
                return None
        except ValueError:
            print("Please enter a valid number.")
            return None

    def store_result(self, result_matrix):
        try:
            choice = int(input("Store result as a new matrix? (Enter 1 for yes, 0 for no): "))
            if choice == 1:
                name = self._get_new_name()
                self.matrices[name] = result_matrix
                print(f"Result stored as Matrix {name}.")
        except ValueError:
            print("Invalid input. Not storing result.")

# -----------------------------
# Menus
# -----------------------------
def management_menu(manager):
    while True:
        print("\nMatrix Management Menu:")
        print("1. New Matrix")
        print("2. Delete Matrix")
        print("3. Edit Matrix")
        print("4. List/Show Matrices")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == '1':
            manager.create_matrix()
        elif choice == '2':
            manager.delete_matrix()
        elif choice == '3':
            manager.edit_matrix()
        elif choice == '4':
            manager.show_matrix()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

def operations_menu(manager):
    while True:
        print("\nMatrix Operations Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Power")
        print("5. Transpose")
        print("6. Inverse")
        print("7. Determinant")
        print("8. Trace")
        print("9. Eigenvalues")
        print("10. Characteristic Equation")
        print("11. Back to Main Menu")
        choice = input("Select an option: ").strip()
        try:
            if choice in ['1', '2', '3']:
                print("Select first matrix:")
                first = manager.select_matrix()
                if first is None: continue
                _, mat1 = first
                print("Select second matrix:")
                second = manager.select_matrix()
                if second is None: continue
                _, mat2 = second
                if choice == '1':
                    result = mat1.add(mat2)
                elif choice == '2':
                    result = mat1.subtract(mat2)
                else:
                    result = mat1.multiply(mat2)
                print("Operation successful. Result:")
                print(result)
                manager.store_result(result)
            elif choice == '4':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                try:
                    exp = float(input("Enter the real exponent: "))
                    result = mat.power(exp)
                    print(f"Matrix raised to the power {exp}:")
                    print(result)
                    manager.store_result(result)
                except ValueError:
                    print("Invalid input for exponent.")
            elif choice == '5':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                result = mat.transpose()
                print("Transpose successful. Result:")
                print(result)
                manager.store_result(result)
            elif choice == '6':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                result = mat.inverse()
                print("Inverse successful. Result:")
                print(result)
                manager.store_result(result)
            elif choice == '7':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                det = mat.determinant()
                print(f"Determinant: {det}")
            elif choice == '8':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                tr = mat.trace()
                print(f"Trace: {tr}")
            elif choice == '9':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                numeric = input("Evaluate eigenvalues numerically? (Enter 1 for yes, 0 for no): ").strip() == '1'
                eigvals = mat.eigenvalues(numeric=numeric)
                print("Eigenvalues:")
                for idx, val in enumerate(eigvals, start=1):
                    print(f"λ{idx} = {val}")
            elif choice == '10':
                chosen = manager.select_matrix()
                if chosen is None: continue
                _, mat = chosen
                char_eq = mat.characteristic_equation()
                print("Characteristic Equation:")
                print(f"{char_eq} = 0")
            elif choice == '11':
                break
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")

def main_menu():
    manager = MatrixManager()
    while True:
        print("\nMain Menu:")
        print("1. Matrix Management")
        print("2. Matrix Operations")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            management_menu(manager)
        elif choice == '2':
            operations_menu(manager)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main_menu()
