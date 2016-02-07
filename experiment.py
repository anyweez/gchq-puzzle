import random
# Local imports
import matrix as puzzle

##
# Create a random square matrix of the specified dimension.
##
def make(dim):
    matrix = puzzle.Matrix(dim)
    
    # Create the matrix
    for y in xrange(dim):
        trues = random.randint(0, dim)
        
        row = [row < trues for row in xrange(dim)]
        random.shuffle(row)
        
        for x in xrange(dim):
            matrix.set(x, y, row[x])

    # Now derive the run constraints
    for y in xrange(dim):
        matrix.xruns(y, puzzle.row2run(matrix._getrow(y)))

    for x in xrange(dim):
        matrix.yruns(x, puzzle.row2run(matrix._getcol(x)))

    print '-- input --'
    matrix.show()
    print ''
    # Reset the matrix
    for y in xrange(dim):
        for x in xrange(dim):
            matrix.set(x, y, False)
            
    return matrix
#
#   X   -   X   -   -
#   -   -   X   X   X
#   X   X   X   -   -
#   X   -   X   X   -
#   -   -   -   X   X
#
def test5():
    DIMENSION = 5
    matrix = puzzle.Matrix(DIMENSION)
    
    matrix.xruns(0, [1, 1])
    matrix.xruns(1, [3])
    matrix.xruns(2, [3])
    matrix.xruns(3, [1, 2])
    matrix.xruns(4, [2])
    
    matrix.yruns(0, [1, 2])
    matrix.yruns(1, [1])
    matrix.yruns(2, [4])
    matrix.yruns(3, [1, 2])
    matrix.yruns(4, [1, 1])
    
    return matrix

#
#   X   -   -   X   X   X
#   X   X   -   -   X   -
#   X   -   X   X   -   X
#   -   -   -   X   -   -
#   -   X   X   -   X   -
#   X   X   -   X   -   X
#
def test6():
    DIMENSION = 6
    matrix = puzzle.Matrix(DIMENSION)

    matrix.xruns(0, [1, 3])
    matrix.xruns(1, [2, 1])
    matrix.xruns(2, [2, 1, 1])
    matrix.xruns(3, [1])
    matrix.xruns(4, [1, 2])
    matrix.xruns(5, [1, 2, 1])
    
    matrix.yruns(0, [3, 1])
    matrix.yruns(1, [2, 1])
    matrix.yruns(2, [1, 1])
    matrix.yruns(3, [1, 1, 2])
    matrix.yruns(4, [2, 1])
    matrix.yruns(5, [1, 1, 1])
    
    return matrix
#
#   X   -   -   X   X   X   -
#   -   X   X   X   -   X   -
#   X   -   X   -   X   -   X
#   X   -   X   X   -   -   X
#   -   X   -   -   -   X   X
#   X   -   X   -   X   X   -
#   -   X   X   X   -   -   -
#
def test7():
    DIMENSION = 7
    matrix = puzzle.Matrix(DIMENSION)

    matrix.xruns(0, [1, 3])
    matrix.xruns(1, [3, 1])
    matrix.xruns(2, [1, 1, 1, 1])
    matrix.xruns(3, [1, 2, 1])
    matrix.xruns(4, [1, 2])
    matrix.xruns(5, [1, 1, 2])
    matrix.xruns(6, [3])
    
    matrix.yruns(0, [1, 2, 1])
    matrix.yruns(1, [1, 1, 1])
    matrix.yruns(2, [3, 2])
    matrix.yruns(3, [2, 1, 1])
    matrix.yruns(4, [1, 1, 1])
    matrix.yruns(5, [2, 2])
    matrix.yruns(6, [3])
    
    return matrix
#
#   X   -   -   X   X   X   -   -   X   X
#   X   X   -   -   X   -   X   X   X   -
#   -   X   X   -   -   -   X   X   X   X
#   X   X   X   X   -   -   -   -   X   -
#   X   -   -   -   X   X   X   -   X   -
#   -   X   -   X   X   -   -   -   -   -
#   -   -   -   X   -   -   -   X   -   -
#   -   X   X   -   -   X   X   -   -   X
#   X   -   -   X   -   X   -   -   X   X
#   -   -   X   X   X   -   -   -   X   -
#

def test10():
    DIMENSION = 10
    matrix = puzzle.Matrix(DIMENSION)
    
    matrix.xruns(0, [1, 3, 2])
    matrix.xruns(1, [2, 1, 3])
    matrix.xruns(2, [2, 4])
    matrix.xruns(3, [4, 1])
    matrix.xruns(4, [1, 3, 1])
    matrix.xruns(5, [1, 2])
    matrix.xruns(6, [1, 1])
    matrix.xruns(7, [2, 2, 1])
    matrix.xruns(8, [1, 1, 1, 2])
    matrix.xruns(9, [3, 1])
    
    matrix.yruns(0, [2, 2, 1])
    matrix.yruns(1, [3, 1, 1])
    matrix.yruns(2, [2, 1, 1])
    matrix.yruns(3, [1, 1, 2, 2])
    matrix.yruns(4, [2, 2, 1])
    matrix.yruns(5, [1, 1, 2])
    matrix.yruns(6, [2, 1, 1])
    matrix.yruns(7, [2, 1])
    matrix.yruns(8, [5, 2])
    matrix.yruns(9, [1, 1, 2])

    return matrix
    
def setup():  
    DIMENSION = 25
    matrix = puzzle.Matrix(DIMENSION)  
    
    matrix.xruns(0, [7, 3, 1, 1, 7])
    matrix.xruns(1, [1, 1, 2, 2, 1, 1])
    matrix.xruns(2, [1, 3, 1, 3, 1, 1, 3, 1])
    matrix.xruns(3, [1, 3, 1, 1, 6, 1, 3, 1])
    matrix.xruns(4, [1, 3, 1, 5, 2, 1, 3, 1])
    matrix.xruns(5, [1, 1, 2, 1, 1])
    matrix.xruns(6, [7, 1, 1, 1, 1, 1, 7])
    matrix.xruns(7, [3, 3])
    matrix.xruns(8, [1, 2, 3, 1, 1, 3, 1, 1, 2])
    matrix.xruns(9, [1, 1, 3, 2, 1, 1])
    matrix.xruns(10, [4, 1, 4, 2, 1, 2])
    matrix.xruns(11, [1, 1, 1, 1, 1, 4, 1, 3])
    matrix.xruns(12, [2, 1, 1, 1, 2, 5])
    matrix.xruns(13, [3, 2, 2, 6, 3, 1])
    matrix.xruns(14, [1, 9, 1, 1, 2, 1])
    matrix.xruns(15, [2, 1, 2, 2, 3, 1])
    matrix.xruns(16, [3, 1, 1, 1, 5, 1])
    matrix.xruns(17, [1, 2, 2, 5])
    matrix.xruns(18, [7, 1, 2, 1, 1, 1, 3])
    matrix.xruns(19, [1, 1, 2, 1, 2, 2, 1])
    matrix.xruns(20, [1, 3, 1, 4, 5, 1])
    matrix.xruns(21, [1, 3, 1, 3, 10, 2])
    matrix.xruns(22, [1, 3, 1, 1, 6, 6])
    matrix.xruns(23, [1, 1, 2, 1, 1, 2])
    matrix.xruns(24, [7, 2, 1, 2, 5])
    
    matrix.yruns(0, [7, 2, 1, 1, 7])
    matrix.yruns(1, [1, 1, 2, 2, 1, 1])
    matrix.yruns(2, [1, 3, 1, 3, 1, 3, 1, 3, 1])
    matrix.yruns(3, [1, 3, 1, 1, 5, 1, 3, 1])
    matrix.yruns(4, [1, 3, 1, 1, 4, 1, 3, 1])
    matrix.yruns(5, [1, 1, 1, 2, 1, 1])
    matrix.yruns(6, [7, 1, 1, 1, 1, 1, 7])
    matrix.yruns(7, [1, 1, 3])
    matrix.yruns(8, [2, 1, 2, 1, 8, 2, 1])
    matrix.yruns(9, [2, 2, 1, 2, 1, 1, 1, 2])
    matrix.yruns(10, [1, 7, 3, 2, 1])
    matrix.yruns(11, [1, 2, 3, 1, 1, 1, 1, 1])
    matrix.yruns(12, [4, 1, 1, 2, 6])
    matrix.yruns(13, [3, 3, 1, 1, 1, 3, 1])
    matrix.yruns(14, [1, 2, 5, 2, 2])
    matrix.yruns(15, [2, 2, 1, 1, 1, 1, 1, 2, 1])
    matrix.yruns(16, [1, 3, 3, 2, 1, 8, 1])
    matrix.yruns(17, [6, 2, 1])
    matrix.yruns(18, [7, 1, 4, 1, 1, 3])
    matrix.yruns(19, [1, 1, 1, 1, 4])
    matrix.yruns(20, [1, 3, 1, 3, 7, 1])
    matrix.yruns(21, [1, 3, 1, 1, 1, 2, 1, 1, 4])
    matrix.yruns(22, [1, 3, 1, 4, 3, 3])
    matrix.yruns(23, [1, 1, 2, 2, 2, 6, 1])
    matrix.yruns(24, [7, 1, 3, 2, 1, 1])
    
    return matrix