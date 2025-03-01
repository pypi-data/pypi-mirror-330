"""
Pymatroh

A cross plattform matrix creation module for Python.

Usage:
    from pymatroh import Matrix
    im = Matrix(2,2)
    im.create_int_matrix()

Return:
    [[100, 24], [90, 84]]

Usage:
    from pymatroh import Matrix
    fm = Matrix(2,2)
    fm.create_float_matrix()

Return:
    [[0.3476066056691818, 82.64139933693019], [55.6682714565969, 37.442624968338635]]

Usage:
    from pymatroh import Matrix
    cm = Matrix(2,1)
    cm.create_complex_matrix()

Return:
    [[(16.081037664553943+86.97288344375117j)], [(21.18506273716121+92.88016833034504j)]]

Usage:
    from pymatroh import Matrix
    cm = Matrix(2,1,applyround=True)
    cm.create_complex_matrix()

Return:
    [[(44+61j)], [(26+64j)]]

Usage:
    import pymatroh
    im = pymatroh.Matrix(1,1)
    im.create_int_matrix()

Return:
    [[53]]    

Author: IT-Administrators
License: MIT

"""

# Include necessary modules.
import random

class Matrix:
    """Create a matrix containing only integers."""

    def __init__(self, row: int, col: int, irange = 100, applyround = False):
        self.row = row
        self.col = col
        self.irange = irange
        self.applyround = applyround

    def create_int_matrix(self):
        """Create a random integer matrix."""

        matrix = []
        for i in range(self.row):
            childmatrix = []
            for j in range(self.col):
                childmatrix.append(random.randint(0, self.irange))
            matrix.append(childmatrix)
        return matrix
    
    def create_float_matrix(self):
        """Create a random float matrix."""

        matrix = []
        for i in range(self.row):
            childmatrix = []
            for j in range(self.col):
                if self.applyround == False:
                    childmatrix.append(random.uniform(0.0, self.irange))
                else:
                    childmatrix.append(round(random.uniform(0.0, self.irange), 3))
            matrix.append(childmatrix)
        return matrix
    
    def create_complex_matrix(self):
        """Create a random matrix with complex values."""

        matrix = []
        for i in range(self.row):
            childmatrix = []
            for j in range(self.col):
                if self.applyround == False:
                    childmatrix.append(complex(random.uniform(0.0, self.irange), random.uniform(0.0, self.irange)))
                else:
                    childmatrix.append(complex(round(random.uniform(0.0, self.irange), 3), round(random.uniform(0.0, self.irange), 3)))
            matrix.append(childmatrix)
        return matrix
    
    def create_binary_matrix(self):
        """Create a random binary matrix."""
        
        self.irange = 1
        matrix = []
        for i in range(self.row):
            childmatrix = []
            for j in range(self.col):
                childmatrix.append(random.randint(0, self.irange))
            matrix.append(childmatrix)
        return matrix

__all__ = ["Matrix"]