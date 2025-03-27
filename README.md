# Matrix Calculator Web Application

A web-based matrix calculator that provides various matrix operations including addition, subtraction, multiplication, transpose, determinant, inverse, and eigenvalues calculation.

## Features

- Matrix addition and subtraction
- Matrix multiplication (with another matrix or scalar)
- Matrix transpose
- Matrix determinant
- Matrix inverse
- Eigenvalues calculation
- Modern, responsive web interface
- Real-time matrix dimension adjustment
- Error handling and validation

## Setup

1. Make sure you have Python 3.7 or higher installed.

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `templates` directory and move the `index.html` file into it:
   ```bash
   mkdir templates
   mv index.html templates/
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Enter the dimensions for Matrix A and Matrix B using the input fields.
2. Fill in the matrix elements using the input boxes.
3. Select the desired operation from the buttons below the matrices.
4. View the result in the result section.

## Project Structure

- `app.py`: Flask application server
- `Matrixcodes.py`: Matrix operations implementation
- `templates/index.html`: Web interface
- `requirements.txt`: Python package dependencies

## Error Handling

The application includes comprehensive error handling for:
- Invalid matrix dimensions
- Non-invertible matrices
- Invalid input values
- Operation-specific errors

## Contributing

Feel free to submit issues and enhancement requests! 