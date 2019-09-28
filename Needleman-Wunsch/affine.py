import numpy as np

d = 11
e = 1

def main():
    """ Main program """
    seq_a = 'GATTACA'
    seq_b = 'GCATGCU'
    F = make_matrix(seq_a, seq_b)
    print(F)
    return 0

def make_matrix(a, b):
    x = np.array(list('_' + a))
    y = np.array(list('_' + b))
    M = np.zeros((len(x), len(y)))
    I_x = np.zeros_like(M)
    I_y = np.zeros_like(M)

    M_x_idx = np.squeeze((np.indices([M.shape[0]])-1)*e+d)
    M_y_idx = np.squeeze((np.indices([M.shape[1]])-1)*e+d)
    M[0] -= M_x_idx
    I_x[0] -= M_x_idx
    M[:,0] -= M_y_idx
    I_y[:,0] -= M_y_idx
    M[0,0] += M_x_idx[0]

    M = M.astype(int)
    I_x = I_x.astype(int)
    I_y = I_y.astype(int)
    for i in range(1, M.shape[0]):
        for j in range(1, M.shape[1]):
            I_x[i, j] = np.max([M[i-1, j] - d,
                               I_x[i-1,j] - e])
            I_y[i, j] = np.max([M[i, j-1] - d,
                               I_x[i,j-1] - e])
            M[i, j] = np.max([M[i-1,j-1] + s(x[i],y[j]),
                              I_x[i-1,j-1],
                              I_y[i-1,j-1]])
    return M

def s(x_i, y_i):
    if x_i == y_i:
        return 1
    else:
        return -1

if __name__ == "__main__":
    main()