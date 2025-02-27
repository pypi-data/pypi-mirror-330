#
"""
QE class for interfacing with quantum espresso
"""

from __future__ import annotations

__author__= "Sabyasachi Tiwari"
__copyright__= "Copyright 2024, EPWpy project"
__version__= "1.0"
__maintainer__= "Sabyasachi Tiwari"
__maintainer_email__= "sabyasachi.tiwari@austin.utexas.edu"
__status__= "Production"
__date__= "May 03, 2024"

import numpy as np
import argparse
import os
import glob
from EPWpy.utilities.set_files import *
from EPWpy.default.default import *
from EPWpy.QE.write_QE import *
from EPWpy.structure.lattice import *
from EPWpy.utilities.k_gen import *
from EPWpy.utilities.epw_pp import *
from EPWpy.utilities.save_state import *
from EPWpy.utilities.EPW_util import *
from EPWpy.QE.PW_util import *
from EPWpy.QE.set_QE import *
from EPWpy.QE.PH_util import *
from EPWpy.utilities.printing import *# printing


class py_QE(set_dir, set_QE, write_QE_files):#(py_prepare,py_run,py_analysis):
    """
    This class builds input files for quantum espresso and EPW. 
    The default values are provided in set_vals class
    """
    def __init__(self,type_input,system='si',code='.',env='mpirun'):
        """ 
        Initialization of the py_QE class 
        **
        This class is standalone and can be used without EPWpy 
        **
        """
        self.system = system
        self.code = code
        self.home = os.getcwd()
        self.env = env
        os.system('mkdir '+self.system)

        self.default_values()
        self.set_values(type_input)
        self._read_master()
    

    def reset(self):
        """
        Reset for a calculation
        """
        print('obtaining nscf and ph attributes')
        self.set_work()
        self._read_master()
        self.set_home()

    def scf(self,control={},
                  system={},
               electrons={},
                    ions={},
                    cell={},
                 kpoints={},
         cell_parameters={},
                 hubbard={},
                     fcp={},
                solvents={},
             occupations={},
       atomic_velocities={},
             constraints={},
           atomic_forces={},
                    rism={},
                   cards={},
                    name='scf'):
        """ 
        scf calculation preparation 
        """
        self.set_work()
        """ 
        set the pw values
        """
        self.pw(control,
                  system,
               electrons,
                    ions,
                    cell,
                 kpoints,
         cell_parameters,
                 hubbard,
                     fcp,
                solvents,
             occupations,
       atomic_velocities,
             constraints,
           atomic_forces,
                    rism,
                   cards)


        self.write_scf(name=name)
        self.scf_file = name
        self.set_home()	

    def ph(self,phonons={}, 
                qpoints={},
                name='ph'):
        """ 
        Phonon calculation preparation 
        """

        self.set_work()
        self.set_phonons(phonons,qpoints)
        self.write_ph(name=name)
        self.ph_file = name
        self.save_PH()
        self.set_home()

    def nscf(self,control={},
                  system={},
               electrons={},
                    ions={},
                    cell={},
                 kpoints={},
         cell_parameters={},
                 hubbard={},
                     fcp={},
                solvents={},
             occupations={},
       atomic_velocities={},
             constraints={},
           atomic_forces={},
                    rism={},
                   cards={},
                   name='nscf'):

        """ 
        nscf calculation preparation 
        """
        self.set_work()        
        self.pw_control['calculation']='\'nscf\''
        self.pw(control,
                  system,
               electrons,
                    ions,
                    cell,
                 kpoints,
         cell_parameters,
                 hubbard,
                     fcp,
                solvents,
             occupations,
       atomic_velocities,
             constraints,
           atomic_forces,
                    rism,
                   cards)
        

        self.write_scf(name)
        self.nscf_file = name
        self.save_PW()
        self.set_home()	

    @decorated_warning
    def epw(self,epwin={},name='epw'): 
        """
        EPW calculation preparation 
        """
        self.set_work()
        self.epw_file = name
        self.epw_refresh = None
        try:
            self.read_PW()
            self.read_PH()
        except FileNotFoundError: 
            print(f'PW PH files not found')

        if((name =='epw1') or (name =='fbw') or (name =='fbw_mu')):
            self.epw_restart = False
        else:
            self.epw_restart = True
            try:
                self.read_EPW()
            except FileNotFoundError:
                self.epw_refresh = None
 
        self.set_epw(epwin)
        self.write_epw(name)
        self.save_EPW()         
        self.set_home()

    def q2r(self,q2r={},name='q2r'):
        """ 
        q2r calculation preparation 
        """

        self.set_work()
        self.set_q2r(q2r)    
        self.write_q2r(name=name)
        self.q2r_file = name
        self.set_home()

    def zg(self,zg={},azg={},name='zg'):
        """ 
        zg calculation preparation 
        """
        self.set_work()
        self.set_zg(zg,azg)
        self.write_zg(name=name)
        self.zg_file = name
        self.set_home()

    def eps(self,inputpp={},energy_grid={},name='eps'):
        """ 
        epsilon from qe preparation 
        """
        self.set_work()
        self.set_eps(inputpp,energy_grid)
        self.write_eps(name = name)
        self.eps_file = name
        self.set_home()

    def wannier(self,win={},pw2wan={},name='win'):
        """
        Wannier calculation
        """
        self.set_work()
        self.set_wannier(win,pw2wan)
        self.write_wann(name=name)
        self.wannier_file = name
        self.set_home()

    def pp(self):
        """
        Run PP for EPW if everything fails
        """
        self.set_work()
        os.chdir('./epw')
        run_pp(self.prefix)
        self.set_home()


    def pw(self,control,
                  system,
               electrons,
                    ions,
                    cell,
                 kpoints,
         cell_parameters,
                 hubbard,
                     fcp,
                solvents,
             occupations,
       atomic_velocities,
             constraints,
           atomic_forces,
                    rism,
                   cards):
        """ 
        PW setup and setting with a changing state
        """
        self.set_control(control)
        self.set_system(system)
        self.set_electrons(electrons)
        self.set_ions(ions)
        self.set_cell(cell)
        self.set_cell_parameters(cell_parameters)
        self.set_kpoints(kpoints)      
        #self.cards = cards
 
        #for card in cards:
        if (len(cards) != 0):
            self.set_cards(cards)

    def bands(self,bands={},name='bands'):
        self.set_work()
        self.write_bands(bands=bands,name=name)
        self.set_home()
        
    def nscf2supercond(self,nscf2supercond={},name='nscf2supercond'):
        self.set_work()
        self.write_nscf2supercond(nscf2supercond=nscf2supercond,name=name)
        self.set_home()

    def matdyn(self,matdyn={},kpoints={},name='matdyn'):
        self.set_work()
        self.set_matdyn(matdyn,kpoints)
        self.write_matdyn(matdyn=matdyn,name=name)
        self.set_home()
       
    def phdos(self,phdos={},name='phdos'):
        self.set_work()
        self.write_phdos(phdos=phdos,name=name)
        self.set_home()

    def dos(self,dos={},name='dos'):
        self.set_work()
        self.write_dos(dos=dos, name=name)
        self.set_home()
        
    def pdos(self,pdos={},name='pdos'):
        self.set_work()
        self.write_pdos(pdos=pdos, name=name)
        self.set_home()

    def save_PW(self):
        """
        Saves PW  state
        """
        dict1={'system':self.pw_system,
              'kpoints':self.pw_kpoints,
              'control':self.pw_control,
              'electrons':self.pw_electrons,
              'atomic_species':self.pw_atomic_species,
              'cell_parameters':self.pw_cell_parameters}

        if (len(self.cards) !=0):

            for card in self.cards.keys():

                dict1.update({card:self.cards[card]})

        self._save_json(self.nscf_file+'_save',dict1)#self.pw_system) 

    def PH_utilities(self):
        """
        Returns the PH utility class
        """
        prefix=self.prefix.replace('\'','')
        self.ph_util = PH_properties(f'{prefix}/{self.ph_fold}/{self.ph_file}.out')
        return(self.ph_util)

    def PW_utilities(self):
        """
        Returns the PW utility class
        """
        prefix=self.prefix.replace('\'','')
        self.pw_util = PW_properties(f'{prefix}/{self.scf_fold}/{self.scf_file}.out')
        return(self.pw_util)
 
    def EPW_utilities(self):
        """
        Returns the PW utility class
        """
        prefix=self.prefix.replace('\'','')
        self.EPW_util = EPW_properties(f'{prefix}/{self.epw_fold}/{self.epw_file}.out')
        return(self.EPW_util)
    
    def save_EPW(self):
        """
        Saves PW  state
        """
        dict1={'epw_data':self.epw_params,
               'refresh': '.true.'}
        self._save_json('epw_save',dict1)#self.pw_system) 
 
    def save_PH(self):
        """
        Saves PH  state
        """
        dict1={'ph_params':self.ph_params}
        self._save_json(self.ph_file+'_save',dict1)#self.pw_system) 


    def _save_json(self,folder,data):

        self.save=Save_state(' ',' ')
        self.save.folder = folder
        self.save.data = data
        self.save.save_state()

    def _read_master(self):
        
        for file in glob.glob("*.json"):
            #print(file)
            self.save=Save_state(' ',' ')            
            dict1=self._read_json(file.split('.json')[0])
            #print(dict1.keys())
            if('control' in dict1.keys()):
             #   print(dict1['control']['calculation']) 
                if(dict1['control']['calculation'] == '\'nscf\''):
                    self.nscf_file = file.split('_')[0]
                if(dict1['control']['calculation'] == '\'bands\''):
                    self.nscf_file = file.split('_')[0]

            if('ph_params' in  dict1.keys()):
                self.ph_file = file.split('_')[0]

            if('epw_params' in dict1.keys()):
                self.epw_file = file.split('_')[0]                         

            if('epwpy_params' in dict1.keys()):
                self._get_folds(dict1)                        
            
 #       print(self.nscf_file,self.ph_file)

    def read_PW(self):
        """
        Reads PW  state
        """
        self.save=Save_state(' ',' ')
        dict1=self._read_json(self.nscf_file+'_save')#self.pw_system) 
        self.pw_kpoints = dict1['kpoints']

    def read_PH(self):
        """
        Reads PH  state
        """
        self.save=Save_state(' ',' ')
        dict1=self._read_json(self.ph_file+'_save')#self.pw_system) 
        self.ph_params = dict1['ph_params']

    def read_EPW(self):
        """
        Reads PH  state
        """
        self.save=Save_state(' ',' ')
        dict1=self._read_json('epw_save')#self.pw_system) 
        self.epw_refresh = dict1['refresh']

    def _read_json(self,folder):

        self.save.folder = folder
        return(self.save.read_state())

    def _get_folds(self,dict1):
        """ Gets the folders for various calculations """
        self.state = dict1 
        self.scf_fold = dict1['scf_fold']

        try:
            self.nscf_fold = dict1['nscf_fold']
        except KeyError:
            pass

        try:
            self.ph_fold = dict1['ph_fold']
        except KeyError:
            pass

        try:
            self.epw_fold = dict1['epw_fold']
        except KeyError:
            pass
         
