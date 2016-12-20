'''
Simplex method
'''
import numpy as np


def simplex(values, paras, maximizing = True, gain = 1.0):
    '''
    A small program for evaluating simplex and return the superior and inferior indexes
    gain = 1.0: simple flip
    '''
    ind_max, ind_min = (np.argmax(values), np.argmin(values))
    if maximizing:
        ind_sup = ind_max # the superior index
        ind_inf = ind_min # the inferior index
    else:
        ind_sup = ind_min
        ind_inf = ind_max

    paras_sup, paras_inf = (paras[ind_sup], paras[ind_inf])
    # assume that the update is along a line in the parameter space.
    para_new = gain*(paras_sup - paras_inf) + paras_sup # update the paras_inf
    return para_new, ind_inf # return the index of the inferior
    # done with simplex


def main():
    a = np.random.randn(5)
    paras = np.random.randn(6,5)
    para_new = simplex(a, paras)
    print(para_new)


if __name__ == '__main__':
    main()
