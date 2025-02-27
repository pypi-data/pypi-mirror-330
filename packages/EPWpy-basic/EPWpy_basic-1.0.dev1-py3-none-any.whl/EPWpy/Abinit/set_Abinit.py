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

class set_Abinit:
    """
    This class sets input files for quantum espresso and EPW. 
    The default values are provided in set_vals class
    """
    def __init__(self, type_input, system='si',code='.',env='mpirun'):
        """
        ** 
        Initialization of the set_QE class
        **
        This class is mostly used for inheritance 
        """
        self.system = system
        self.code = code
        self.home = os.getcwd()
        self.env = env
        os.system('mkdir '+self.system)

        self.default_values()
        self.set_values(type_input)

    def set_abi(self, input_abi):

        if ('quadrupole' in input_abi.keys()):
            self.abinit_params['control'] = self._quadrupole_calc()

        self._set_QE2Abinit()
       
        if('control' in input_abi.keys()):
            for key in input_abi['control'].keys():
                self.abinit_params['control'][key] = input_abi[key]
        if('common' in input_abi.keys()):
            self._set_common(input_abi,'atom')
            self._set_common(input_abi,'cell')
            self._set_common(input_abi,'kpoints')
            self._set_common(input_abi,'band')
            self._set_common(input_abi,'electron')
            self._set_common(input_abi,'pseudo')

            self.abinit_params['common']={}
            for key in input_abi['common'].keys():
                self.abinit_params['common'][key] = input_abi['common'][key]
 
    def _set_common(self,input_abi,keyin):
        delete = []
        for key in input_abi['common'].keys():
            if key in self.abinit_params[keyin].keys():
                self.abinit_params[keyin][key] = input_abi['common'][key]
                print(key,self.abinit_params[keyin][key])
                delete.append(key)
        for key in delete:
            del input_abi['common'][key]

    def _set_QE2Abinit(self):

        self._set_cell()        
        self._set_atom()
        self._set_band()
        self._set_kpoints()
        self._set_electron()
        self._set_pseudo()

    def _set_cell(self, input_abi = None):
        self.abinit_params['cell'] = {}
        a,self.abinit_params['cell']['rprim']= unit2prim(self.QE.pw_cell_parameters['lattice_vector'])
        a = a/Bohr2Ang
        self.abinit_params['cell']['acell'] = f'3*{a}'

    def _set_atom(self, input_abi= None):
        self.abinit_params['atom'] = {}       
        self.abinit_params['atom']['type']= 'xred' #pw_atomic_positions['atomic_position_type']
        typeat = [1]        
        typ_prev = self.QE.pw_atomic_positions['atoms'][0]
        self.abinit_params['atom']['ntypat']= self.QE.pw_system['ntyp'] #pw_atomic_positions['atomic_position_type']
        self.abinit_params['atom']['natom']= self.QE.pw_system['nat'] #pw_atomic_positions['atomic_position_type']

        self.abinit_params['atom']['znucl'] = []
        for i in range(len(self.QE.pw_atomic_species['mass'])):
            self.abinit_params['atom']['znucl'].append(int(np.floor(self.QE.pw_atomic_species['mass'][i]/2)))
 
        for i,typ in enumerate(self.QE.pw_atomic_positions['atoms']):
            if typ != typ_prev:
                typeat.append(typeat[-1]+1)
            else:
                if(i > 0):
                    typeat.append(typeat[-1])
        self.abinit_params['atom']['typat'] = typeat
        self.abinit_params['atom']['atomic_pos'] = self.QE.pw_atomic_positions['atomic_pos']

    def _set_band(self, input_abi= None):

        self.abinit_params['band'] = {}
        if ('nband' in self.QE.pw_system.keys()):
            self.abinit_params['nband'] = self.QE.pw_system['nband'] 
        else:
            self.abinit_params['band']['nband'] = None
        self.abinit_params['band']['ecut'] = self.QE.pw_system['ecutwfc']*Ryd2Hart
    
    def _set_kpoints(self, input_abi = None):

        self.abinit_params['kpoints'] = {}
        T = ' '
        for i in range(len(self.QE.pw_kpoints['kpoints'][:,0])):
            for j in range(len(self.QE.pw_kpoints['kpoints'][0,:])):
                T += str(int(self.QE.pw_kpoints['kpoints'][i,j]))+' '
        self.abinit_params['kpoints']['ngkpt'] = T # self.QE.pw_kpoints['kpoints']

    def _set_electron(self, input_abi = None):

        self.abinit_params['electron'] = {'nstep': 100,
                                          'diemac': 9.0}
    def _set_pseudo(self, input_abi = None):

        self.abinit_params['pseudo'] = {}
        self.abinit_params['pseudo']['pp_dirpath'] = self.QE.pw_control['pseudo_dir']
        self.abinit_params['pseudo']['pseudo'] = self.QE.pw_atomic_species['pseudo']
    
    def _quadrupole_calc(self):

        quadrupole_inp = {'ndtset':5,
                          '###dset 1': ' ', 
                          'getwfk1':0,
                          'kptopt1':1,
                          'nqpt1':0,
                          'tolvrs1':'1.0d-10',
                          '###dset 2': ' ',
                          'iscf2':-3,
                          'rfelfd2':2,
                          'tolwfr2':'1.0d-22',
                          'rfdir2':'1 1 1',  
                          '###dset 3': ' ',
                          'getddk3':2,
                          'iscf3':'-3',
                          'rf2_dkdk3':3,
                          'tolwfr3': '1.0d-22',
                          '###dset 4': ' ',
                          'getddk4':2,
                          'rfelfd4':3,
                          'rfphon4':1,
                          'rfatpol4':'1 2',
                          'rfdir4':'1 1 1',
                          'tolvrs4':'1.0d-10',
                          'prepalw4': 2,
                          '###dset 5': ' ',
                          'optdriver5': 10,
                          'get1wf5':4,
                          'get1den5':4,
                          'getddk5':2,
                          'getdkdk5':3,
                          'lw_qdrpl5':1, 
                          '###Common': ' ',
                          'getwfk': 1,
                          'useylm':1,
                          'kptopt':2}
 
        return(quadrupole_inp)
