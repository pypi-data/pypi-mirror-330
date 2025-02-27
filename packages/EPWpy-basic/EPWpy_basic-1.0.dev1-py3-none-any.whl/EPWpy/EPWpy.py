#
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
from EPWpy.Logo import plot_logo
from EPWpy.default.code_loc import *
from EPWpy.EPWpy_run import *
from EPWpy.EPWpy_prepare import *
from EPWpy.EPWpy_analysis import *
from EPWpy.BGW.EPWpy_BGW import *
from EPWpy.QE.EPWpy_QE import *
from EPWpy.default.set_default import *
from EPWpy.structure.lattice import *
from EPWpy.error_handling.error_handler import *
from EPWpy.flow.transport import flow_manager
from EPWpy.flow.transport import *

import os
import EPWpy.utilities

class EPWpy(set_default_vals,flow_manager, py_BGW, py_QE,  py_analysis, job_status, lattice):#, flow_manager):#(py_prepare,py_run,py_analysis):
    """ 
    EPWpy provides a python interface for codes including QE, BGW and EPW 
    ! 

    ** EPWpy is a collaboration between four groups\n
    (1) The University of Texas at Austin (Prof. Feliciano Giustino's group)\n
    (2) Binghampton University (Prof. Roxana Margine's group)\n
    (3) University of Michigan (Prof. Emmanouil Kioupakis)\n
    (4) University Catholique de Louvain (Prof. Samuel Ponce)\n

    **\n
    ** All outputs are stored in dictionary format which can be obtaiend \n
    by calling respective methods of pw/ph/epw **\n
    **Example**\n
    To extract atomic species -> self.pw_atomic_species['atomic_species']\n
    !\n
    **List of dictionaries""\n
    !\n
    ..pw_system  :: system inputs and outputs\n
    ..pw_control :: control inputs and outputs\n
    ..pw_electrons :: electrons inputs and outputs\n
    ..pw_ions :: ions inputs and outputs (only enabled when iondynamics=True)\n
    ..pw_cell :: cell inputs and outputs (only enabled when celldynamics = True)\n
    ..pw_atomic_positions :: atomic positions, atoms\n
    ..pw_atomic_species :: atomic species, pseudos, mass\n
    ..pw_cell_parameters :: lattice vectors\n
    ..pw_bands :: bands.x related inputs\n
    ..ph_params :: PH code inputs    \n
    ..epw_params :: epw inputs\n
    ..wannier_params :: wannier code inputs\n
    ..pw2wann_params :: pw2wannier code inputs\n
    ..BGW_init :: initial BGW calculation inputs\n
    ..BGW_epsilon :: epsilon related inputs\n
    ..BGW_sigma :: sigma related inputs \n
    ..BGW_kernel :: kernel related inputs\n
    ..BGW_absorption :: absorption related inputs\n
    ..BGW_sig2wan :: sigma to wannier inputs\n
    ..BGW_pw2bgw :: pw to BerkeleyGW inputs \n
    ..zg_params :: ZG related inputs\n
    ..q2r_params :: q2r related inputs\n
    ..eps_inputpp :: epsilon.x related iputs\n
    ..eps_energy_grid :: epsilon.x energy_grid related inputs\n
    **\n
    **Inherited Classes **\n
    !
    ..py_BGW :: Class handling BerkeleyGW interface\n
    ..py_QE  :: class handling QE interface\n
    ..py_analysis :: comprises of properties that can be extracted\n
    ..job_status :: status of various jobs\n
    ..lattice :: automatic reading of input structure and pseudo potential download\n
    ..set_default_vals :: initializes the EPWpy class\n
    **\n
    ** Composed Classes **\n
    !\n
    ..py_run :: Class handling running of various codes (PW, PH, EPW, BGW)\n
    ..py_prepare :: Class handling preparation of calculations\n
    **
    ** __init__ options **\n
    ..type_input -> type (dict) :: dictionary with QE input variables to initialize the EPWpy\n
    ..system -> type (str) :: folder name in which calculation will take place\n
    ..env -> type (str) :: Environment for run utility e.g., mpirun, ibrun etc\n
    **
    """    
    def __init__(self,type_input = None,system='si',code=None,env='mpirun'):
        """ 
        The EPWpy is a utility that wraps EPW 
        """
        self.transfer_file=[]
        self.dont_do = []
        self.epwpy_logo()
        self.system=system
        self.code=code
        self.code = code
        if (self.code == None):
            if (code_set == None):
                print('No code chosen')
            else:
                self.code = code_set
        self.home=os.getcwd()
        self.env=env
        
        os.system('mkdir -p '+self.system)

        self.default_values()
        self.set_values(type_input)

        self.Run = py_run(1,self.env,self.code)
        self.Prepare = py_prepare(self.prefix,self.pseudo, files=[])      
        self.verbosity = 1
        self.state = {'epwpy_params':None}
        self.run_serial = True

    def epwpy_logo(self):
        """
        Print EPWpy logo
        """
        plot_logo()
       
    def prepare(self, procs = 1, type_run = 'scf', name = None, 
                infile = None, transfer_file = []):
        """ 
        This function prepares various runs for EPWpy 
        """

        if(len(transfer_file) != 0):
            for file in transfer_file:
                self.transfer_file.append(file)

        if(infile == None):
            infile = f'{type_run}.in'

        if(name == None):
            name = type_run

        self.prep=py_prepare(self.prefix,self.pseudo,self.transfer_file)
        self.set_folds(name,type_run,self.prep)
        self.set_work()
        self._save_json('epwpy_save',self.state)#self.pw_system) 
        self.set_home()

        if(type_run=='scf'):
            self.set_work()
            self.prep.prepare_scf(name, infile)
            self.set_home()

        elif(type_run=='nscf'):
            self.set_work()
            self.prep.prepare_nscf(name, infile)
            self.set_home()	

        elif(type_run=='bs'):
            self.set_work()
            self.prep.prepare_bs(name, infile)
            self.set_home()	

        elif(type_run=='ph'):
            self.set_work()
            self.prep.prepare_ph(name, infile)
            self.set_home()

        elif(type_run=='epw1'):
            self.set_work()
            
            if (name == 'epw1'):
                name = 'epw'
                self.epw_fold = name
            self.prep.prepare_epw1(name, infile)
            self.set_home()

        elif(type_run=='epw2'):
            self.set_work()
            if (name == 'epw2'):
                name = 'epw'    
            self.prep.prepare_epw2(name, infile)
            self.set_home()

        elif(type_run=='epw3'):
            self.set_work()
            if (name == 'epw3'):
                name = 'epw'    
            self.prep.prepare_epw3(name, infile)
            self.set_home()

        elif(type_run=='q2r'):
            self.set_work()            
            if (name == 'q2r'):
                name = self.ph_fold
            self.prep.prepare_q2r(name, infile)
            self.set_home()

        elif(type_run=='zg'):
            self.set_work()
            self.prep.prepare_zg(name, infile)
            self.set_home()

        elif(type_run=='wannier'):
            self.set_work()
            self.prep.prepare_wannier(name, infile)
            self.set_home()

        elif(type_run=='eps'):
            self.set_work()
            self.prep.prepare_eps()
            self.set_home()

        elif(type_run=='bands'):
            self.set_work()
            self.prep.prepare_bands()
            self.set_home()
            
        elif(type_run=='nscf2supercond'):
            self.set_work()
            self.prep.prepare_nscf2supercond()
            self.set_home()
            
        elif(type_run=='matdyn'):
            self.set_work()
            self.prep.prepare_matdyn(name = self.ph_fold)
            self.set_home()
            
        elif(type_run=='phdos'):
            self.set_work()
            self.prep.prepare_phdos(name = self.ph_fold)
            self.set_home()
            
        elif(type_run=='nscf_tetra'):
            self.set_work()
            self.prep.prepare_nscf_tetra()
            self.set_home()
            
        elif(type_run=='dos'):
            self.set_work()
            self.prep.prepare_dos()
            self.set_home()
            
        elif(type_run=='pdos'):
            self.set_work()
            self.prep.prepare_pdos()
            self.set_home()
            
        elif(type_run=='fbw'):
            self.set_work()
            self.prep.prepare_fbw()
            self.set_home()
            
        elif(type_run=='fbw_mu'):
            self.set_work()
            self.prep.prepare_fbw_mu()
            self.set_home()
            
        elif(type_run=='nesting'):
            self.set_work()
            self.prep.prepare_nesting()
            self.set_home()
            
        elif(type_run=='phselfen'):
            self.set_work()
            self.prep.prepare_phselfen()
            self.set_home()
            
        elif(type_run=='epw_outerbands'):
            self.set_work()
            self.prep.prepare_outerbands()
            self.set_home()

    def run(self,procs, type_run = 'scf', infile = None , name = None, 
                parallelization = None, flow_parallelization=[], flavor = 'cplx'):
        """ 
        Run utility of EPWpy
        """
        self.run_QE=py_run(procs,self.env,self.code)
        self.run_QE.serial = self.run_serial
        self.procs = procs
        self.run_QE.verbosity = self.verbosity
        self.run_QE.proc_set = None
        #self.flow_parallelization = flow_parallelization
        if (parallelization != None):
            if (self.verbosity > 1):
                print('parallelization chosen: ', parallelization)
            self.run_QE.proc_set = parallelization
        

        if (infile == None):
            infile = type_run 

        if(type_run=='scf'):
            self.set_work()
            self.run_QE.run_scf(name = infile, folder = self.scf_fold)
            self.set_home()

        elif(type_run=='nscf'):
            self.set_work()
            self.run_QE.run_nscf(name = infile, folder = self.nscf_fold)
            self.set_home()	

        elif(type_run=='bs'):
            self.set_work()
            self.run_QE.run_bs(name = infile, folder = self.bs_fold)
            self.set_home()	

        elif(type_run=='ph'):
            self.set_work()
            self.run_QE.run_ph(name = infile, folder = self.ph_fold)
            self.set_home()

        elif(type_run=='epw1'):
            self.set_work()
            self.run_QE.run_epw1(name = infile, folder = self.epw_fold)
            self.set_home()

        elif(type_run=='epw2'):
            self.set_work()
            self.run_QE.run_epw2(name = infile, folder = self.epw_fold)
            self.set_home()

        elif(type_run=='epw3'):
            self.set_work()
            self.run_QE.run_epw3(name = infile, folder = self.epw_fold)
            self.set_home()

        elif(type_run=='q2r'):
            self.set_work()
            self.run_QE.run_q2r(name = infile)
            self.set_home()

        elif(type_run=='zg'):
            self.set_work()
            self.run_QE.run_zg(name = infile)
            self.set_home()

        elif(type_run=='eps'):
            self.set_work()
            self.run_QE.run_eps(name = infile)
            self.set_home()

        elif(type_run=='nscf_tetra'):
            self.set_work()
            self.run_QE.run_nscf_tetra()
            self.set_home()	

        elif(type_run=='bands'):
            self.set_work()
            self.run_QE.run_bands(name = infile)
            self.set_home()

        elif(type_run=='nscf2supercond'):
            self.set_work()
            self.run_QE.run_nscf2supercond(name = infile)
            self.set_home()

        elif(type_run=='matdyn'):
            self.set_work()
            self.run_QE.run_matdyn(name = infile)
            self.set_home()

        elif(type_run=='phdos'):
            self.set_work()
            self.run_QE.run_phdos(name = infile)
            self.set_home()

        elif(type_run=='dos'):
            self.set_work()
            self.run_QE.run_dos(name = infile)
            self.set_home()

        elif(type_run=='pdos'):
            self.set_work()
            self.run_QE.run_pdos(name = infile)
            self.set_home()

        elif(type_run=='fbw'):
            self.set_work()
            self.run_QE.run_fbw(name = infile)
            self.set_home()

        elif(type_run=='fbw_mu'):
            self.set_work()
            self.run_QE.run_fbw_mu(name = infile)
            self.set_home()

        elif(type_run=='nesting'):
            self.set_work()
            self.run_QE.run_nesting(name = infile)
            self.set_home()

        elif(type_run=='phselfen'):
            self.set_work()
            self.run_QE.run_phselfen(name = infile)
            self.set_home()

        elif(type_run=='epw_outerbands'):
            self.set_work()
            self.run_QE.run_epw_outerbands(name = infile)
            self.set_home()
            
        elif(type_run=='wannier'):
            self.set_work()
            self.run_QE.run_wannier(name=self.prefix)
            self.set_home()

        elif(type_run=='GW'):
            self.set_work()
            self.run_QE.run_nscf(folder='./GW/wfn',name='wfn')
            self.run_QE.run_pw2bgw(folder='./',name=self.prefix)
            self.set_home()
            self.set_work()
            self.run_QE.run_nscf(folder='./GW/wfnq',name='wfnq')
            self.run_QE.run_pw2bgw(folder='./',name=self.prefix)
            self.set_home()
            self.set_work()
            self.run_QE.run_nscf(folder='./GW/wfnfi',name='wfnfi')
            self.run_QE.run_pw2bgw(folder='./',name=self.prefix)
            self.set_home()

        elif(type_run=='epsilon'):
            self.set_work()
            self.run_QE.run_epsilon(folder='./GW/epsilon',name='epsilon',flavor = flavor)
            self.set_home()

        elif(type_run=='sigma'):
            self.set_work()
            self.run_QE.run_sigma(folder='./GW/sigma',name='sigma',flavor = flavor)
            self.set_home()

        elif(type_run=='sigma2wan'):
            self.set_work()
            self.run_QE.run_sig2wan(folder='./GW/sigma',name='sig2wan')
            self.set_home()

        elif(type_run=='kernel'):
            self.set_work()
            self.run_QE.run_kernel(folder='./GW/kernel',name='kernel',flavor = flavor)
            self.set_home()

        elif(type_run=='absorption'):
            self.set_work()
            self.run_QE.run_absorption(folder='./GW/absorption',name='absorption',flavor = flavor)
            self.set_home()

        elif(type_run == 'transport'):
            #self.fm = flow_manager(self)
            self.flow_parallelization = flow_parallelization
            if (len(self.flow_parallelization) == 0):
                self.flow_parallelization=[None, None, None]
            self.set_work()            
            #self.fm.transport_flow()
            self.transport_flow()
            self.set_home()

