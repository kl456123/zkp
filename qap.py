# -*- coding: utf-8 -*-
import numpy as np

def qeval(x):
    y = x**3
    return x + y + 5

# flattening
def qeval_flatten(x):
    sym_1 = x*x
    y = sym_1 * x
    sym_2 = y + x
    out = sym_2 + 5
    return out


# (S.dot(A) * (S.dot(B)) - S.dot(C) = 0
def r1cs():
    name = ['one', 'x', 'out', 'sym_1', 'y', 'sym_2']
    A = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [5, 0, 0, 0, 0, 1]
    ])

    B = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0]
    ])

    C = np.array([
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0]
    ])

    s = np.array([1, 3, 35, 9, 27, 30])
    S = np.array([
        [1, 1, 7, 1, 1, 2],
        [1, 2, 15, 4, 8, 10],
        [1, 3, 35, 9, 27, 30],
        [1, 4, 73, 16, 64, 68]
    ])

    # A*S.T*B*S.T - C*S.T = np.zeros((4,4))
    # (A_p*M).T*S.T = M.T*A_p.T*S.T
    # (B_p*M).T*S.T = M.T*B_p.T*S.T
    # M.T*(A_t*M.T*B_t-C_t) = 0

    M = []

    M = np.array([
        [1, 1, 1, 1],
        [1, 2, 3, 4],
        [1, 4, 9, 16],
        [1, 8, 27, 64]
    ])

    A_p_expect = np.array([
        [-5.0, 9.166, -5.0, 0.833],
        [8.0, -11.333, 5.0, -0.666],
        [0.0, 0.0, 0.0, 0.0],
        [-6.0, 9.5, -4.0, 0.5],
        [4.0, -7.0, 3.5, -0.5],
        [-1.0, 1.833, -1.0, 0.166]
    ])

    M_inv = np.linalg.inv(M)
    A_p = A.T.dot(M_inv)
    B_p = B.T.dot(M_inv)
    C_p = C.T.dot(M_inv)
    # print(A_p - A_p_expect)

    A_t = A_p.T.dot(S.T)
    B_t = B_p.T.dot(S.T)
    C_t = C_p.T.dot(S.T)

    # M.T.dot()
    T = A_t.dot(B_t) - C_t
    print(T)

if __name__=='__main__':
    r1cs()
