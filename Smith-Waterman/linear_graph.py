from operator import itemgetter
import numpy as np #ONLY FOR 2D LIST PRETTY PRINT

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
    def __init__(self, root, string):
        self.root = root
        self.score = 0
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

d = 2
seq_a = 'TGTTACGG'
seq_b = 'GGTTGACTA'

def main():
    """ Main program """
    F, max_cell = make_matrix()
    pretty_matrix = np.array(F)
    print(pretty_matrix)

    alignments = backtrack(F, max_cell)
    print('Best Alignments')
    for alignment in alignments:
        print(alignment)

    return 0

def make_matrix():
    x = list(' ' + seq_a)
    y = list(' ' + seq_b)
    rows, cols = (len(x), len(y))
    matrix = [[Cell(0) for j in range(cols)] for i in range(rows)]

    matrix[0][0].position = (0, 0)
    for i in range(1, rows):
        matrix[i][0](0, (i, 0)).parents = [matrix[0][0]]
    for j in range(1, cols):
        matrix[0][j](0, (0, j)).parents = [matrix[0][0]]

    max_cell = matrix[0][0]
    for i in range(1, rows):
        for j in range(1, cols):
            cells = {0: matrix[i-1][j-1],
                     1: matrix[i-1][j],
                     2: matrix[i][j-1],
                     3: None}
            values = [cells[0] + s(x[i],y[j]),
                      cells[1] - d,
                      cells[2] - d,
                      0]
            result, indices = maxes(range(len(values)), key=values.__getitem__)
            parents = itemgetter(*indices)(cells)
            if(not type(parents) == tuple):
                parents = tuple([parents])
            matrix[i][j](result, (i, j)).parents = parents
            if(matrix[i][j].value > max_cell.value):
                max_cell = matrix[i][j]
    
    return matrix, max_cell

def backtrack(F, max_cell):
    cell = max_cell
    stack = [Alignment(cell, ('', ''))]
    alignments = []
    while(stack):
        alignment = stack.pop()
        cell = alignment.root
        alignment.score += cell.value
        for parent in cell.parents:
            if parent is None:
                alignments.append(alignment)
                continue
            x = alignment.strings[0]
            y = alignment.strings[1]
            if(parent.position[0] < cell.position[0] and parent.position[1] < cell.position[1]):
                x = seq_a[parent.position[0]] + x
                y = seq_b[parent.position[1]] + y
            elif(parent.position[0] < cell.position[0]):
                x = seq_a[parent.position[0]] + x
                y = '-' + y
            elif(parent.position[1] < cell.position[1]):
                x = '-' + x
                y = seq_b[parent.position[1]] + y
            else:
                raise Exception
            stack.append(Alignment(parent, (x,y)))
    return alignments

def s(x_i, y_i):
    if x_i == y_i:
        return 3
    else:
        return -3

if __name__ == "__main__":
    main()
