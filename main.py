import itertools
import sys
# Local imports
import experiment

def memoize_generator(generator):
    storage = {}
    
    ## `generated` is the function that we return that keeps closure
    ## over the `storage` dict and will retrieve / store depending on
    ## whether data is available.
    def generated(dim, run, validate):
        run_t = tuple(run)
        yielded = set()

        # If  a record doesn't exist yet for this tuple, create it. Initialize
        # new generator and empty cache for rows.
        if run_t not in storage:
            storage[run_t] = {
                'generator': generator(dim, run, validate),
                'rows': []
            }
        
        # First run throw all pre-computed rows for quick winz. No computation to
        # be done for these, and number should be small. Keep track of how many
        # we evaluate here so that we can skip over them later.
        stored_i = 0
        for row in storage[run_t]['rows']:
            row_t = tuple(row)
            if row_t not in yielded:
                yielded.add(row_t)
                yield row
            
        # If the pre-computed results don't give us what we're looking for
        for row in storage[run_t]['generator']:
            storage[run_t]['rows'].append(row)

            row_t = tuple(row)
            if row_t not in yielded:
                yielded.add(row_t)
                yield row
        
        # Run through all cached values again now that everything's been computed.
        # Otherwise you can get into some race condition-y circumstances if more
        # than one row shared the same run sequence. Skip over the ones that we
        # ran beforehand.
        for row in storage[run_t]['rows'][stored_i:]:
            row_t = tuple(row)
            if row_t not in yielded:
                yielded.add(row_t)
                yield row

    return generated

def row_order(matrix):
    # Lowest numbers get ranked first.
    def rank(row_id):
        runs = matrix._getxruns(row_id)
        
        # If the row is all falses or all truths, do those first. Then basically
        # prefer rows that give the most information about runs, including both
        # runs (Trues) and the number of legs in a run (which indicates at least
        # one false between).
        if len(runs) is 0:
            return 0
        if sum(runs) is matrix.dim():
            return 0

        return float(1) / (sum(runs) + len(runs))
            
    return sorted([i for i in xrange(matrix.dim())], key=rank)

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
        if dim is 0 or len(run) is 0:
            yield [False for _ in xrange(dim)]
        # If there are no runs left then everything else is False
        else:
            current = run[0]
            run_len = len(run)
            # If it's the last leg of the run, you can have a gap size of
            # zero; otherwise you cannot. The gap can be split between before
            # and after the gap. 'Before' is particularly important for the
            # first leg of the run since there's no other way to start with one
            # or more falses in the run.
            for i in xrange(1 if run_len > 1 else 0, (dim - current) + 1):
                for pre_size, post_size in gaps(i):
                    pre = [False for _ in xrange(pre_size)]
                    filled = [True for _ in xrange(current)]
                    post = [False for _ in xrange(post_size)]   
                    
                    full = pre + filled + post
                    full_len = len(full)
                
                    # If we've filled up the row AND used up all the runs, yield.
                    if full_len is dim and run_len is 1:
                        yield full
                    # Otherwise if we're not done, keep searching.
                    elif full_len < dim:
                        for path in search(dim - full_len, run[1:], validate):
                            if full_len + len(path) is dim:
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
def traverse(matrix, row_ids, generator):
    # failure base case (when we traverse too deeply)
    if len(row_ids) is 0:
        return False
    # standard case: create a new generator that'll iterate through
    # all possible permutations for this row. update the matrix with
    # each permutation and then do the same thing on the next row. if
    # none of the iterations on later rows work, try the next pattern.
    else:
        row_id = row_ids[0]
        
        for current in generator(matrix.dim(), matrix._getxruns(row_id), matrix._validate):
            for i in row_ids[1:]:
                update_row(matrix, i, [False for _ in xrange(matrix.dim())])
            update_row(matrix, row_id, current)
            
            # If the new matrix is overloaded, nothing useful can happen with it so skip
            # this iteration. If it's not overloaded then (1) first check if it's already
            # valid, and short-circuit + return true if so, or (2) traverse deeper.
            if not matrix.overloaded() and (matrix.validate() or traverse(matrix, row_ids[1:], generator)):
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
#    generator = memoize_generator(generate_consecutive)
#    
#    for record in generator(matrix.dim(), matrix._getxruns(0), matrix._validate):
#        print record
#
#    for record in generator(matrix.dim(), matrix._getxruns(0), matrix._validate):
#        print record
#        
#    return

    matrix = experiment.test10()
    generator = memoize_generator(generate_consecutive)
    
    valid = traverse(matrix, row_order(matrix), generator)
    print valid
    matrix.show()
    
    return
       
    for iteration in xrange(iterations):
        print 'starting #%d' % iteration
        matrix = experiment.make(dimensions)
        generator = memoize_generator(generate_consecutive)
        
        # Do the work
        valid = traverse(matrix, row_order(matrix), generator)
        
        if not valid:
            raise Exception("Couldn't find a valid matrix even though there is one.")
        print '== output =='
        print 'Success? %s' % valid
        if valid:
            matrix.show()
            print ''
    
if __name__ == '__main__':
    main()