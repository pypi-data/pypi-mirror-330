import numpy as np



class structure:
    """ This is the structure class that contains the structure info """

    def __init__(self,filename,data=[]):

        self.filename = filename
        if  (len(data.keys()) == 0):
            self.atom_pos_frac,\
            self.atom_pos_cart,\
            self.lattice_vector,\
            self.mat,\
            self.materials,\ 
            self.natoms, \
            self.lattice_const = self.atomic_positions()
        else:
            self.atom_pos_frac,\
            self.atom_pos_cart,\
            self.lattice_vector,\
            self.mat,\
            self.materials,\ 
            self.natoms, \
            self.lattice_const = self.atomic_positions()

    def atomic_position(self):

        atom_pos_frac,atom_cart,lattice_vector,mat,materials,natoms, a = main_extract([0.0,0.0],self.structure,T=1)
        return(atom_pos,lattice_vec,mat,materials,natoms,a)

      
