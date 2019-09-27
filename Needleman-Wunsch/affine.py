import numpy as np

d = 11
e = 1

def main():
    """ Main program """
    seq_a = 'GATTACA'
    seq_b = 'GCATGCU'
    F = make_matrix(seq_a, seq_b)

    return 0

def make_matrix(a, b):
    x = np.array(list('_' + a))
    y = np.array(list('_' + b))
    M = np.zeros((len(x), len(y)))
    I_x = np.zeros_like(M)
    I_y = np.zeros_like(M)

    for i in range(1, F.shape[0]):
        for j in range(1, F.shape[1]):
            I_x[i, j] = np.max(M[i-1, j] - d,
                               I_x[i-1,j] - e)
            I_y[i, j] = np.max(M[i, j-1] - d,
                               I_x[i,j-1] - e)
            M[i, j] = np.max([M[i-1,j-1] + s(x[i],y[j]),
                              I_x[i-1,j-1] + s(x[i],y[j]),
                              I_y[i-1,j-1] + s(x[i],y[j])])
    print(F)
    return F

def s(x_i, y_i):
    if x_i == y_i:
        return 1
    else:
        return -1

if __name__ == "__main__":
    main()