import itertools
import sys
# Local imports
import experiment

## Cycles through all possible permutations of the provided run, and 
## yields each in order. A 'valid' permutation in this case is one that
## contains all described run lengths, though not necessarily in the
## prescribed order.
def generate_all(dim, run, validate):
    # Convert a run into one potential row. Doesn't matter which
    # one since we'll be finding all permutations of this row. Note
    # that this doesn't need to generate a valid row.
    def run2row(dim, run):
        trues = sum(run)   
        return [i < trues for i in xrange(dim)]
    
    unique = set()
    for current in itertools.permutations(run2row(dim, run)):
        if current not in unique and validate(current, run):
            unique.add(current)
            yield current

def generate_consecutive(dim, run, validate):
    def gaps(size):
        if size is 0:
            yield (0, 0)
        else:
            for i in xrange(size + 1):
                yield (i, size - i)
    
    # Each execution is expected to return a list of length DIM.
    def search(dim, run, validate):
        if dim is 0:
            yield []
        # If there are no runs left then everything else is False
        elif len(run) is 0:
            yield [False for _ in xrange(dim)]
        else:
            current = run[0]
            
            # If it's the last leg of the run, you can have a gap size of
            # zero; otherwise you cannot. The gap can be split between before
            # and after the gap. 'Before' is particularly important for the
            # first leg of the run since there's no other way to start with one
            # or more falses in the run.
            for i in xrange(1 if len(run) > 1 else 0, (dim - current) + 1):
                for pre_size, post_size in gaps(i):
                    pre = [False for _ in xrange(pre_size)]
                    filled = [True for _ in xrange(current)]
                    post = [False for _ in xrange(post_size)]   
                    
                    full = pre + filled + post
                
                    # If we've filled up the row AND used up all the runs, yield.
                    if len(full) is dim and len(run) is 1:
                        yield full
                    # Otherwise if we're not done, keep searching.
                    elif len(full) < dim:
                        for path in search(dim - len(full), run[1:], validate):
                            if len(full + path) is dim:
                                yield full + path
    
    # Maintain a set that caches examples that have already been returned so that all generated
    # solutions are unique. This trades space for execution speed, and branching factor of the
    # recursive traversal in traverse() in this case (which means it's a significant speedup, 
    # especially on larger matrices).
    cache = set()
    for path in search(dim, run, validate):
        path_tup = tuple(path)
        if path_tup not in cache and validate(path_tup, run):
            cache.add(path_tup)
            yield path

def update_row(matrix, y, row):
    for x, val in enumerate(row):
        matrix.set(x, y, val)
    
# The main 'work' function. Recursively examine each row, starting
# at the bottom and working up towards y=1. All calls mutate a single
# object; this is in effect similar to many nested loops.
#
# Each instance returns True if the matrix is currently set to a 
# valid matrix, and False if it is not.
def traverse(matrix, y, generator):
    # failure base case (when we traverse too deeply)
    if y < 0:
        return False
    # standard case: create a new generator that'll iterate through
    # all possible permutations for this row. update the matrix with
    # each permutation and then do the same thing on the next row. if
    # none of the iterations on later rows work, try the next pattern.
    else:
        for current in generator(matrix.dim(), matrix._getxruns(y), matrix._validate):
#            print 'possibility for run <%s>: %s' % (matrix._getxruns(y), current)
            for i in xrange(y):
                update_row(matrix, i, [False for _ in xrange(matrix.dim())])
            update_row(matrix, y, current)
            
            # If the new matrix is overloaded, nothing useful can happen with it so skip
            # this iteration. If it's not overloaded then (1) first check if it's already
            # valid, and short-circuit + return true if so, or (2) traverse deeper.
#            if not matrix.overloaded() and (matrix.validate() or traverse(matrix, y - 1, generator)):
            if matrix.validate() or traverse(matrix, y - 1, generator):
                return True

        return False
    
def main():
    dimensions = 5
    iterations = 1
    if len(sys.argv) > 1:
        dimensions = int(sys.argv[1])
        
        if len(sys.argv) > 2:
            iterations = int(sys.argv[2])
    
#    matrix = experiment.make(dimensions)
#    for pattern in generate_consecutive(dimensions, [4,], matrix._validate):
#        print 'solution: %s' % pattern
        
#    return
    
    for iteration in xrange(iterations):
        print 'starting #%d' % iteration
        matrix = experiment.make(dimensions)
        # Do the work
        valid = traverse(matrix, matrix.dim() - 1, generate_consecutive)
    
        if not valid:
            raise Exception("Couldn't find a valid matrix even though there is one.")
        print '-- output --'
        print 'Success? %s' % valid
        if valid:
            matrix.show()
    
if __name__ == '__main__':
    main()