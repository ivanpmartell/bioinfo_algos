from operator import itemgetter
import numpy as np #ONLY FOR 2D LIST PRETTY PRINT

class Cell:
    def __init__(self, value, matrix):
        self.value = value
        self.matrix = matrix
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
e = 1
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

from_matrix = {'M': 0, 'I_x': 1, 'I_y': 2}
def make_matrix():
    x = list(' ' + seq_a)
    y = list(' ' + seq_b)
    rows, cols = (len(x), len(y))
    matrix = [[Cell(0, from_matrix['M']) for j in range(cols)] for i in range(rows)]
    matrix[0][0].position = (0, 0)
    I_x = [[Cell(0, from_matrix['I_x']) for j in range(cols)] for i in range(rows)]
    I_x[0][0].position = (0, 0)
    I_y = [[Cell(0, from_matrix['I_y']) for j in range(cols)] for i in range(rows)]
    I_y[0][0].position = (0, 0)

    for i in range(1, rows):
        matrix[i][0](0, (i, 0)).parents = [matrix[i-1][0]]
        I_y[i][0](0, (i, 0)).parents = [I_y[0][i-1]]
    for j in range(1, cols):
        matrix[0][j](0, (0, j)).parents = [matrix[0][j-1]]
        I_x[0][j](0, (0, j)).parents = [I_x[0][j-1]]

    max_cell = matrix[0][0]
    for i in range(1, rows):

        for j in range(1, cols):
            I_x_cells = {0: matrix[i][j-1],
                         1: I_x[i][j-1]}
            I_x_values = [I_x_cells[0] - d,
                          I_x_cells[1] - e]
            result, parents = get_max_and_parents(I_x_cells, I_x_values)
            I_x[i][j](result, (i, j)).parents = parents

            I_y_cells = {0: matrix[i-1][j],
                         1: I_y[i-1][j]}
            I_y_values = [I_y_cells[0] - d,
                          I_y_cells[1] - e]
            result, parents = get_max_and_parents(I_y_cells, I_y_values)
            I_y[i][j](result, (i, j)).parents = parents

            matrix_cells = {0: matrix[i-1][j-1],
                            1: I_x[i][j],
                            2: I_y[i][j],
                            3: None}
            matrix_values = [matrix_cells[0] + s(x[i],y[j]),
                             matrix_cells[1].value,
                             matrix_cells[2].value,
                             0]
            result, parents = get_max_and_parents(matrix_cells, matrix_values)
            matrix[i][j](result, (i, j)).parents = parents
            if(matrix[i][j].value > max_cell.value):
                max_cell = matrix[i][j]
    
    return matrix, max_cell

def get_max_and_parents(cells, values):
    result, indices = maxes(range(len(values)), key=values.__getitem__)
    parents = itemgetter(*indices)(cells)
    if(not type(parents) == tuple):
        parents = tuple([parents])
    return result, parents

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
            if(cell.matrix == from_matrix['M']):
                x = seq_a[parent.position[0]] + x
                y = seq_b[parent.position[1]] + y
            elif(cell.matrix == from_matrix['I_y']):
                x = seq_a[parent.position[0]] + x[1:]
                y = '-' + y[1:]
            elif(cell.matrix == from_matrix['I_x']):
                x = '-' + x[1:]
                y = seq_b[parent.position[1]] + y[1:]
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
