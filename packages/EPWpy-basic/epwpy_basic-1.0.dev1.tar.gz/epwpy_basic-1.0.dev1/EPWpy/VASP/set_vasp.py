#
"""
QE class for interfacing with quantum espresso
"""
from __future__ import annotations
import numpy as np
import argparse
import os
from EPWpy.default.default import *
from EPWpy.structure.lattice import *
from EPWpy.structure.position_atoms import unit2prim
from EPWpy.utilities.k_gen import *
from EPWpy.utilities.epw_pp import *
from EPWpy.utilities.save_state import *
from EPWpy.utilities.printing import *
from EPWpy.utilities.constants import *

class set_VASP:
    """
    This class sets input files for quantum espresso and EPW. 
    The default values are provided in set_vals class
    """
    def __init__(self, type_input, system='si',code='.',env='mpirun'):
        """
        ** 
        Initialization of the set_VASP class
        **
        This class is mostly used for inheritance to 
        set the values for VASP calculation
        """
        self.system = system
        self.code = code
        self.home = os.getcwd()
        self.env = env
        os.system('mkdir '+self.system)

        self.default_values()
        self.set_values(type_input)

    def set_initial(self, type_input={}):
        """
        sets initial vasp inputs
        """
        self.structure = os.getcwd()+f'/{self.QE.structure}'
        if ('pseudo' in type_input.keys()):
            self.pseudo = type_input['pseudo']
        else:
            self.pseudo = os.getcwd()+f'/POTCAR'

        for key in type_input:
            for key in type_input['INCAR'].keys():
                #if (key in self.vasp_params.keys()):
                    self.vasp_params[key] = type_input['INCAR'][key]

        for key in type_input:
            for key in type_input['KPOINTS'].keys():
                #if (key in self.vasp_kpoint_params.keys()):
                    self.vasp_kpoint_params[key] = type_input['KPOINTS'][key]

    def set_vasp_incar(self, input_vasp):
        """
        sets the VASP INCAR file
        """
        if ('INCAR' in input_vasp.keys()):
            for key in input_vasp:
               for key in input_vasp['INCAR'].keys():
               #if (key in self.vasp_params.keys()):
                   self.vasp_params[key] = input_vasp['INCAR'][key]

    def set_vasp_kpoints(self, input_vasp):
        """
        sets the VASP KPOINTS file
        """
        if ('KPOINTS' in input_vasp.keys()):
            for key in input_vasp:
               for key in input_vasp['KPOINTS'].keys():
               #if (key in self.vasp_kpoint_params.keys()):
                   self.vasp_kpoint_params[key] = input_vasp['KPOINTS'][key]

        
