"""
This is an implementation of evolutionary strategy.
Created by Dan on 11/13/2016
"""

import numpy as np
import scipy as scp

class evolutionary(object):
    """
    The framework of evolutionary algorithm
    """

    def __init__(self, measurement):
        """
        dummy: the dummy argument that I may want to put into the function.
        """
        self.mut_ratio = mut_ratio
        self.old_generation = None
        self.new_generation = None
        self.population = None
        # done with __init__


    def _mutation_(self, mut_ratio, OG, n_mut):
        """
        OG: the old generation of genes
        mut_ratio: the mutation ratio, some value between 0 and 1
        NG: the new generation of genes
        """
        N = len(OG)
        NG = OG
        n_mut = int(N*mut_ratio)
        mut_list = np.random.choice(N, n_mut, replace=False)
        rest_mut = OG[~mut_list] # the complementary array
        mut_assist = np.random.choice(N, 2*n_mut, replace = False).reshape((n_mut, 2))
        NG[mut_list] = OG[mut_list] + mut_ratio*(mut_assist[:,0] - mut_assist[:,1])

        return NG
        # done with _mutation_


    def _crossover_(self,OG_father, OG_mother, n_offspring = 2):
        """
        OG: the old genration of Genes, a 1-d array
        OG_father: the old generation, father individual.
        OG_mother: the old generation, mother individual;
        n_offspring: number of offsprings each pair of parent produces.
        rule: each gene of father and mother has 50 percent probability of contributing to the offspring
        """
        n_genes = len(OG_father)
        off_spring = []
        for noff in xrange(n_offspring):
            select = np.random.binomial(1, 0.5, size = n_genes)
            ind_f = np.where(select)
            ind_m = np.where(1-select)
            new_ofs = np.zeros_like(OG_father)
            new_ofs[ind_f] = OG_father[ind_f]
            new_ofs[ind_m] = OG_mother[ind_m]
            off_spring.append(new_ofs)

        return off_spring


    
