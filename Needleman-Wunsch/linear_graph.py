from operator import itemgetter
import numpy as np #ONLY FOR 2D LIST PRETTY PRINT
from helper import maxes, backtrack, Cell

d = 2
seq_a = 'ATCAGAGTC'
seq_b = 'TTCAGTC'

def main():
    """ Main program """
    F = make_matrix()
    pretty_matrix = np.array(F)
    print(pretty_matrix)

    alignments = backtrack(F, backtrack_formulas)
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
        matrix[i][0](-i*d, (i, 0)).parents = [matrix[i-1][0]]
    for j in range(1, cols):
        matrix[0][j](-j*d, (0, j)).parents = [matrix[0][j-1]]

    for i in range(1, rows):
        for j in range(1, cols):
            cells = {0: matrix[i-1][j-1],
                     1: matrix[i-1][j],
                     2: matrix[i][j-1]}
            values = [cells[0] + s(x[i],y[j]),
                      cells[1] - d,
                      cells[2] - d]
            result, indices = maxes(range(len(values)), key=values.__getitem__)
            parents = itemgetter(*indices)(cells)
            if(not type(parents) == tuple):
                parents = tuple([parents])
            matrix[i][j](result, (i, j)).parents = parents
    
    return matrix

def backtrack_formulas(alignment, cell, parent):
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
    return x, y

def s(x_i, y_i):
    if x_i == y_i:
        return 2
    else:
        return -1

if __name__ == "__main__":
    main()
