class Cell:
    def __init__(self, value):
        self.value = value
        self.parents = [None]
        self.position = (-999, -999)
    
    def __call__(self, value, position):
        self.value = value
        self.position = position
        return self

    def __repr__(self):
        return str(self.value)

    def __add__(self, r):
        return self.value + r
    
    def __sub__(self, r):
        return self.value - r

class Alignment:
    def __init__(self, root, string, score):
        self.root = root
        self.score = score
        self.strings = string
    
    def __repr__(self):
        return '-----------------\n' + self.strings[0]+ '\n' +self.strings[1] + '\nScore: ' + str(self.score)

def maxes(a, key=None):
    if key is None:
        key = lambda x: x
    m, max_list = key(a[0]), []
    for s in a:
        k = key(s)
        if k > m:
            m, max_list = k, [s]
        elif k == m:
            max_list.append(s)
    return m, max_list

def backtrack(F, formulas):
    rows, cols = (len(F), len(F[0]))
    cell = F[rows-1][cols-1]
    root_alignment = Alignment(cell, ('', ''), cell.value)
    stack = [root_alignment]
    alignments = []
    while(stack):
        alignment = stack.pop()
        cell = alignment.root
        
        for parent in cell.parents:
            if parent is None:
                alignments.append(alignment)
                continue
            if(parent.position == (-999, -999)):
                continue
            x, y = formulas(alignment, cell, parent)
            stack.append(Alignment(parent, (x,y), alignment.score))
    return alignments