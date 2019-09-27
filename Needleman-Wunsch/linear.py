import numpy as np

d = 1

def main():
    """ Main program """
    seq_a = 'GATTACA'
    seq_b = 'GCATGCU'
    F = make_matrix(seq_a, seq_b)
    print(F)
    return 0

def make_matrix(a, b):
    x = np.array(list(' ' + a))
    y = np.array(list(' ' + b))
    F = np.zeros((len(x), len(y)))
    F_x_idx = np.indices([F.shape[0]])*d
    F_y_idx = np.indices([F.shape[1]])*d
    F[0] -= np.squeeze(F_x_idx)
    F[:,0] -= np.squeeze(F_y_idx)

    for i in range(1, F.shape[0]):
        for j in range(1, F.shape[1]):
            result = np.max([F[i-1,j-1] + s(x[i],y[j]),
                              F[i-1,j] - d,
                              F[i, j-1] - d])
            F[i, j] = result

    return F

def s(x_i, y_i):
    if x_i == y_i:
        return 1
    else:
        return -1

if __name__ == "__main__":
    main()
