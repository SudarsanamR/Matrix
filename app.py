from flask import Flask, render_template, request, jsonify
from Matrixcodes import Matrix
import sympy as sp
import json
import os

app = Flask(__name__)

# Matrix storage
MATRICES_FILE = 'matrices.json'

def load_matrices():
    if os.path.exists(MATRICES_FILE):
        with open(MATRICES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_matrices(matrices):
    with open(MATRICES_FILE, 'w') as f:
        json.dump(matrices, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matrices', methods=['GET'])
def get_matrices():
    return jsonify(load_matrices())

@app.route('/matrices', methods=['POST'])
def save_matrix():
    try:
        data = request.get_json()
        name = data['name']
        matrix_data = data['matrix']
        
        matrices = load_matrices()
        matrices[name] = matrix_data
        save_matrices(matrices)
        
        return jsonify({'message': f'Matrix {name} saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/matrices/<name>', methods=['DELETE'])
def delete_matrix(name):
    try:
        matrices = load_matrices()
        if name in matrices:
            del matrices[name]
            save_matrices(matrices)
            return jsonify({'message': f'Matrix {name} deleted successfully'})
        return jsonify({'error': f'Matrix {name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/matrices/<name>', methods=['PUT'])
def update_matrix(name):
    try:
        data = request.get_json()
        matrix_data = data['matrix']
        
        matrices = load_matrices()
        if name in matrices:
            matrices[name] = matrix_data
            save_matrices(matrices)
            return jsonify({'message': f'Matrix {name} updated successfully'})
        return jsonify({'error': f'Matrix {name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        operation = data['operation']
        matrix_a = Matrix(data['matrixA'])
        matrix_b = Matrix(data['matrixB']) if data.get('matrixB') else None
        scalar = data.get('scalar')

        if operation == 'add':
            result = matrix_a.add(matrix_b)
        elif operation == 'subtract':
            result = matrix_a.subtract(matrix_b)
        elif operation == 'multiply':
            result = matrix_a.multiply(matrix_b)
        elif operation == 'scalar_multiply':
            result = matrix_a.multiply(scalar)
        elif operation == 'transpose':
            result = matrix_a.transpose()
        elif operation == 'determinant':
            result = matrix_a.determinant()
        elif operation == 'inverse':
            result = matrix_a.inverse()
        elif operation == 'eigenvalues':
            result = matrix_a.eigenvalues(numeric=True)
        elif operation == 'characteristic':
            result = matrix_a.characteristic_equation()
        elif operation == 'power':
            if scalar is None:
                return jsonify({'error': 'Please provide a power value'}), 400
            result = matrix_a.power(scalar)
        elif operation == 'trace':
            result = matrix_a.trace()
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        # Convert result to a format suitable for JSON
        if isinstance(result, Matrix):
            result_data = [[float(sp.N(elem)) for elem in row] for row in result.data]
        elif isinstance(result, list):
            result_data = [float(sp.N(elem)) for elem in result]
        else:
            result_data = float(sp.N(result))

        return jsonify({'result': result_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/check_property', methods=['POST'])
def check_property():
    try:
        data = request.get_json()
        property_name = data['property']
        matrix_a = Matrix(data['matrixA'])

        if property_name == 'symmetric':
            result = matrix_a.is_symmetric()
            message = "Matrix is symmetric" if result else "Matrix is not symmetric"
        elif property_name == 'orthogonal':
            result = matrix_a.is_orthogonal()
            message = "Matrix is orthogonal" if result else "Matrix is not orthogonal"
        elif property_name == 'invertible':
            try:
                matrix_a.inverse()
                message = "Matrix is invertible"
            except ValueError:
                message = "Matrix is not invertible"
        elif property_name == 'diagonalizable':
            try:
                matrix_a.power(1)  # Try to diagonalize
                message = "Matrix is diagonalizable"
            except ValueError:
                message = "Matrix is not diagonalizable"
        else:
            return jsonify({'error': 'Invalid property'}), 400

        return jsonify({'result': message})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 