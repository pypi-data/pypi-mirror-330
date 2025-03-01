import unittest
from linear_matrix.matrix import Matrix

class TestMatrix(unittest.TestCase):
    def test_addition(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = A + B
        self.assertEqual(C.data.tolist(), [[6, 8], [10, 12]])

    def test_multiplication(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = A * B
        self.assertEqual(C.data.tolist(), [[19, 22], [43, 50]])

    def test_transpose(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.transpose().data.tolist(), [[1, 3], [2, 4]])

    def test_determinant(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertAlmostEqual(A.determinant(), -2)

    def test_inverse(self):
        A = Matrix([[4, 7], [2, 6]])
        A_inv = A.inverse()
        expected = [[0.6, -0.7], [-0.2, 0.4]]
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(A_inv.data[i][j], expected[i][j])

if __name__ == '__main__':
    unittest.main()
