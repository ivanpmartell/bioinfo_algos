from operator import itemgetter
import numpy as np #ONLY FOR 2D LIST PRETTY PRINT
from helper import maxes, backtrack, Cell as helper_cell

class Cell(helper_cell):
    def __init__(self, value, matrix):
        self.value = value
        self.matrix = matrix
        self.parents = [None]
        self.position = (-999, -999)

d = 2
e = 1
seq_a = 'ATCAGAGTC'
seq_b = 'TTCAGTC'

def main():
    """ Main program """
    F, max_cells = make_matrix()
    pretty_matrix = np.array(F)
    print(pretty_matrix)

    alignments = backtrack(F, backtrack_formulas, max_cells)
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
        I_y[i][0](0, (i, 0)).parents = [I_y[i-1][0]]
    for j in range(1, cols):
        matrix[0][j](0, (0, j)).parents = [matrix[0][j-1]]
        I_x[0][j](0, (0, j)).parents = [I_x[0][j-1]]

    max_cells = [matrix[0][0]]
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
            if(matrix[i][j].value > max_cells[0].value):
                max_cells = [matrix[i][j]]
            elif(matrix[i][j].value == max_cells[0].value):
                max_cells.append(matrix[i][j])
    
    return matrix, max_cells

def get_max_and_parents(cells, values):
    result, indices = maxes(range(len(values)), key=values.__getitem__)
    parents = itemgetter(*indices)(cells)
    if(not type(parents) == tuple):
        parents = tuple([parents])
    return result, parents

def backtrack_formulas(alignment, cell, parent):
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
    return x, y

def s(x_i, y_i):
    if x_i == y_i:
        return 2
    else:
        return -1

if __name__ == "__main__":
    main()
