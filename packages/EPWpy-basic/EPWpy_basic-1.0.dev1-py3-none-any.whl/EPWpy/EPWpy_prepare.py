from __future__ import annotations

__author__= "Sabyasachi Tiwari, Shashi Mishra"
__copyright__= "Copyright 2024, EPWpy project"
__version__= "1.0"
__maintainer__= "Sabyasachi Tiwari"
__maintainer_email__= "sabyasachi.tiwari@austin.utexas.edu"
__status__= "Production"
__date__= "May 03, 2024"

import numpy as np
import os
import subprocess as sp
from EPWpy.utilities.set_files import*
from EPWpy.utilities.epw_pp import *
from EPWpy.utilities.printing import *

class py_prepare(set_dir):
    """
    py_prepare class prepares the input/output files for EPW calculations
    Mostly used for transferring files for EPW calculations
    """
    def __init__(self,prefix,pseudo, files=[]):
        """
        Preparation init 
        """
        self.prefix=prefix
        self.pseudo=pseudo  
        self.files = files
        self.folder_name = 'dummy'

    def decorated_save(func):
        """
        Saves state
        """
        def inner(self,**kwargs):
            fold = kwargs['name']
            self.save = Save_state(' ',' ')
            dict1={f'{util}':fold}
            self._save_json('state',dict1)#self.pw_system) 
            func(self,**kwargs)
        return inner

#    @decorated_save
    def prepare_scf(self, name = 'scf', filename = 'scf.in'):
        """ 
        Transfer file of scf 
        """
        self.makedir(name)
        self.run(f'{filename}','./scf')

    def prepare_nscf(self, name = 'nscf', filename = 'nscf.in'):
        """ 
        Transfer nscf files 
        """
        self.prepare_post_scf(name, filename)

    def prepare_bs(self, name = 'bs', filename = 'bs.in'):

        self.prepare_post_scf(name, filename)

    def prepare_ph(self, name = 'ph', filename = 'ph.in'):
        """ 
        Prepares phonon calculation 
        """
        self.prepare_post_scf(name, filename)
 
    def prepare_q2r(self, name='ph', filename = 'q2r.in'):
        """ 
        Prepares a q2r calculation 
        """
        self.run(f'{filename}',f'./{name}')

    def prepare_bands(self, name = 'bs', filename = 'bands.in'):
        """ 
        Prepares a bamds calculation 
        """
        self.run(f'{filename}',f'./{name}')

    def prepare_matdyn(self, name = 'ph', filename = 'matdyn.in'):
        """ 
        Prepares a matdyn calculation 
        """
        self.run(f'{filename}',f'./{name}') 
        
    def prepare_nscf2supercond(self, name = 'nscf', filename = 'nscf2supercond.in'):
        """ 
        Prepares a phdos calculation 
        """
        self.run(f'{filename}',f'./{name}')
       
    def prepare_phdos(self, name = 'ph', filename = 'phdos.in'):
        """ 
        Prepares a phdos calculation 
        """
        self.run(f'{filename}',f'./{name}')
        
    def prepare_nscf_tetra(self, name = 'nscf_tetra', filename = 'nscf.in'):
        """
        Prepares a nscf tetragonal calculation
        """ 
        self.prepare_post_scf(name, filename)

    def prepare_dos(self, name = 'nscf_tetra', filename = 'dos.in'):
        """ 
        Prepares a dos calculation 
        """
        self.run(f'{filename}',f'./{name}')
            
    def prepare_pdos(self, name = 'nscf_tetra', filename = 'pdos.in'):
        """ 
        Prepares a pdos calculation 
        """
        self.run(f'{filename}',f'./{name}')

          
    def prepare_fbw(self, name = 'fbw', filename = 'fbw.in'):
        """
        Prepares FBW calculation
        """
        self.prepare_post_epw(name,filename)
       
    def prepare_outerbands(self, name = 'epw_outerbands', filename = 'epw_outerbands.in'):
        """
        Prepares outerbands calculation
        """
        self.prepare_post_epw(name,filename)
       
    def prepare_fbw_mu(self, name = 'fbw_mu', filename = 'fbw_mu.in'):
        """
        Prepares fbw mu calculation
        """
        self.prepare_post_epw(name,filename)
       
    def prepare_nesting(self, name = 'nesting', filename = 'nesting.in'):
        """
        Prepares nesting calculation
        """
        self.prepare_post_epw2(name,filename)
       
    def prepare_phselfen(self, name = 'phselfen', filename = 'phselfen.in'):
        """
        Prepares phselfen calculation
        """
        self.prepare_post_epw2(name,filename)

    def prepare_zg(self, name = 'zg', filename = 'zg.in'):
        """ 
        Prepares ZG calculation 
        """
        self.makedir(name)

        for file in self.files:
            self.run(file,f' ./{name}') 
        self.run(f'{filename}',f'./{name}')
        self.run(f'./{self.scf_fold}/'+str(self.prefix)+'.save','./zg')
        self.run(f'./{self.ph_fold}/_ph0',f'./{name}')
        self.run(f'./{self.ph_fold}/*dyn*',f'./{name}')
        self.run(f'./{self.ph_fold}/*.fc',f'./{name}')
        self.run(f'./{self.scf_fold}/scf.in',f'./{name}')

    def prepare_eps(self, name = 'eps', filename = 'eps.in'):
        """ 
        Prepares epsilon.x calculation for QE 
        """
        self.makedir(name)
        self.run(f'{filename}',f'./{name}')
        self.run(f'./{self.nscf_fold}/'+str(self.prefix)+'.save',f'./{name}')
        self.run(f'./{self.nscf_fold}/*wfc*',f'./{name}')
 
    def prepare_epw1(self, name = 'epw', filename='epw1.in'):
        """ 
        Prepares epw1 coarse grid calculation 
        """
        self.makedir(name)
        self.run(f'./{self.nscf_fold}/'+str(self.prefix)+'.save',f'./{name}')
        self.run(f'{filename}',f'./{name}')
        self.run(f'./{self.ph_fold}/_ph0',f' ./{name}')
        self.run(f'./{self.ph_fold}/'+str(self.prefix)+'.dyn*',f'./{name}')
        self.run_transfer(name)
        self.changedir(name)
        self.pp()
        self.changedir('../')

    def prepare_epw2(self, name = 'epw', filename = 'epw2.in'): 
        """ 
        Prepares a second interpolated epw claculation 
        """
        self.run_transfer(name)
        self.run(f'{filename}',f'./{name}')

    def prepare_epw3(self, name = 'epw', filename = 'epw3.in'):
        """ 
        Prepares a third epw calculation 
        """
        self.run_transfer(name) 
        self.run(f'{filename}',f'./{name}')

    def prepare_wannier(self, name = 'wannier', filename = ''):
        """ 
        Prepares Wannier files 
        """
        self.makedir(name)
        self.run_transfer(name)
        self.run(f'./{self.nscf_fold}/'+str(self.prefix)+'.save',f'./{name}')
        self.run(str(self.prefix)+'.win',f'./{name}')
        self.run(str(self.prefix)+'.pw2wan',f'./{name}')


    def prepare_dummy(self):
        """ Prepares a dummy run on any type """
        self.makedir(self.folder_name)
        self.run_transfer(self.outfile)
        self.run(self.infile,self.outfile)

    def prepare_post_scf(self, name, filename):

        self.makedir(name)
        self.run_transfer(name)
        self.run(f'{filename}',f'./{name}')
        self.run(f'./{self.scf_fold}/'+str(self.prefix)+'.save',f'./{name}')

    def prepare_post_epw(self, name, filename):
        """
        Prepares a post epw calculation outside epw folder
        """
        self.makedir(f'{name}')
        self.link(f'../{self.epw_fold}/{self.prefix}.ephmat',f'{name}')
        self.run(f'./{self.epw_fold}/*.fmt', '{name}')
        self.run(f'./{self.epw_fold}/{self.prefix}.a2f', f'{name}')
        self.run(f'./{self.epw_fold}/{self.prefix}.dos', f'{name}')
        self.run(f'{filename}', f'{name}')        

    def prepare_post_epw2(self, name, filename):
        """
        Prepares a post epw calculation outside epw folder
        """
        self.makedir(f'{name}')
        self.run(f'../{self.epw_fold}/{self.prefix}.epmatwp',f'{name}')
        self.run(f'./{self.epw_fold}/*.fmt', '{name}')
        self.run(f'./{self.epw_fold}/{self.prefix}.ukk', f'{name}')
        self.run(f'./{self.ph_fold}/{self.prefix}._band.kpt', f'{name}')
        self.run(f'{filename}', f'{name}')        

    def prepare_abinit(self, name='abinit', filename = 'abi.abi'):
        """ 
        Prepares an Abinit calculation 
        """
        self.makedir(f'{name}')
        self.run(f'{filename}',f'./{name}')

    def prepare_vasp(self, name='vasp', filename = 'INCAR', structure = 'POSCAR'):
        """ 
        Prepares an Abinit calculation 
        """
        self.makedir(f'{name}')
        self.run(f'{filename}',f'./{name}')
        self.run(f'KPOINTS',f'./{name}')
        self.run(f'{self.pseudo}',f'./{name}/POTCAR')
        self.run(f'{structure}',f'./{name}/POSCAR')

    def prepare_vasp_nscf(self, name='bands', filename = 'INCAR',
                    name_vasp = 'vasp', structure ='POSCAR'):
        """ 
        Prepares an Abinit calculation 
        """
        fold = f'{name_vasp}/{name}'
        self.makedir(f'{fold}')
        self.run(f'{filename}',f'./{fold}')
        self.run(f'KPOINTS',f'./{fold}')
        self.run(f'{name_vasp}/WAVECAR',f'./{fold}')
        self.run(f'{name_vasp}/CHGCAR',f'./{fold}')
        self.run(f'{name_vasp}/POTCAR',f'./{fold}')
        self.run(f'{structure}',f'./{fold}/POSCAR')
        self.run_transfer(f'{fold}')
 
    def run_transfer(self, name):
        """ Runner for file transfer """
        for file in self.files:
            if(file !=None):
                self.run(file,f' ./{name}')
        
    def link(self,infile,outfile):

        sp.Popen('ln -sf '+str(infile)+'  '+str(outfile), shell=True).wait()


    def run(self,infile,outfile):

        sp.Popen('cp -r '+str(infile)+'  '+str(outfile), shell=True).wait()

    def pp(self):
        try:
            prefix=self.prefix.replace('\'','')
            
            run_pp(prefix)
        except FileNotFoundError:
            prefix='\''+str(prefix)+'\''
            run_pp(prefix)


