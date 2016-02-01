import collections

class Matrix(object):
    def __init__(self, dim):
        self._dim = dim
        self._rows = []
        
        # Initialize all of the rows
        for i in xrange(dim):
            self._rows.append([False for x in xrange(dim)])
        
        self._xruns = [None for x in xrange(dim)]
        self._yruns = [None for x in xrange(dim)]
        
    def set(self, x, y, val):
        # Intentionally inverted. Data is stored per row, so first select
        # the correct row, then select the correct column in that row.
        self._rows[y][x] = val
        
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
    ## TODO: remove zeros just to make the API a bit more robust
    def _validate(self, row, run):
        actual = collections.Counter()
        count = 0
    
        for val in row:
            if val:
                count += 1
            elif count > 0:
                actual[count] += 1
                count = 0

        if count > 0:
            actual[count] += 1

        target = collections.Counter()
        
        for val in run:
            target[val] += 1
            
        return actual == target
#
#        count = 0
#        actual = set()
    
#        for val in row:
#            if val:
#                count += 1
#            elif count > 0:
#                actual.add(count)
#                count = 0
    
        # Leftovers at the end still need to be added
#        if count > 0:
#            actual.add(count)
        
#        print 'actual: %s, run: %s' % (actual, run)
#        return len(actual.symmetric_difference(run)) is 0
#        return len(actual.symmetric_difference(run)) is 0
#        return (actual.issubset(run) and actual.issuperset(run))
        
#        actual = sorted(actual)
#        for i, val in enumerate(sorted(run)):
#            try:
#                if actual[i] != val:
#                    return False
#            except IndexError:
#                return False
#        
#        return True

    def validate_row(self, x):
        valid = self._validate(self._getrow(x), self._xruns[x])
#        print 'Row %d valid? %s' % (x, valid)
        
        return valid
    
    def validate_col(self, y):
        valid = self._validate(self._getcol(y), self._yruns[y])
#        print 'Col %d valid? %s' % (y, valid)
        
        return valid
    
    def validate(self, check_rows=True, check_cols=True):
        rows = True
        cols = True
        
        if check_rows:
            rows = reduce(lambda x, y: x and y, [self.validate_row(i) for i in xrange(self._dim)])
        
        # Shortcut the second (slower) evaluation if the first one already fails.
        # TODO: why do I ever generate invalid rows if I'm using generators that only provide valid rows?
        if rows is False:
            return False
        
        if check_cols:
            cols = reduce(lambda x, y: x and y, [self.validate_col(i) for i in xrange(self._dim)])
        
        return (rows and cols)
            
    def show(self):
        for row in self._rows:
            print '  '.join(['X' if val else '-' for val in row])