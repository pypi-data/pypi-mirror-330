"""Testing the module with the python internal unittest module."""

import unittest

from addimportdir import importdir,removedir

# Import Matrix class from pymatroh
from pymatroh import Matrix

importdir()

# Prerequistes to test.
# Matrix dimensions 1x1, 2x2, 3x3, 4x4.
test_matrices_quad = [(1,1), (2,2), (3,3), (4,4)]
# Matrix length. 
testcases_length_quad_mat = [1, 2, 3, 4]
test_matrices_non_quad = [(1,2),(2,3),(1,4)]
testcases_length_non_quad_mat = [1,2,1]

# Tests if the created matrices are the specified length.

# Python matrix definition:
# mxn: m = row, n = col
#    n1 ,n2 ,n3
# m1:x11,x12,x13
# m2:x12,x22,x23
# => 2x3 matrix

# 2x2 = [[x1,x2],[y1,y2]] length(2)
# 3x2 = [[x1,x2],[y1,y2],[z1,z2]] length(3)
class TestPymatrohMatrix_Length(unittest.TestCase):
    """Test Matrix class of pymatroh module."""

    def setUp(self):

        self.quad_mat = test_matrices_quad
        self.quad_mat_len = testcases_length_quad_mat
        self.non_quad_mat = test_matrices_non_quad
        self.non_quad_mat_len = testcases_length_non_quad_mat


    # Test length of quadratic matrices.
    def test_mat_length_quad_mat(self):
        for ltest in range(len(self.quad_mat_len)):
            # Create matrix object.
            rm = Matrix(self.quad_mat[ltest][0],self.quad_mat[ltest][1])
            # Test if length of quadratic matrix is as long as specified.
            self.assertEqual(len(rm.create_int_matrix()),self.quad_mat_len[ltest])
            self.assertEqual(len(rm.create_float_matrix()),self.quad_mat_len[ltest])
            self.assertEqual(len(rm.create_complex_matrix()),self.quad_mat_len[ltest])
            self.assertEqual(len(rm.create_binary_matrix()),self.quad_mat_len[ltest])

    # Test length of non quadratic matrices.
    def test_mat_length_non_quad_mat(self):
        for ltest in range(len(self.non_quad_mat_len)):
            rm = Matrix(self.non_quad_mat[ltest][0],self.non_quad_mat[ltest][1])
            # Test if length of non quadratic matrix is as long as specified.
            self.assertEqual(len(rm.create_int_matrix()),self.non_quad_mat_len[ltest])
            self.assertEqual(len(rm.create_float_matrix()),self.non_quad_mat_len[ltest])
            self.assertEqual(len(rm.create_complex_matrix()),self.non_quad_mat_len[ltest])
            self.assertEqual(len(rm.create_binary_matrix()),self.non_quad_mat_len[ltest])

class TestPymatrohMatrix_ValueType(unittest.TestCase):
    """Test Matrix class of pymatroh module."""

    def setUp(self):

        self.quad_mat = test_matrices_quad
        self.quad_mat_len = testcases_length_quad_mat
        self.non_quad_mat = test_matrices_non_quad
        self.non_quad_mat_len = testcases_length_non_quad_mat

    # Test if all values of integer matrix are from type integer.
    def test_int_mat_value_type(self):
        # Test integer matrix.
        for ltest in range(len(self.quad_mat_len)):
            # Create matrix object.
            rm = Matrix(self.quad_mat[ltest][0],self.quad_mat[ltest][1])
            # Create integer matrix.
            imat = rm.create_int_matrix()
            # Check if each element of every submatrix is from type int.
            for childmat in imat:
                for element in childmat:
                    if type(element) != int:
                        raise TypeError("Non integer Type in integer matrix:", element)
    
    # Test if all values of float matrix are from type integer.
    def test_float_mat_value_type(self):
        for ltest in range(len(self.quad_mat_len)):
            rm = Matrix(self.quad_mat[ltest][0],self.quad_mat[ltest][1])
            fmat = rm.create_float_matrix()
            # Check if each element of every submatrix is from type float.
            for childmat in fmat:
                for element in childmat:
                    if type(element) != float:
                        raise TypeError("Non float Type in float matrix:", element)
    
    # Test if all values of complex matrix are from type integer.          
    def test_complex_mat_value_type(self):
        for ltest in range(len(self.quad_mat_len)):
            rm = Matrix(self.quad_mat[ltest][0],self.quad_mat[ltest][1])
            cmat = rm.create_complex_matrix()
            # Check if each element of every submatrix is from type complex.
            for childmat in cmat:
                for element in childmat:
                    if type(element) != complex:
                        raise TypeError("Non complex Type in complex matrix:", element)
    
    # Test if matrix only contains binary values.
    def test_binary_mat_value_type(self):
        # Test binary matrix.
        for ltest in range(len(self.quad_mat_len)):
            # Create matrix object.
            rm = Matrix(self.quad_mat[ltest][0],self.quad_mat[ltest][1])
            # Create binary matrix.
            bmat = rm.create_binary_matrix()
            for childmat in bmat:
                for element in childmat:
                    if element != 0 and element != 1:
                        raise ValueError("Non binary type in binary matrix:", element)

            
if __name__ == '__main__':
    # Verbose unittests.
    unittest.main(verbosity=2)
    removedir()