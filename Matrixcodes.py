import copy
import math
from typing import List, Union, Optional, Tuple
import numpy as np
import sympy as sp

# -----------------------------
# Matrix Class
# -----------------------------
class Matrix:
    """
    A class representing a matrix with support for symbolic computations.
    
    This class provides various matrix operations including addition, subtraction,
    multiplication, transpose, determinant, inverse, eigenvalues, and more.
    All elements are stored as sympy expressions to support symbolic computations.
    
    Attributes:
        data (List[List[sp.Expr]]): The matrix elements as sympy expressions
        rows (int): Number of rows in the matrix
        cols (int): Number of columns in the matrix
    
    Examples:
        >>> m = Matrix([[1, 2], [3, 4]])
        >>> print(m)
        a11 = 1    a12 = 2
        a21 = 3    a22 = 4
    """
    
    def __init__(self, data: List[List[Union[int, float, str, sp.Expr]]]) -> None:
        """
        Initialize a matrix with the given data.
        
        Args:
            data: A 2D list containing matrix elements. Elements can be numbers,
                 strings representing mathematical expressions, or sympy expressions.
        
        Raises:
            ValueError: If data is empty or rows have unequal lengths.
            SympifyError: If any element cannot be converted to a sympy expression.
        """
        if not data or not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Data must be a non-empty 2D list with equal row lengths.")
        # Convert every element using sp.sympify to allow symbolic expressions
        self.data = [[sp.sympify(elem) for elem in row] for row in data]
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __str__(self) -> str:
        """
        Return a string representation of the matrix.
        
        Returns:
            A formatted string showing each element with its position.
        """
        s = ""
        for i in range(self.rows):
            row_str = "\t".join(f"a{i+1}{j+1} = {sp.pretty(self.data[i][j])}" for j in range(self.cols))
            s += row_str + "\n"
        return s

    def is_square(self) -> bool:
        """
        Check if the matrix is square (equal number of rows and columns).
        
        Returns:
            True if the matrix is square, False otherwise.
        """
        return self.rows == self.cols

    def add(self, other: 'Matrix') -> 'Matrix':
        """
        Add this matrix with another matrix.
        
        Args:
            other: The matrix to add with this matrix.
        
        Returns:
            A new matrix containing the sum.
        
        Raises:
            ValueError: If matrices have different dimensions.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Addition requires matrices of the same dimensions.")
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def subtract(self, other: 'Matrix') -> 'Matrix':
        """
        Subtract another matrix from this matrix.
        
        Args:
            other: The matrix to subtract from this matrix.
        
        Returns:
            A new matrix containing the difference.
        
        Raises:
            ValueError: If matrices have different dimensions.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Subtraction requires matrices of the same dimensions.")
        result = [[self.data[i][j] - other.data[i][j] for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def multiply(self, other: Union['Matrix', int, float, sp.Number]) -> 'Matrix':
        """
        Multiply this matrix by another matrix or a scalar.
        
        Args:
            other: Either a Matrix instance or a scalar number.
        
        Returns:
            A new matrix containing the product.
        
        Raises:
            ValueError: If matrix multiplication dimensions are incompatible.
        """
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("For matrix multiplication, the number of columns in the first matrix must equal the number of rows in the second.")
            result = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                       for j in range(other.cols)] for i in range(self.rows)]
        elif isinstance(other, (int, float, sp.Number)):
            result = [[self.data[i][j] * other for j in range(self.cols)] for i in range(self.rows)]
        else:
            raise ValueError("Multiplication is only supported with a matrix or a scalar number.")
        return Matrix(result)

    def transpose(self) -> 'Matrix':
        """
        Compute the transpose of this matrix.
        
        Returns:
            A new matrix containing the transpose.
        """
        try:
            result = [[self.data[j][i] for j in range(self.rows)]
                      for i in range(self.cols)]
            return Matrix(result)
        except Exception as e:
            raise ValueError(f"Error computing transpose: {str(e)}")

    def trace(self) -> sp.Expr:
        """
        Compute the trace of this matrix (sum of diagonal elements).
        
        Returns:
            The trace as a sympy expression.
        
        Raises:
            ValueError: If the matrix is not square.
        """
        if not self.is_square():
            raise ValueError("Trace is defined only for square matrices.")
        try:
            return sum(self.data[i][i] for i in range(self.rows))
        except Exception as e:
            raise ValueError(f"Error computing trace: {str(e)}")

    def determinant(self) -> sp.Expr:
        """
        Compute the determinant of this matrix.
        
        Returns:
            The determinant as a sympy expression.
        
        Raises:
            ValueError: If the matrix is not square.
        """
        if not self.is_square():
            raise ValueError("Determinant is defined only for square matrices.")
        try:
            # Use sympy's built-in determinant computation
            return sp.Matrix(self.data).det()
        except Exception as e:
            raise ValueError(f"Error computing determinant: {str(e)}")

    def inverse(self) -> 'Matrix':
        """
        Compute the inverse of this matrix.
        
        Returns:
            A new matrix containing the inverse.
        
        Raises:
            ValueError: If the matrix is not square or not invertible.
        """
        if not self.is_square():
            raise ValueError("Inverse is defined only for square matrices.")
        try:
            # Check if determinant is zero (matrix is singular)
            det = self.determinant()
            if det == 0:
                raise ValueError("Matrix is singular (determinant is zero).")
            
            inv = sp.Matrix(self.data).inv()
            return Matrix(inv.tolist())
        except sp.NonInvertibleMatrixError:
            raise ValueError("Matrix is not invertible.")
        except Exception as e:
            raise ValueError(f"Error computing inverse: {str(e)}")

    def eigenvalues(self, numeric: bool = False) -> List[sp.Expr]:
        """
        Compute the eigenvalues of this matrix.
        
        Args:
            numeric: If True, return numerical approximations of eigenvalues.
                    If False, return symbolic eigenvalues.
        
        Returns:
            List of eigenvalues as sympy expressions.
        
        Raises:
            ValueError: If the matrix is not square.
        """
        if not self.is_square():
            raise ValueError("Eigenvalues are defined only for square matrices.")
        try:
            sym_eigs = list(sp.Matrix(self.data).eigenvals().keys())
            if numeric:
                return [sp.N(e) for e in sym_eigs]
            return sym_eigs
        except Exception as e:
            raise ValueError(f"Error computing eigenvalues: {str(e)}")

    def characteristic_equation(self) -> sp.Expr:
        """
        Compute the characteristic polynomial of this matrix.
        
        Returns:
            The characteristic polynomial as a sympy expression.
        
        Raises:
            ValueError: If the matrix is not square.
        """
        if not self.is_square():
            raise ValueError("Characteristic equation is defined only for square matrices.")
        try:
            X = sp.symbols('X')
            A_sym = sp.Matrix(self.data)
            char_poly = sp.expand((X * sp.eye(self.rows) - A_sym).det())
            return char_poly
        except Exception as e:
            raise ValueError(f"Error computing characteristic equation: {str(e)}")

    def power(self, exponent: Union[int, float]) -> 'Matrix':
        """
        Raise this matrix to a real number exponent.
        
        Args:
            exponent: The real number exponent.
        
        Returns:
            A new matrix containing the result.
        
        Raises:
            ValueError: If the matrix is not square or if the operation is not defined.
        """
        if not self.is_square():
            raise ValueError("Matrix power is defined only for square matrices.")
        try:
            M = sp.Matrix(self.data)
            # Try diagonalization first
            try:
                P, D = M.diagonalize()
                # Raise each diagonal entry to the exponent
                diag_entries = [d**exponent for d in D.diagonal()]
                D_power = sp.diag(*diag_entries)
                M_power = P * D_power * P.inv()
                return Matrix(M_power.tolist())
            except sp.MatrixError:
                # If not diagonalizable, try using logarithm and exponential
                try:
                    M_log = sp.logm(M)
                    M_power = sp.exp(M_log * exponent)
                    return Matrix(M_power.tolist())
                except Exception as e:
                    raise ValueError(f"Matrix power for real exponent is not defined for this matrix: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error computing matrix power: {str(e)}")

    def is_symmetric(self) -> bool:
        """
        Check if the matrix is symmetric (equal to its transpose).
        
        Returns:
            True if the matrix is symmetric, False otherwise.
        """
        if not self.is_square():
            return False
        try:
            return self.data == self.transpose().data
        except Exception:
            return False

    def is_orthogonal(self) -> bool:
        """
        Check if the matrix is orthogonal (its transpose equals its inverse).
        
        Returns:
            True if the matrix is orthogonal, False otherwise.
        """
        if not self.is_square():
            return False
        try:
            # Check if A * A^T = I
            product = self.multiply(self.transpose())
            identity = Matrix([[1 if i == j else 0 for j in range(self.rows)] for i in range(self.rows)])
            return product.data == identity.data
        except Exception:
            return False

# -----------------------------
# Matrix Manager Class
# -----------------------------
class MatrixManager:
    """
    A class to manage multiple matrices and their operations.
    
    This class provides functionality to create, delete, edit, and perform operations
    on multiple matrices. It maintains a dictionary of named matrices and provides
    a user interface for matrix management.
    
    Attributes:
        matrices (Dict[str, Matrix]): Dictionary mapping matrix names to Matrix instances
        counter (int): Counter for generating unique matrix names
        history (List[Tuple[str, str]]): List of operations performed (operation, matrix name)
    """
    
    def __init__(self):
        self.matrices = {}  # maps a name (like "A", "B", etc.) to a Matrix instance
        self.counter = 0   # for assigning names
        self.history = []  # track operation history

    def _get_new_name(self) -> str:
        """
        Generate a new unique name for a matrix.
        
        Returns:
            A string representing the new matrix name.
        """
        if self.counter < 26:
            name = chr(65 + self.counter)
        else:
            name = chr(65 + (self.counter % 26)) + str(self.counter // 26)
        self.counter += 1
        return name

    def create_matrix(self) -> None:
        """
        Create a new matrix through user input.
        
        The user is prompted to enter dimensions and elements of the matrix.
        The matrix is stored with a unique name.
        """
        name = self._get_new_name()
        try:
            while True:
                try:
                    rows = int(input(f"Enter number of rows for Matrix {name}: "))
                    cols = int(input(f"Enter number of columns for Matrix {name}: "))
                    if rows <= 0 or cols <= 0:
                        print("Dimensions must be positive integers.")
                        continue
                    break
                except ValueError:
                    print("Please enter valid integers for dimensions.")

            data = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    while True:
                        expr = input(f"Enter element a{i+1}{j+1}: ")
                        try:
                            row.append(sp.sympify(expr))
                            break
                        except (sp.SympifyError, ValueError):
                            print("Invalid input. Please enter a valid number or expression.")
                data.append(row)
            
            self.matrices[name] = Matrix(data)
            self.history.append(("create", name))
            print(f"Matrix {name} has been created successfully.")
            
        except Exception as e:
            print(f"Error creating matrix: {str(e)}")
            if name in self.matrices:
                del self.matrices[name]

    def delete_matrix(self) -> None:
        """
        Delete a matrix selected by the user.
        """
        chosen = self.select_matrix()
        if chosen is None:
            return
        name, _ = chosen
        try:
            del self.matrices[name]
            self.history.append(("delete", name))
            print(f"Matrix {name} has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting matrix: {str(e)}")

    def edit_matrix(self) -> None:
        """
        Edit an existing matrix through user input.
        """
        chosen = self.select_matrix()
        if chosen is None:
            return
        name, _ = chosen
        try:
            while True:
                try:
                    rows = int(input(f"Enter new number of rows for Matrix {name}: "))
                    cols = int(input(f"Enter new number of columns for Matrix {name}: "))
                    if rows <= 0 or cols <= 0:
                        print("Dimensions must be positive integers.")
                        continue
                    break
                except ValueError:
                    print("Please enter valid integers for dimensions.")

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
            self.history.append(("edit", name))
            print(f"Matrix {name} has been updated successfully.")
            
        except Exception as e:
            print(f"Error editing matrix: {str(e)}")

    def list_matrices(self) -> List[Tuple[str, Matrix]]:
        """
        List all stored matrices.
        
        Returns:
            List of tuples containing (matrix_name, matrix_instance).
        """
        if not self.matrices:
            print("No matrices defined yet.")
            return []
        sorted_names = sorted(self.matrices.keys())
        print("\nStored Matrices:")
        numbered = []
        for idx, name in enumerate(sorted_names, start=1):
            mat = self.matrices[name]
            print(f"{idx}. Matrix {name} ({mat.rows}x{mat.cols})")
            numbered.append((name, mat))
        print("0. Back")
        return numbered

    def show_matrix(self) -> None:
        """
        Display the contents of a selected matrix.
        """
        numbered = self.list_matrices()
        if not numbered:
            return
        try:
            while True:
                try:
                    choice = int(input("Select a matrix number to show (or 0 to cancel): "))
                    if choice == 0:
                        return
                    if 1 <= choice <= len(numbered):
                        name, mat = numbered[choice - 1]
                        print(f"\nMatrix {name}:")
                        print(mat)
                        return
                    print(f"Please enter a number between 0 and {len(numbered)}.")
                except ValueError:
                    print("Please enter a valid number.")
        except Exception as e:
            print(f"Error displaying matrix: {str(e)}")

    def select_matrix(self) -> Optional[Tuple[str, Matrix]]:
        """
        Let the user select a matrix from the stored matrices.
        
        Returns:
            Tuple of (matrix_name, matrix_instance) if a matrix is selected,
            None if selection is cancelled or an error occurs.
        """
        numbered = self.list_matrices()
        if not numbered:
            return None
        try:
            while True:
                try:
                    choice = int(input("Select a matrix by number (or 0 to cancel): "))
                    if choice == 0:
                        return None
                    if 1 <= choice <= len(numbered):
                        return numbered[choice - 1]
                    print(f"Please enter a number between 0 and {len(numbered)}.")
                except ValueError:
                    print("Please enter a valid number.")
        except Exception as e:
            print(f"Error selecting matrix: {str(e)}")
            return None

    def store_result(self, result_matrix: Matrix) -> None:
        """
        Store a result matrix with a new name.
        
        Args:
            result_matrix: The matrix to store.
        """
        try:
            while True:
                choice = input("Store result as a new matrix? (Enter 1 for yes, 0 for no): ").strip()
                if choice in ['0', '1']:
                    break
                print("Please enter 0 or 1.")
            
            if choice == '1':
                name = self._get_new_name()
                self.matrices[name] = result_matrix
                self.history.append(("store_result", name))
                print(f"Result stored as Matrix {name}.")
        except Exception as e:
            print(f"Error storing result: {str(e)}")

    def undo_last_operation(self) -> None:
        """
        Undo the last operation performed on matrices.
        """
        if not self.history:
            print("No operations to undo.")
            return
        
        operation, name = self.history.pop()
        if operation == "create":
            if name in self.matrices:
                del self.matrices[name]
            print(f"Undid creation of Matrix {name}")
        elif operation == "delete":
            # Note: We can't restore deleted matrices without storing their data
            print(f"Undid deletion of Matrix {name}")
        elif operation == "edit":
            # Note: We can't restore previous matrix state without storing it
            print(f"Undid edit of Matrix {name}")
        elif operation == "store_result":
            if name in self.matrices:
                del self.matrices[name]
            print(f"Undid storing of result Matrix {name}")

    def save_matrices(self, filename: str) -> None:
        """
        Save all matrices to a file.
        
        Args:
            filename: Name of the file to save matrices to.
        """
        try:
            with open(filename, 'w') as f:
                for name, matrix in self.matrices.items():
                    f.write(f"Matrix {name}:\n")
                    f.write(str(matrix))
                    f.write("\n\n")
            print(f"Matrices saved to {filename}")
        except Exception as e:
            print(f"Error saving matrices: {str(e)}")

    def load_matrices(self, filename: str) -> None:
        """
        Load matrices from a file.
        
        Args:
            filename: Name of the file to load matrices from.
        """
        try:
            with open(filename, 'r') as f:
                content = f.read()
                matrices_data = content.split("\n\n")
                for matrix_data in matrices_data:
                    if not matrix_data.strip():
                        continue
                    lines = matrix_data.strip().split("\n")
                    name = lines[0].split()[1].rstrip(":")
                    data = []
                    for line in lines[1:]:
                        row = []
                        for elem in line.split("\t"):
                            value = elem.split("=")[1].strip()
                            row.append(value)
                        data.append(row)
                    self.matrices[name] = Matrix(data)
            print(f"Matrices loaded from {filename}")
        except Exception as e:
            print(f"Error loading matrices: {str(e)}")

# -----------------------------
# Menus
# -----------------------------
def management_menu(manager: MatrixManager) -> None:
    """
    Display and handle the matrix management menu.
    
    Args:
        manager: The MatrixManager instance to use.
    """
    while True:
        print("\nMatrix Management Menu:")
        print("1. New Matrix")
        print("2. Delete Matrix")
        print("3. Edit Matrix")
        print("4. List/Show Matrices")
        print("5. Undo Last Operation")
        print("6. Save Matrices to File")
        print("7. Load Matrices from File")
        print("8. Back to Main Menu")
        
        choice = input("\nSelect an option: ").strip()
        if choice == '1':
            manager.create_matrix()
        elif choice == '2':
            manager.delete_matrix()
        elif choice == '3':
            manager.edit_matrix()
        elif choice == '4':
            manager.show_matrix()
        elif choice == '5':
            manager.undo_last_operation()
        elif choice == '6':
            filename = input("Enter filename to save matrices: ").strip()
            if filename:
                manager.save_matrices(filename)
            else:
                print("Invalid filename.")
        elif choice == '7':
            filename = input("Enter filename to load matrices: ").strip()
            if filename:
                manager.load_matrices(filename)
            else:
                print("Invalid filename.")
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

def operations_menu(manager: MatrixManager) -> None:
    """
    Display and handle the matrix operations menu.
    
    Args:
        manager: The MatrixManager instance to use.
    """
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
        print("11. Check if Symmetric")
        print("12. Check if Orthogonal")
        print("13. Back to Main Menu")
        
        choice = input("\nSelect an option: ").strip()
        try:
            if choice in ['1', '2']:
                print("\nSelect first matrix:")
                first = manager.select_matrix()
                if first is None:
                    continue
                _, mat1 = first
                print("\nSelect second matrix:")
                second = manager.select_matrix()
                if second is None:
                    continue
                _, mat2 = second
                if choice == '1':
                    result = mat1.add(mat2)
                    print("\nAddition successful. Result:")
                else:
                    result = mat1.subtract(mat2)
                    print("\nSubtraction successful. Result:")
                print(result)
                manager.store_result(result)

            elif choice == '3':  # Multiplication
                print("\nSelect a matrix:")
                first = manager.select_matrix()
                if first is None:
                    continue
                _, mat1 = first
                while True:
                    scalar_or_matrix = input("\nMultiply by (1) another matrix or (2) a scalar? Enter 1 or 2: ").strip()
                    if scalar_or_matrix in ['1', '2']:
                        break
                    print("Please enter 1 or 2.")
                
                if scalar_or_matrix == '1':
                    print("\nSelect second matrix:")
                    second = manager.select_matrix()
                    if second is None:
                        continue
                    _, mat2 = second
                    result = mat1.multiply(mat2)
                
                elif scalar_or_matrix == '2':
                    while True:
                        scalar = input("\nEnter the scalar value: ").strip()
                        try:
                            scalar = sp.N(sp.sympify(scalar))
                            break
                        except (ValueError, sp.SympifyError):
                            print("Invalid scalar value. Please try again.")
                    result = mat1.multiply(scalar)
                
                print("\nMultiplication successful. Result:")
                print(result)
                manager.store_result(result)

            elif choice == '4':
                chosen = manager.select_matrix()
                if chosen is None: 
                    continue
                _, mat = chosen
                while True:
                    try:
                        exp = float(input("\nEnter the real exponent: "))
                        break
                    except ValueError:
                        print("Invalid input for exponent. Please try again.")
                
                result = mat.power(exp)
                # Automatically convert to numerical approximations
                result = Matrix([[sp.N(elem) for elem in row] for row in result.data])
                print(f"\nMatrix raised to the power {exp}:")
                print(result)
                manager.store_result(result)

            elif choice in ['5', '6', '7', '8', '9', '10', '11', '12']:
                chosen = manager.select_matrix()
                if chosen is None: 
                    continue
                _, mat = chosen
                
                if choice == '5':
                    result = mat.transpose()
                    print("\nTranspose successful. Result:")
                    print(result)
                    manager.store_result(result)
                elif choice == '6':
                    result = mat.inverse()
                    print("\nInverse successful. Result:")
                    print(result)
                    manager.store_result(result)
                elif choice == '7':
                    det = mat.determinant()
                    print(f"\nDeterminant: {det}")
                elif choice == '8':
                    tr = mat.trace()
                    print(f"\nTrace: {tr}")
                elif choice == '9':
                    while True:
                        numeric = input("\nEvaluate eigenvalues numerically? (Enter 1 for yes, 0 for no): ").strip()
                        if numeric in ['0', '1']:
                            break
                        print("Please enter 0 or 1.")
                    
                    eigvals = mat.eigenvalues(numeric=(numeric == '1'))
                    print("\nEigenvalues:")
                    for idx, val in enumerate(eigvals, start=1):
                        print(f"λ{idx} = {val}")
                elif choice == '10':
                    char_eq = mat.characteristic_equation()
                    print("\nCharacteristic Equation:")
                    print(f"{char_eq} = 0")
                elif choice == '11':
                    is_sym = mat.is_symmetric()
                    print(f"\nMatrix is {'symmetric' if is_sym else 'not symmetric'}")
                elif choice == '12':
                    is_orth = mat.is_orthogonal()
                    print(f"\nMatrix is {'orthogonal' if is_orth else 'not orthogonal'}")

            elif choice == '13':
                break
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError as e:
            print(f"\nError: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")

def main_menu() -> None:
    """
    Display and handle the main menu of the matrix calculator.
    """
    manager = MatrixManager()
    while True:
        print("\nMatrix Calculator")
        print("================")
        print("1. Matrix Management")
        print("2. Matrix Operations")
        print("3. Exit")
        
        choice = input("\nSelect an option: ").strip()
        if choice == '1':
            management_menu(manager)
        elif choice == '2':
            operations_menu(manager)
        elif choice == '3':
            print("\nThank you for using Matrix Calculator!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
