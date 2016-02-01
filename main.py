import itertools
# Local imports
import experiment

## Cycles through all possible permutations of the provided
## run, and yields each in order. Will only return valid 
## permutations (permutations that contain the described
## runs).
def generator(dim, run, validate):
    # Convert a run into one potential row. Doesn't matter which
    # one since we'll be finding all permutations of this row. Note
    # that this doesn't need to generate a valid row.
    def run2row(dim, run):
        row = [False for _ in xrange(dim)]
#        trues = sum(run)
#        row = [True if i < trues else False for i in xrange(dim)]

        for i in xrange(sum(run)):
            row[i] = True
            
        return row
    
    unique = set()
    for current in itertools.permutations(run2row(dim, run)):
        if current not in unique and validate(current, run):
            unique.add(current)
            yield current

def update_row(matrix, y, row):
    for x, val in enumerate(row):
        matrix.set(x, y, val)
    
# The main 'work' function. Recursively examine each row, starting
# at the bottom and working up towards y=1. All calls mutate a single
# object; this is in effect similar to many nested loops.
#
# Each instance returns True if the matrix is currently set to a 
# valid matrix, and False if it is not.
def traverse(matrix, y):
    # failure base case (when we traverse too deeply)
    if y < 0:
        return False
    # standard case: create a new generator that'll iterate through
    # all possible permutations for this row. update the matrix with
    # each permutation and then do the same thing on the next row. if
    # none of the iterations on later rows work, try the next pattern.
    else:
        for current in generator(matrix.dim(), matrix._getxruns(y), matrix._validate):
            update_row(matrix, y, current)
            
            if matrix.validate() or traverse(matrix, y - 1):
                return True

        return False
    
def main():
    global calls
    
    matrix = experiment.test5()
    calls = [0 for _ in xrange(matrix.dim())]
    
    ## Benchmark
#    count = 0
#    for current in generator(matrix.dim(), matrix._getxruns(0), matrix._validate):
#        print count
#        count += 1    
#    
#    print count
#    return
    
    # Do the work
    valid = traverse(matrix, matrix.dim() - 1)
    
    print 'Success? %s' % valid
    if valid:
        matrix.show()
    
if __name__ == '__main__':
    main()