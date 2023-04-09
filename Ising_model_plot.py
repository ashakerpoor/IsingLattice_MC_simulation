#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plots the average magnetizetion obtained from 
Monte Carlo simulation of an Ising lattice.

@author: alireza
"""

import pylab
import matplotlib as plt
import sys
sys.path.append('/path/to/MC_Ising_model/module/')
from MC_Ising_model import mc_simulate


L1 = mc_simulate(0.1, 50000, 40, 'quadruplet')
iter_list, mag_list = L1.calculate()

iter_list = [n/1000 for n in iter_list]
def demo(sty):
    plt.style.use(sty)
    pylab.xlabel(r'number of iterations $(\times 10^3)$')
    pylab.ylabel('<M>')
    pylab.ylim(-420, 420)
    pylab.rcParams['lines.markersize'] = 9
    pylab.rcParams['xtick.labelsize'] = 12
    pylab.rcParams['ytick.labelsize'] = 12
    pylab.rcParams['axes.labelsize'] = 12
    pylab.plot(iter_list, mag_list, 'C9', label = str(L1))
    pylab.legend(loc = 'upper right')
    pylab.grid(True)
    
demo('default')
