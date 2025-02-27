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
import os
import subprocess as sp
from EPWpy.utilities.printing import *

class py_run:
    """ 
    ** This is the run class of EPWpy which provides acces to running QE and BGW
    **
    ** This class can be called from hgiher level and can be run independently with
    EPWpy object
    ** attributes **
    ..env (str) :: type of environment mpirun, ibrun, srun etc.
    ..procs (int) :: number of processors
    ..code (str) :: location of the code from where one wants to run
    ** Returns  Run objects **
    """

    def __init__(self,procs,env,code):
        """
        Intitilize
        """
        self.procs=procs
        self.env=env
        self.code=code
        self.serial=True

    @decorated_progress
    def run_scf(self,folder='./scf',name='scf'):
        """ Run scf calculation
        """
        if (self.proc_set == None):
            nt,nk=self.set_processors(self.procs)
            nt=int(nt)
            nk=int(nk)
            self.util='pw.x -nk '+str(nk)+' -nt '+str(nt)+' -in '
        else:
            self.util='pw.x '+str(self.proc_set)+' -in '
 
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.runner()

    @decorated_progress
    def run_nscf(self,folder='./nscf',name='nscf'):
        """ Run nscf calculation
        """
        if (self.proc_set == None):
            nt,nk=self.set_processors(self.procs)
            nt=int(nt)
            nk=int(nk)
            self.util='pw.x -nk '+str(nk)+' -nt '+str(nt)+' -in '
        else:
            self.util='pw.x '+str(self.proc_set)+' -in '
        namein = name+'.in'
        nameout = name+'.out'
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.runner()
    
    @decorated_progress
    def run_bs(self,folder='./bs',name='bs'):
        """ Run bandstructure calculation
        """
        if (self.proc_set == None):
            nt,nk=self.set_processors(self.procs)
            nt=int(nt)
            nk=int(nk)
            self.util='pw.x -nk '+str(nk)+' -nt '+str(nt)+' -in '
        else:
            self.util='pw.x '+str(self.proc_set)+' -in '
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.runner()
    
    @decorated_progress
    def run_ph(self,folder='./ph',name='ph'):
        """ 
        Runner for phonon 
        """
        if (self.proc_set == None):
            nt,nk=self.set_processors(self.procs)
            nt=int(nt)
            nk=int(nk)
            self.util='ph.x -pd .true. -nk '+str(nk)+' -nt '+str(nt)+' -in '
        else:
            self.util='ph.x '+str(self.proc_set)+' -in '
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.runner()

    @decorated_progress
    def run_epw1(self,folder='./epw',name='epw1'):
        """ 
        Runner for epw1 
        """
        self.dir=folder 
        nk=int(self.procs)
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.util='epw.x -nk '+str(nk)+' -in '
        self.runner()

    @decorated_progress
    def run_abinit(self,folder='./abinit',name='abi'):
        """ 
        Runner for abinit 
        """
        self.dir=folder 
        nk=int(self.procs)
        self.filein=name+'.abi'
        self.fileout=name+'.log'
        self.util='abinit '
        self.runner()

    @decorated_progress
    def run_vasp(self,folder='./vasp',name=' ',flavor='std'):
        """ 
        Runner for abinit 
        """
        self.dir=folder 
        nk=int(self.procs)
        self.filein=name#+'.abi'
        self.fileout='output'#+'.log'
        self.util=f'vasp_{flavor}'
        self.runner()
    
    @decorated_progress
    def run_epw2(self,folder='./epw',name='epw2'):
        """ 
        Runner for epw2 
        """
        self.dir=folder 
        nk=int(self.procs)

        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.util='epw.x -nk '+str(nk)+' -in '
        self.runner()

    @decorated_progress
    def run_epw3(self,folder='./epw',name='epw3'):
        """ 
        Runner for epw3 
        """
        self.dir=folder 
        nk=int(self.procs)
 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.util='epw.x -nk '+str(nk)+' -in '
        self.runner()

    @decorated_progress
    def run_zg(self,folder='./zg',name = 'zg'):
        """ 
        Runner for ZG 
        """
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.util='ZG.x -in '
        self.runner()

    @decorated_progress
    def run_q2r(self,folder='./ph', name='q2r'):
        """ 
        Runner for q2r 
        """
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.util='q2r.x -in '
        self.runner()

    @decorated_progress
    def run_eps(self,folder='./eps',name='eps'):
        """ 
        Runner for epsilon 
        """
        self.dir=folder 
        self.filein=name+'.in'
        self.fileout=name+'.out'
        self.util='epsilon_Gaus.x -in'
        self.runner()

    @decorated_progress
    def run_nscf_tetra(self,folder='./nscf_tetra',name='nscf'):
        namein = name+'.in'
        nameout = name+'.out'
        nt, nk = self.set_processors(self.procs)
        nt = int(nt)
        nk = int(nk)
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'pw.x -nk '+str(nk)+' -nt '+str(nt)+' -in '
 
        #print("running nscf with "+str(nk)+' nk and '+str(nt)+" tasks")
        p1 = self.runner()
        if(self.serial):
            p1.wait()
            
    @decorated_progress
    def run_bands(self,folder='./bs',name='bands'):
        """ Runner for bands """
        self.dir = folder 
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'bands.x -in'
        #print("running post-proc bands")
        self.runner()
        
    @decorated_progress
    def run_nscf2supercond(self,folder='./nscf',name='nscf2supercond'):
        """ Runner for nscf2supercond """
        self.dir = folder 
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = '../EPW/bin/nscf2supercond.x -in'
        #print("running nscf2supercond to extract eigen energies")
        self.runner()
        
    @decorated_progress
    def run_matdyn(self, folder='./ph', name='matdyn'):
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'matdyn.x -in'
        #print("running phonon bands calculation")
        p1 = self.runner()
        
    @decorated_progress
    def run_phdos(self, folder='./ph', name='phdos'):
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'matdyn.x -in'
        #print("running phonon dos calculation")
        p1 = self.runner()
        
    @decorated_progress
    def run_dos(self, type_run='nscf_tetra', folder='./nscf_tetra', name='dos'):
        if type_run == 'nscf':
            folder = './nscf'
        else:
            folder = './nscf_tetra'

        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'dos.x -in'
        #print("running electron DOS calculation")
        p1 = self.runner()
        
    @decorated_progress        
    def run_pdos(self,type_run='nscf_tetra',folder='./nscf_tetra',name='pdos'):
        if type_run=='nscf':
            folder = './nscf'
        else:
            folder = './nscf_tetra'

        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'projwfc.x -in'
        #print("running electron PDOS calculation")
        p1 = self.runner()
        
    @decorated_progress
    def run_fbw(self, folder='./fbw', name='fbw'):
        nk = int(self.procs)
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'epw.x -nk '+str(nk)+' -in '
        #print("running FBW calculation")
        p1 = self.runner()
        
    @decorated_progress       
    def run_fbw_mu(self, folder='./fbw_mu', name='fbw_mu'):
        nk = int(self.procs)
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'epw.x -nk '+str(nk)+' -in '
        #print("running FBW+mu calculation")
        p1 = self.runner()
        
    @decorated_progress   
    def run_epw_outerbands(self, folder='./epw_outerbands', name='epw_outerbands'):
        nk = int(self.procs)
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'epw.x -nk '+str(nk)+' -in '
        #print("running epw calculation with Coulomb correction")
        p1 = self.runner()
        
    @decorated_progress
    def run_nesting(self, folder='./nesting', name='nesting'):
        nk = int(self.procs)
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'epw.x -nk '+str(nk)+' -in '
        #print("running nesting function calculation")
        p1 = self.runner()
        
    @decorated_progress    
    def run_phselfen(self, folder='./phselfen', name='phselfen'):
        nk = int(self.procs)
        self.dir = folder
        self.filein = name+'.in'
        self.fileout = name+'.out'
        self.util = 'epw.x -nk '+str(nk)+' -in '
        p1 = self.runner()
            
    @decorated_progress
    def run_wannier(self,folder='./wannier',name='win'):
        """ 
        Runner for Wannier 
        """
        self.dir=folder 
        name=name.replace('\'','')

        self.filein=name+'.win'
        self.fileout=name+'.wout'
        self.util='wannier90.x -pp '
        serial=self.serial
        self.serial=True
        p1=self.runner()
        self.filein=name+'.pw2wan'
        self.fileout=name+'.pw2wan.out'
        self.util='pw2wannier90.x -pd .true. -in'
        self.runner()
        self.filein=name
        self.util='wannier90.x'
        self.runner()
        self.serial=serial
        self.runner()

    def run_pw2bgw(self,folder=' ',name=None):
        """ 
        Runner for pw2BGW 
        """
        self.dir = folder 
 
        if(name !=None):
            pw2bgw=name
        else:
            pw2bgw=self.prefix
        self.filein=pw2bgw+'.pw2bgw'
        self.fileout=pw2bgw+'.out'
        self.util='pw2bgw.x -pd .true. -in'
        self.runner()

    @decorated_progress 
    def run_epsilon(self,folder=' ',name=None, flavor='cplx'):

        self.dir = folder
        if(name !=None):
            eps_file=name
        else:
            eps_file='epsilon'

        self.filein=eps_file+'.inp'
        self.fileout=eps_file+'.out'
        self.util='epsilon.'+str(flavor)+'.x -in'
        self.runner()

    @decorated_progress
    def run_sigma(self,folder=' ',name=None,flavor='cplx'):
        self.dir = folder

        if(name !=None):
            eps_file=name
        else:
            eps_file='sigma'
        self.filein=eps_file+'.inp'
        self.fileout=eps_file+'.out'
        self.util='sigma.'+str(flavor)+'.x -in'
        self.runner()

    @decorated_progress
    def run_sig2wan(self,folder=' ',name=None):
        self.dir = folder

        if(name !=None):
            eps_file=name
        else:
            eps_file='sig2wan'
        self.filein=eps_file+'.inp'
        self.fileout=eps_file+'.out'
        self.util='sig2wan.x -in'
        self.runner()

    @decorated_progress
    def run_kernel(self,folder=' ',name=None,flavor='cplx'):
        self.dir = folder

        if(name !=None):
            eps_file=name
        else:
            eps_file='kernel'
        self.filein=eps_file+'.inp'
        self.fileout=eps_file+'.out'
        self.util='kernel.'+str(flavor)+'.x -in'
        self.runner()

    @decorated_progress
    def run_absorption(self,folder=' ',name=None,flavor='cplx'):
        self.dir = folder

        if(name !=None):
            eps_file=name
        else:
            eps_file='absorption'
        self.filein=eps_file+'.inp'
        self.fileout=eps_file+'.out'
        self.util='absorption.'+str(flavor)+'.x -in'
        self.runner()


#    @decorated_progress
    def runner(self):
        """ 
        Main runner for executing executables..
        
        Uses subprocess 
 
        """
        os.chdir(self.dir)
        cmd = None

        if self.env:
            if (self.env == 'mpirun'):
                cmd = f'{self.env} -np {self.procs} {self.code}/{self.util} {self.filein} > {self.fileout}'
            elif (self.env == 'srun'):
                cmd = f'{self.env} -n {self.procs} {self.code}/{self.util} {self.filein} > {self.fileout}'
            elif (self.env == 'ibrun'):
                cmd = f'{self.env} {self.code}/{self.util} {self.filein} > {self.fileout}'
            else:
                cmd = f'{self.env} {self.procs} {self.code}/{self.util} {self.filein} > {self.fileout}'
        else:
            cmd = f'{self.code}/{self.util} {self.filein} > {self.fileout}'

        if (self.verbosity > 1):
            print('running: ',cmd)

        if (self.verbosity > 2):
            cmd +=f'{cmd}| tail -f {self.fileout}' 
 
        p1=sp.Popen(cmd, shell=True)

        if (self.env == 'serial'):

            p1=sp.Popen('/'+self.code+'/'+self.util+' '+self.filein+' > '+self.fileout, shell=True)

        if(self.serial):
            p1.wait()
        return(p1)

    def set_processors(self,procs):
        if(np.sqrt(procs)%2==0):
            return(np.sqrt(procs),np.sqrt(procs))
        else:
            return(1,procs)                    
