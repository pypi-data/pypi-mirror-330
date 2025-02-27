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
import subprocess as sp
import os
from EPWpy.utilities.set_files import *
from EPWpy.default.default import *
from EPWpy.utilities.k_gen import *
from EPWpy.utilities.Band import *
from EPWpy.BGW.BGW_set_links import *
from EPWpy.BGW.write_BGW import write_BGW_files
from EPWpy.BGW.write_QE_BGW import *
from EPWpy.QE.PW_util import find_fermi

class py_BGW(set_dir, write_BGW_files, write_QE_BGW_files):
    """
    This is the class that interacts with BerkeleyGW
    **
    To do: create flow
    **
    """
    def __init__(self,structure):

         self.inp=structure
       
    def GW(self,GW={}):
        """ 
        Prepares GW calculations 
        """
        self.prepare_GW()
        self.BGW_init = BGW_init
        self.BGW_pw2bgw = BGW_pw2bgw
        self.BGW_sig2wan = BGW_sig2wan
        self.BGW_epsilon = BGW_epsilon
        self.BGW_sigma = BGW_sigma
        self.BGW_kernel = BGW_kernel
        self.BGW_absorption = BGW_absorption
        self.BGW_epsilon['number_bands'] = self.nbnd_co

        if(self.nbnd_co == None):
            print('Manually set the number of bands in epsilon')
            self.BGW_epsilon['number_bands'] = BGW_init['nbnd']
        self.pw_control['calculation'] ='\'bands\''
        self.prepare_link()

        for key in GW.keys():
            if(key in self.BGW_init.keys()):
                self.BGW_init[key] = GW[key]         
            
    def epsilon(self,epsilon={},type_calc=1):
        """
        prepare epsilon calculation
        """

        if (type_calc==1):
            print('Preparing ESPRESSO files, else use type_calc=2')
            self.prepare_wfn(kpoints = {'grid':self.BGW_init['grid_co']}) 
            self.prepare_wfnq(kpoints = {'grid':self.BGW_init['grid_co'],
                                        'shift':self.BGW_init['shift']}) 
            self.prepare_wfnfi(kpoints = {'grid':self.BGW_init['grid_fi']}) 
            self.prepare_wfnfiq(kpoints ={'grid':self.BGW_init['grid_fi'],
                                         'shift':self.BGW_init['shift']})
        self.set_work()
        print('shifted grid',self.shift, self.GW_k[0,:3])
        for i in range(len(self.GW_k[:,0])):
            for l in range(3):
                self.GW_k[i,l]="{:.8f}".format(self.GW_k[i,l])
                 
        self.GW_ks = self.GW_k
        self.GW_ks[0,:3] += self.shift 
        self.write_epsilon(epsilonin=epsilon)
        sp.Popen('cp -r epsilon.inp GW/epsilon',shell=True)        
        self.set_home()    

    def sigma(self,sigma={}):
        """
        prepare sigma calculation
        """
        self.set_work()
        (self.nk1,self.nk2,self.nk3) = self.BGW_init['grid_co']
        self.BGW_sigma['band_index_min'] = 1
        self.BGW_sigma['band_index_max'] = self.BGW_epsilon['number_bands']

        for key in sigma.keys():    
            self.BGW_sigma[key] = sigma[key]
        self.write_sigma()
        self.BGW_sig2wan['nbands'] = self.BGW_sigma['band_index_max']-self.BGW_sigma['band_index_min']
        self.BGW_sig2wan['ib_start'] = self.BGW_sigma['band_index_min']
        self.write_sig2wan()
        sp.Popen('cp -r sigma.inp GW/sigma/',shell=True)
        sp.Popen('cp -r sig2wan.inp GW/sigma/',shell=True)
        self.set_home()

    def kernel(self, kernel={}):
        """
        prepare kernel calculation
        """
        print('Kernel calculation')
        self.set_work()
        (self.nk1,self.nk2,self.nk3) = self.BGW_init['grid_co']
        self.BGW_kernel['number_val_bands'] = self.nbnd_val
        self.BGW_kernel['number_cond_bands'] = self.nbnd_cond
        self.BGW_kernel['screening_semiconductor'] = ' '

        for key in kernel.keys():    
            self.BGW_kernel[key] = kernel[key]
        print(self.BGW_kernel)
        self.write_kernel()
        sp.Popen('cp -r kernel.inp GW/kernel/',shell=True)
        self.set_home()

    def absorption(self, absorption={}):
        """
        prepare absorption calculation
        """
        self.set_work()
        (self.nk1,self.nk2,self.nk3) = self.BGW_init['grid_co']
        self.BGW_absorption['number_cond_bands_coarse'] = self.nbnd_val
        self.BGW_absorption['number_val_bands_coarse']  = self.nbnd_cond

        for key in absorption.keys():    
            self.BGW_absorption[key] = absorption[key]
        self.write_absorption()
        sp.Popen('cp -r absorption.inp GW/absorption/',shell=True)
        self.set_home()

        
    def prepare_wfn(self,kpoints={'grid':[6,6,6]},control={},system={},electrons={},cell={},pw2bgw={},filename ='GW/wfn'):
        self.set_work()
        self.wfn_filename = filename
        self.changedir(self.wfn_filename)

        if 'grid' in kpoints.keys():
            (self.nk1,self.nk2,self.nk3)=kpoints['grid']
            self.BGW_init['grid_co']=[self.nk1,self.nk2,self.nk3]
        else:
            (self.nk1,self.nk2,self.nk3)=self.BGW_init['grid_co']
            
        self.pw_kpoints['kpoints'] = self.GW_k
        self.pw_kpoints['kpoints_type'] = 'crystal'
        self.BGW_pw2bgw['wfng_nk1'] = self.nk1
        self.BGW_pw2bgw['wfng_nk2'] = self.nk2
        self.BGW_pw2bgw['wfng_nk3'] = self.nk3
                        
        self.pw_system['nbnd']=self.BGW_init['nbnd'] 
        if 'nbnd' in system.keys():
            self.BGW_pw2bgw['vxc_diag_nmax']=system['nbnd']

        self.write_scf_QE(control=control,system=system,electrons=electrons,ions={},cell=cell,name='wfn')
        self.write_pw2bgw(pw2bgw={})
        self.set_home()	

    def prepare_wfnq(self,kpoints={'grid':[6,6,6],'shift':[0.0,0.0,0.001]},control={},system={},electrons={},cell={},pw2bgw={},filename = 'GW/wfnq'):
        self.set_work()
        self.wfnq_filename = filename
        self.changedir(self.wfnq_filename)

        if 'grid' in kpoints.keys():
            (self.nk1,self.nk2,self.nk3) = kpoints['grid']
            self.BGW_init['grid_co'] = [self.nk1,self.nk2,self.nk3]
        else:
            (self.nk1,self.nk2,self.nk3) = self.BGW_init['grid_co']
            kpoints['shift'] = self.BGW_init['shift']
        self.shift = np.array(kpoints['shift'])
        self.GW_k[0,:3] += np.array(kpoints['shift'])
        self.pw_kpoints['kpoints'] = self.GW_k
        self.pw_kpoints['kpoints'][:,:3] += np.array(kpoints['shift'])
        self.pw_kpoints['kpoints_type']='crystal'
        self.BGW_pw2bgw['wfng_nk1'] = self.nk1
        self.BGW_pw2bgw['wfng_nk2'] = self.nk2
        self.BGW_pw2bgw['wfng_nk3'] = self.nk3
        self.BGW_pw2bgw['wfng_dk1'] = kpoints['shift'][0]
        self.BGW_pw2bgw['wfng_dk2'] = kpoints['shift'][1]
        self.BGW_pw2bgw['wfng_dk3'] = kpoints['shift'][2]
             
        self.pw_system['nbnd']=self.BGW_init['nbnd'] 
        if 'nbnd' in system.keys():
            self.BGW_pw2bgw['vxc_diag_nmax']=system['nbnd']

        self.write_scf_QE(control=control,system=system,electrons=electrons,ions={},cell=cell,name='wfnq')
        self.write_pw2bgw(pw2bgw={})
        self.set_home()	

    def prepare_wfnfi(self,kpoints={'grid':[6,6,6]},control={},system={},electrons={},cell={},pw2bgw={},filename='GW/wfnfi'):
        self.set_work()
        self.wfnfi_filename = filename
        self.changedir(self.wfnfi_filename)

        if 'grid' in kpoints.keys():
            (self.nk1,self.nk2,self.nk3) = kpoints['grid']
            self.BGW_init['grid_fi'] = [self.nk1,self.nk2,self.nk3]
        else:
            (self.nk1,self.nk2,self.nk3) = self.BGW_init['grid_fi'] 
          
        self.pw_kpoints['kpoints'] = self.GW_k
        self.pw_kpoints['kpoints_type'] = 'crystal'
        self.BGW_pw2bgw['wfng_nk1'] = self.nk1
        self.BGW_pw2bgw['wfng_nk2'] = self.nk2
        self.BGW_pw2bgw['wfng_nk3'] = self.nk3
        self.BGW_pw2bgw['wfng_dk1'] = 0.0
        self.BGW_pw2bgw['wfng_dk2'] = 0.0
        self.BGW_pw2bgw['wfng_dk3'] = 0.0
                    
        self.pw_system['nbnd'] = self.BGW_init['nbnd'] 
        if 'nbnd' in system.keys():
            self.BGW_pw2bgw['vxc_diag_nmax'] = system['nbnd']

        self.write_scf_QE(control=control,system=system,electrons=electrons,ions={},cell=cell,name='wfnfi')
        self.write_pw2bgw(pw2bgw={})
        self.set_home()	

    def prepare_wfnfiq(self,kpoints={'grid':[6,6,6]},control={},system={},electrons={},cell={},pw2bgw={},filename='GW/wfnfiq'):
        self.set_work()
        self.wfnfiq_filename = filename
        self.changedir(self.wfnfiq_filename)

        if 'grid' in kpoints.keys():
            (self.nk1,self.nk2,self.nk3) = kpoints['grid']
            self.BGW_init['grid_fi'] = [self.nk1,self.nk2,self.nk3]
        else:
            (self.nk1,self.nk2,self.nk3) = self.BGW_init['grid_fi'] 
          
        self.pw_kpoints['kpoints'] = self.GW_k
        self.pw_kpoints['kpoints'][:,:3] += np.array(kpoints['shift'])
        self.pw_kpoints['kpoints_type'] = 'crystal'
        self.BGW_pw2bgw['wfng_nk1'] = self.nk1
        self.BGW_pw2bgw['wfng_nk2'] = self.nk2
        self.BGW_pw2bgw['wfng_nk3'] = self.nk3
        self.BGW_pw2bgw['wfng_dk1'] = kpoints['shift'][0]
        self.BGW_pw2bgw['wfng_dk2'] = kpoints['shift'][1]
        self.BGW_pw2bgw['wfng_dk3'] = kpoints['shift'][2]
                    
        self.pw_system['nbnd'] = self.BGW_init['nbnd'] 
        if 'nbnd' in system.keys():
            self.BGW_pw2bgw['vxc_diag_nmax'] = system['nbnd']

        self.write_scf_QE(control=control,system=system,electrons=electrons,ions={},cell=cell,name='wfnfiq')
        self.write_pw2bgw(pw2bgw={})
        self.set_home()        



    def prepare_GW(self):
        self.set_work()
        prefix=self.prefix.replace('\'','')
        self.makedir('GW')
        self.makedir('GW/wfn')
        self.makedir('GW/wfnq')
        self.makedir('GW/wfnfi')
        self.makedir('GW/wfnfiq')
        self.makedir('GW/epsilon')
        self.makedir('GW/sigma')
        self.makedir('GW/kernel')
        self.makedir('GW/absorption')
        self.makedir('GW/sig2wan') 
        try:
            sp.Popen('cp -r ./scf/'+str(prefix)+'.save ./GW/wfn/',shell=True)
            sp.Popen('cp -r ./scf/'+str(prefix)+'.save ./GW/wfnq/',shell=True)
            sp.Popen('cp -r ./scf/'+str(prefix)+'.save ./GW/wfnfi/',shell=True)
            sp.Popen('cp -r ./scf/'+str(prefix)+'.save ./GW/wfnfiq/',shell=True)
        except FileNotFoundError:
            print('No DFT save file found')
            print('Run scf first')
        self.set_home()

    def prepare_link(self):
        self.set_work()
        cwd=os.getcwd()
        set_links(cwd)
        self.set_home()

    @property
    def GW_k(self):
        k = np.zeros((self.nk1*self.nk2*self.nk3,4),dtype=float)
        kx = [1,0,0]
        ky = [0,1,0]
        kz = [0,0,0]
        h = np.linspace(0.0,1,self.nk1,endpoint=False)
        k = np.linspace(0.0,1,self.nk2,endpoint=False)
        l = np.linspace(0.0,1,self.nk3,endpoint=False)
        k = k_mesh(h,k,l,kx,ky,kz)
        return(np.array(k))

    @property
    def nbnd_co(self):
        self.set_work()
        try:
            Bands = extract_band_scf('GW/wfn/wfn.out')
            return(len(Bands[0,:])-1)
        except FileNotFoundError:
            return(None)
        self.set_home()

    @property
    def nbnd_cond(self):
        self.set_work()
        try:
            Bands = extract_band_scf('GW/wfn/wfn.out')
            ef = find_fermi(f'{self.scf_fold}/{self.scf_file}')
            minband = self.BGW_sigma['band_index_min']
            maxband = self.BGW_sigma['band_index_max']
            nband = maxband - minband
            print('nband',nband)
            print('Fermi',ef)
            for i in range(nband):
                if (min(Bands[:,minband+i-1]) > ef):
                    print('minband',minband+i-1)
                    return(minband+i-1)
        except FileNotFoundError:
            print('no prior coarse grid calculation')
        self.set_home()

    @property
    def nbnd_val(self):
        self.set_work()
        try:
            Bands = extract_band_scf('GW/wfn/wfn.out')
            ef = find_fermi(f'{self.scf_fold}/{self.scf_file}')
            minband = self.BGW_sigma['band_index_min']
            maxband = self.BGW_sigma['band_index_max']
            nband = maxband - minband
            for i in range(nband):
                if (min(Bands[:,minband+i-1]) > ef):
                    return(minband+i-2)
        except FileNotFoundError:
            print('no prior coarse grid calculation')
        self.set_home()

    @property
    def nbnd_fi(self):
        self.set_work()
        try:
            Bands = extract_band_scf('GW/wfnfi/wfnfi.out')
            return(len(Bands[0,:])-1)
        except FileNotFoundError:
            return(None)
        self.set_home()
 
