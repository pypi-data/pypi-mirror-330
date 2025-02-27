# W.I.P
import numpy as np
import argparse
import os
from EPWpy.default.default import *
from EPWpy.Abinit.write_Abinit import *
from EPWpy.Abinit.set_Abinit import *
from EPWpy.structure.lattice import *
from EPWpy.utilities.set_files import *
from EPWpy.utilities.k_gen import *
from EPWpy.EPWpy_prepare import *
from EPWpy.EPWpy_run import *
from EPWpy.structure.lattice import *

class py_Abinit(set_dir, set_Abinit):#(py_prepare,py_run,py_analysis):
    """
    This code builds an interface to abinit 
    """
    def __init__(self,QE,type_input={},system='si',code='.',env='mpirun'):
        self.system=system
        self.code=code
        self.home=os.getcwd()
        self.env=env
        os.system('mkdir '+self.system)
        self.QE = QE
        self.verbosity = 1
	###### Material default inputs ########################################
        self.abinit_params = {}
        self.transfer_file = []
#        self.default_values()
#        self.set_values(type_input)
	##############################################################################
        self.run_serial = True
        if (self.QE.pseudo_auto == True):
            self.get_pseudo(type_input)

    def abi(self, input_abi = {}, name = 'abi'):
        """
        This is the main inout class for Abinit input which writes the input file

        The input_abi is a dictionary that can take all Abinit keywords

        Since in Abinit, input position is important, care must be taken while feeding this 
        input_abi dictionary 
        """
        self.set_work()
        self.set_abi(input_abi)
        self.writer = write_Abinit_files(self.abinit_params)
        self.writer.write_abi(name)
        self.set_home()


    def get_pseudo(self, type_input):
        """
        Gets the pseudos for abinit
        """
        print('Downloading pseudo for Abinit')
        self.lattice = lattice({})
        self.lattice.atomic_species = self.QE.pw_atomic_species
        self.lattice.pseudo_typ = 'PBE-FR-PDv0.4'
        self.lattice.pseudo_orbitals = ['','_r','-sp_r','-d_r','-s_r','-sp','-d','-s']
        self.lattice.pseudo_end = 'psp8'
        if ('pseudo_type' in type_input.keys()):
            print('setting pseudo type to:', type_input['pseudo_type'])
            self.lattice.pseudo_typ = type_input['pseudo_type']
        if ('pseudo_orbitals' in type_input.keys()):
            self.lattice.pseudo_orbitals = type_input['pseudo_orbitals']
        
        self.lattice.atomic_species = self.QE.pw_atomic_species['atomic_species']
        pseudo, pseudo_dir = self.lattice.get_pseudo()
        print(pseudo,pseudo_dir)
        self.QE.pw_control['pseudo_dir']='\''+pseudo_dir+'\''
        self.QE.pw_atomic_species['pseudo'] = pseudo
        self.pseudo = self.QE.pw_atomic_species['pseudo'] 

    def prepare(self, procs = 1, type_run = 'abinit', name = None, 
                infile = None, transfer_file = []):
        """ 
        This function prepares Abinit files 
        """

        if(len(transfer_file) != 0):
            for file in transfer_file:
                self.transfer_file.append(file)

        if(infile == None):
            infile = f'{type_run}.in'

        if(name == None):
            name = type_run

        self.prep=py_prepare(self.prefix,self.pseudo,self.transfer_file)
       # self.set_folds(name,type_run,self.prep)
        self.set_work()
       # self._save_json('epwpy_save',self.state)#self.pw_system) 
        self.set_home()

        if(type_run=='abinit'):
            self.set_work()
            self.prep.prepare_abinit(name, infile)
            self.set_home()

    def run(self,procs, type_run = 'abinit', infile = None , name = None, 
                parallelization = None, flow_parallelization=[], flavor = 'cplx'):
        """ 
        Run utility of EPWpy
        """
        self.run_Abi=py_run(procs,self.env,self.code)
        self.run_Abi.serial = self.run_serial
        self.procs = procs
        self.run_Abi.verbosity = self.verbosity
        self.run_Abi.proc_set = None
        #self.flow_parallelization = flow_parallelization
        if (parallelization != None):
            if (self.verbosity > 1):
                print('parallelization chosen: ', parallelization)
            self.run_Abi.proc_set = parallelization
        
        if(type_run=='abinit'):
            self.set_work()
            self.run_Abi.run_abinit(folder='abinit',name=infile)
            self.set_home()



 

    
def QE2Abi(QE_class):
    pass
