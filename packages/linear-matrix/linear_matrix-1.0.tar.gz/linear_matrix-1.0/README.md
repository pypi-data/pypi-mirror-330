# Linear Matrix

Linear Matrix is a Python library for performing linear algebra matrix operations.

## Features
- Matrix Addition
- Matrix Multiplication
- Determinants
- Inverse Matrices
- Transposition
- Eigenvalues & Eigenvectors

## Installation
```sh
pip install linear-matrix
```

## Usage

```python
from linear_matrix.matrix import Matrix

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

# Matrix addition
C = A + B
print(C)

# Matrix multiplication
D = A * B
print(D)

# Transpose
print(A.transpose())

# Determinant
print(A.determinant())

# Inverse
print(A.inverse())
```

## License
MIT License
