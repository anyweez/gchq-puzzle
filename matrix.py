import collections, random

def row2run(row):
    run = []
    count = 0
    
    for val in row:
        if val:
            count += 1
        elif count > 0:
            run.append(count)
            count = 0

    if count > 0:
        run.append(count)

    return run

class Matrix(object):
    def __init__(self, dim):
        self._dim = dim
        self._rows = []
        
        # Initialize all of the rows
        for i in xrange(dim):
            self._rows.append([False for x in xrange(dim)])
        
        self._xruns = [None for x in xrange(dim)]
        self._yruns = [None for x in xrange(dim)]
        
        self._count_actual = collections.Counter()
        self._count_target = collections.Counter()
        
        self._row_mapping = []
        
    def set(self, x, y, val):
        # Intentionally inverted. Data is stored per row, so first select
        # the correct row, then select the correct column in that row.
        self._rows[y][x] = val

    ## TODO: when this function is called, reorganize rows so that the most
    ## constrained come first. 
#    def pack(self):
#        self._row_mapping = [i for i in xrange(self._dim)]
#        self._row_mapping[0] = 1
#        self._row_mapping[1] = 0
#        random.shuffle(self._row_mapping)
#        
#        orig_rows = [list(row) for row in self._rows]
#        orig_runs = [list(run) for run in self._xruns]
#        
#        for orig_i, new_i in enumerate(self._row_mapping):
#            self._rows[new_i] = orig_rows[orig_i]    
#            self._xruns[new_i] = orig_runs[orig_i]
#            
#            print '%s %s => %s' % (self._xruns[new_i], orig_i, new_i)
#        
#        print self._xruns
#
#    def unpack(self):
#        new_rows = [list(row) for row in self._rows]
#        new_runs = [list(run) for run in self._xruns]
#        
#        for orig_i, new_i in enumerate(self._row_mapping):
#            self._rows[orig_i] = new_rows[new_i]
#            self._xruns[orig_i] = new_runs[new_i]
    
    def xruns(self, x, vals):
        self._xruns[x] = vals
    
    def yruns(self, y, vals):
        self._yruns[y] = vals
        
    def dim(self):
        return self._dim
        
    def _getrow(self, x):
        return self._rows[x]
    
    def _getcol(self, y):
        return [self._rows[i][y] for i in xrange(len(self._rows))]
        
    def _getxruns(self, x):
        return self._xruns[x]
    
    def _getyruns(self, y):
        return self._yruns[y]
        
    ## Determines whether a row meets the runs constraints
    def _validate(self, row, run):
        count = 0
        current_run_i = 0
        run_len = len(run)
        
        ## Run through the list of values and determine what the run
        ## should be. Compare to the value of `run` once each run leg
        ## gets tallied.
        for val in row:
            if val:
                count += 1
            elif count > 0:
                # If the there are too many legs or the value of a leg is not the
                # expected value then this row is not valid.
                if current_run_i >= run_len or count != run[current_run_i]:
                    return False
                else:
                    count = 0
                    current_run_i += 1

        if count > 0:
            # If there row ends in a row, there needs to be space left in the specified
            # run and the value of that last slot needs to be correct.
            return (current_run_i == run_len - 1) and run[current_run_i] == count
        else:
            return current_run_i == run_len
## This function is the validation function for the general-purpose generator. I need to
## modularize the validation function I suppose so that either one can be used. At this
## point you can just comment one or the other out. Nothing else needs to be changed.
#       def _validate(self, row, run):
#        self._count_actual.clear()
#        self._count_target.clear()
        
#        count = 0
    
#        for val in row:
#            if val:
#                count += 1
#            elif count > 0:
#                self._count_actual[count] += 1
#                count = 0

#        if count > 0:
#            self._count_actual[count] += 1

#        for val in run:
#            self._count_target[val] += 1
            
#        return self._count_actual == self._count_target

    def validate_row(self, x):
        return self._validate(self._getrow(x), self._xruns[x])   
    
    def validate_col(self, y):
        return self._validate(self._getcol(y), self._yruns[y])
    
    ##
    # Checks whether the matrix is valid according to the run restrictions
    # that've been placed on it.
    ##
    def validate(self, check_rows=True, check_cols=True):
        if check_rows:
            for i in xrange(self._dim):
                if not self.validate_row(i):
                    return False

        if check_cols:
            for i in xrange(self._dim):
                if not self.validate_col(i):
                    return False

        return True
    ##
    # Returns true if the matrix contains a column that makes a run impossible.
    ##
    def overloaded(self):
        for col in xrange(self._dim):
            run = row2run(self._getcol(col))

            # If we ever find a case where we've got a longer run than the longest
            # expected run, we've found an overloaded matrix.
            if len(run) > 0 and len(self._getyruns(col)) > 0 and max(run) > max(self._getyruns(col)):
                return True
        
        return False
        
    def show(self):
        for row in self._rows:
            print '  '.join(['X' if val else '-' for val in row])