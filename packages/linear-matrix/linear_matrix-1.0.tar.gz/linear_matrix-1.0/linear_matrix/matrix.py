import numpy as np

class Matrix:
    def __init__(self, data):
        self.data = np.array(data)

    def __add__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.data + other.data)
        raise ValueError("Addition only allowed between Matrix objects")

    def __sub__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.data - other.data)
        raise ValueError("Subtraction only allowed between Matrix objects")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(np.dot(self.data, other.data))
        raise ValueError("Multiplication only allowed between Matrix objects")

    def transpose(self):
        return Matrix(self.data.T)

    def determinant(self):
        return np.linalg.det(self.data)

    def inverse(self):
        return Matrix(np.linalg.inv(self.data))

    def __repr__(self):
        return str(self.data)
