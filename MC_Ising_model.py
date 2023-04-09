#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The code calculates the average magnetization |M| and energy
of an nd x nd dimensional spin lattice. In effect, it simulates
the phase transition in the lattice using Monte Carlo method.

The object "lattice" can take any of spins up, dipole, quadruplet,
and random configurations.

@author: alireza
"""

import numpy as np

class lattice(object):
    
    def __init__(self, nd):
        self.nd = nd
        self.array = np.zeros((self.nd, self.nd),dtype=int)

    def spins_up(self):
        for i in range(self.nd):
          for j in range(self.nd):
            self.array[i,j] = 1
        return self.array
    
    def dipole(self):
        half = int(self.nd/2)
        for i in range(self.nd):
            for j in range(half):
                self.array[i,j] = 1
        for i in range(self.nd):
            for j in range(half, self.nd):
                self.array[i,j] = -1
        return self.array
    
    def quadruplet(self):
        half = int(self.nd/2)
        for i in range(half):
            for j in range(half):
                self.array[i,j] = 1
            for j in range(half, self.nd):
                self.array[i,j] = -1
        for i in range(half, self.nd):
            for j in range(half):
                self.array[i,j] = -1
            for j in range(half, self.nd):
                self.array[i,j] = 1
        return self.array
    
    def rand_config(self):
        np.random.seed()
        for i in range(self.nd):
          for j in range(self.nd):
              self.array[i,j] = np.sign(2*np.random.rand()-1)
        return self.array


class params(lattice):
    
    def __init__(self, nd, lattice_name=''):
        lattice.__init__(self, nd)
        self.lattice_name = lattice_name
        self.energy = 0
        self.mag = 0
        
    def get_lattice(self):
        if self.lattice_name == 'spins_up':
            return lattice.spins_up(self)
        elif self.lattice_name == 'dipole':
            return lattice.dipole(self)
        elif self.lattice_name == 'quadruplet':
            return lattice.quadruplet(self)
        elif self.lattice_name == 'rand_config':
            return lattice.rand_config(self)
        else:
            print('Lattice configuration not found.')
            return None
        
    def get_params(self):
        try:
            config = params.get_lattice(self)
        except:
            print('Something went wrong.')
            return None
        
        self.mag = sum(sum(config))
        
        for i in range(self.nd):
          for j in range(self.nd):
            WF = config[(i+1)%self.nd,j] + config[(i-1)%self.nd,j] \
                + config[i,(j+1)%self.nd] + config[i,(j-1)%self.nd]
            self.energy += config[i,j]*WF
        self.energy /= 2.0
        
        parameters = {'energy':self.energy,
                 'magnetization':self.mag,
                 'configuration': config}

        return parameters
    
    def __str__(self):
        return str(params.get_lattice(self))
    
    
class mc_simulate(params):
    
    def __init__(self, T, cycles, nd, lattice_name=''):
        params.__init__(self, nd, lattice_name)
        self.T = T
        self.cycles = cycles
            
    def calculate(self):
        inv_T = 1/self.T
        dummy = params.get_params(self)
        energy = dummy['energy']
        mag = dummy['magnetization']
        config = dummy['configuration']
        iter_list, mag_list = [], []
        in_file = open('output.dat','w')
        
        for num in range(self.cycles):
            np.random.seed()
            i = int(self.nd*np.random.rand())
            j = int(self.nd*np.random.rand())
            spin = config[i,j]
            WF = config[(i+1)%self.nd,j] + config[(i-1)%self.nd,j] \
            + config[i,(j+1)%self.nd] + config[i,(j-1)%self.nd]
            delta_E = 2*spin*WF
            if np.exp(-float(delta_E)*inv_T) > np.random.rand():
                config[i,j] = -spin
                energy += delta_E
                mag -= 2*spin
            if num%10 == 0:
                in_file.write("%10d %10.5f %10.5f\n" % (num, float(energy),float(mag)))
                mag_list.append(mag)
                iter_list.append(num)
        in_file.close()
        
        return iter_list, mag_list
    
    def __str__(self):
        return 'T = ' + str(self.T) + ', ' + 'cycles = ' + str(self.cycles) + ', ' + '\n' \
                + 'lattice = ' + str(self.lattice_name) + ', ' + 'size = ' + str(self.nd)




# # Main Function
    # def main():   
    #     if __name__ == '__main__':
    #         obj = lattice(4)
    #         print(obj.spins_up())
