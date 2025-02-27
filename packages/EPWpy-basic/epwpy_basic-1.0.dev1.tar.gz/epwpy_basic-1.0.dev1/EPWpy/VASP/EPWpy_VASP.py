# W.I.P
import numpy as np
import argparse
import os
from EPWpy.default.default import *
from EPWpy.VASP.write_vasp import *
from EPWpy.VASP.set_vasp import *
from EPWpy.structure.lattice import *
from EPWpy.utilities.set_files import *
from EPWpy.utilities.k_gen import *
from EPWpy.EPWpy_prepare import *
from EPWpy.EPWpy_run import *
from EPWpy.structure.lattice import *

class py_VASP(set_dir, set_VASP):#(py_prepare,py_run,py_analysis):
    """
    This code builds an interface to VASP
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
        self.vasp_params = {}
        self.transfer_file = []
        self.set_vasp_values(type_input)
	##############################################################################
        self.run_serial = True
        self.verbosity = 1

    def set_vasp_values(self,type_input):
        """
        Setting vasp dictionaries
        """
        self.vasp_params = vasp_params
        self.vasp_kpoint_params = vasp_kpoint_params
        self.set_initial(type_input)

    def VASP_SCF(self, input_vasp = {}, name = 'abi'):
        """
        This is the main inout class for VASP input which writes the input file
        The input_vasp is a dictionary that can take all VASP keywords
        """
        self.set_work()
        self.set_vasp_incar(input_vasp)
        self.set_vasp_kpoints(input_vasp)
        self.writer = write_vasp_files(self.vasp_params, self.vasp_kpoint_params)
        self.writer.write_INCAR(name='INCAR')
        self.writer.write_KPOINTS(name='KPOINTS')
        self.set_home()

    def VASP_NSCF(self, input_vasp = {}, name = 'abi'):
        """
        This is the main inout class for VASP input which writes the input file
        The input_vasp is a dictionary that can take all VASP keywords
        """
        self.set_work()
        self.set_vasp_incar(input_vasp)
        self.set_vasp_kpoints(input_vasp)
        if (self.verbosity > 2):
            print('Displaying kpoints', self.vasp_kpoint_params)
        self.writer = write_vasp_files(self.vasp_params, self.vasp_kpoint_params)
        self.writer.write_INCAR(name='INCAR')
        self.writer.write_KPOINTS(name='KPOINTS')
        self.set_home()


    def prepare(self, procs = 1, type_run = 'vasp', name = None, 
                infile = None, transfer_file = []):
        """ 
        This function prepares VASP files 
        """

        if(len(transfer_file) != 0):
            for file in transfer_file:
                self.transfer_file.append(file)

        if(infile == None):
            infile = f'INCAR'

        if(name == None):
            name = type_run

        self.name_vasp = name
        self.prep=py_prepare(self.prefix,self.pseudo,self.transfer_file)
        self.prep.pseudo = self.pseudo
        if (self.verbosity > 1):
            print('Pseudopotential location for VASP: ',self.prep.pseudo)

        if(type_run=='vasp'):
            self.set_work()
            self.vasp_file = name
            self.prep.prepare_vasp(name, infile, structure = self.structure)
            self.run_fold = f'{self.name_vasp}'
            self.set_home()

        if(type_run=='vasp_nscf'):
            self.set_work()
            self.prep.prepare_vasp_nscf(name, infile, name_vasp = self.vasp_file, structure = self.structure)
            self.run_fold = f'{self.vasp_file}/{self.name_vasp}'
            self.set_home()


    def run(self,procs, type_run = 'std', infile = '' , name = None, 
            parallelization = None, flow_parallelization=[], flavor = 'std'):
        """ 
        Run utility of EPWpy for VASP

        The type_run decides if we perform standard or ncl calculations
    
        To do: Flow calculations when interface becomes available
        Flavor to control folders in future     
        """

        self.run_vasp=py_run(procs,self.env,self.code)
        self.run_vasp.serial = self.run_serial
        self.procs = procs
        self.run_vasp.verbosity = self.verbosity
        self.run_vasp.proc_set = None
        #self.flow_parallelization = flow_parallelization
        if (parallelization != None):
            if (self.verbosity > 1):
                print('parallelization chosen: ', parallelization)
            self.run_vasp.proc_set = parallelization
                 
        if (name == None):
            try:
                folder = self.run_fold
            except AttributeError:
                folder = 'vasp'
        self.set_work()
        self.run_vasp.run_vasp(folder=folder,name=infile, flavor=type_run)
        self.set_home()



