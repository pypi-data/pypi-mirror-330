#
"""
QE class for interfacing with quantum espresso
"""
from __future__ import annotations
import numpy as np
import argparse
from EPWpy.utilities.set_files import *
from EPWpy.default.default import *
from EPWpy.structure.lattice import *
import os
from EPWpy.utilities.k_gen import *
from EPWpy.utilities.epw_pp import *
from EPWpy.utilities.save_state import *
from EPWpy.utilities.printing import *
from EPWpy.QE.PW_util import *


class set_QE:
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

    def set_electrons(self, electrons):

        for key in electrons.keys():
            self.pw_electrons[key] = electrons[key]

    def set_control(self, control):

        for key in control.keys():
            self.pw_control[key] = control[key]

    def set_system(self, system):

        for key in system.keys():
            self.pw_system[key]=system[key]

    def set_ions(self, ions):

        for key in ions.keys():
            self.pw_ions[key] = ions[key]

    def set_cell(self, cell):

        for key in cell.keys():
            self.pw_cell[key] = cell[key]

    def set_kpoints(self, kpoints):

        for key in kpoints.keys():
            if key in self.pw_kpoints.keys():
                self.pw_kpoints[key]=kpoints[key]
        if 'grid' in kpoints.keys():
            (nk1,nk2,nk3)=kpoints['grid']

            self.grid = kpoints['grid']

            k=np.zeros((nk1*nk2*nk3,4),dtype=float)
            kx=[1,0,0]
            ky=[0,1,0]
            kz=[0,0,0]
            
            h=np.linspace(0.0,1,nk1,endpoint=False)
            k=np.linspace(0.0,1,nk2,endpoint=False)
            l=np.linspace(0.0,1,nk3,endpoint=False)

            k=k_mesh(h,k,l,kx,ky,kz)
            self.k = k
            self.pw_kpoints['kpoints']=k
            self.pw_kpoints['grid'] = kpoints['grid']
    
    def set_cell_parameters(self, cell_parameters, setcell = False):
        """
        sets cell_parameters
        """
        for key in cell_parameters.keys():
            self.pw_cell_parameters[key]=cell_parameters[key]

        if(setcell == True):

            if (self.pw_control['calculation'] != 'scf'):
                PW_ut = PW_properties(f'{self.scf_file}/scf.out')
                param = 0.529177 
                self.pw_cell_parameters['lattice_vector'] = PW_ut.lattice_vec*param
 
    def set_cards(self, cards):
        for card in cards:
            print(card)
            self.card_params[card] = cards[card]
            for key in cards[card].keys():
                self.card_params[card][key]=cards[card][key]
 
    def set_phonons(self, phonons, qpoints):
        """
        setting phonon attributes
        """
        self.ph_params['fildyn'] = f'\'{self.prefix}.dyn\''
        self.ph_params['fildvscf'] = f'\'dvscf\''
        for key in phonons:
            self.ph_params[key] = phonons[key] 

        for key in qpoints:
            self.ph_qpoints[key] = qpoints[key] 

    def set_matdyn(self,matdyn, kpoints):
        """
        setting matdyn attributes
        """
        self.matdyn_input['mass']=self.pw_atomic_species['mass']
        self.matdyn_input['flfrc']=f'\'{self.prefix}.fc\''
        self.matdyn_input['flfrq']=f'\'{self.prefix}.freq\'',
        for key in kpoints.keys():
            self.matdyn_kpoints[key]=kpoints[key]

        for key in matdyn.keys():
            self.matdyn_input[key]=matdyn[key]

    def set_eps(self, inputpp, energy_grid):
        """
        setup eps
        """
        self.eps_inputpp['prefix']=f'\'{self.prefix}\'' 
        for key in inputpp.keys():
            self.eps_inputpp[key] = inputpp[key]

        for key in energy_grid.keys():
            self.eps_energy_grid[key] = energy_grid[key]
         

        for key in qpoints:
            self.ph_qpoints[key] = qpoints[key] 


    def set_wannier(self, win, pw2wan):
        """
        Sets the variables for a Wannier function calculation
        """
        self.pw2wann_params['seedname']=self.prefix
        #
        if('noncollin' in self.pw_system.keys()):
            self.wannier_params['spinor']='.true.'

        fermi=find_fermi()
        self.wannier_params['dis_win_max'] = fermi+10        
        self.wannier_params['dis_win_min'] = fermi-10
        # for future implementation of projections
        #self.default_wannier['projections'][:]=obtain_projections()
        #
        self.wannier_params['kpoints'] = None
        self.wannier_params['projections'] = 'auto_projections'
        self.wannier_params['num_bands'] = obtain_bands([self.wannier_params['dis_win_min'],
                                                self.wannier_params['dis_win_max']]) 
        self.wannier_params['num_wann'] = obtain_bands([self.wannier_params['dis_win_min'],
                                                self.wannier_params['dis_win_max']]) 
        self.wannier_params['atomic_positions'] = self.pw_atomic_positions['atomic_pos']
        self.wannier_params['cell_parameters'] = self.pw_cell_parameters['lattice_vector']
        try:
            if (np.sum(self.wannier_params['cell_parameters'].astype(float)[:,0]) == 0):
                self.set_cell_parameters()
 
        except ValueError:

            self.set_cell_parameters(cell_parameters={},setcell = True)
        self.wannier_params['cell_parameters'] = self.pw_cell_parameters['lattice_vector']
 
        for key in win.keys():
           self.wannier_params[key]=win[key]
        for key in pw2wan.keys():
           self.pw2wann_params[key]=pw2wan[key]

    def set_q2r(self, q2r):
        q2r_params['fildyn']=f'\'{self.prefix}.dyn\''
        q2r_params['flfrc']=f'\'{self.prefix}.fc\''
        for key in q2r.keys():
            self.q2r_params[key] = q2r[key]

    def set_bands(self, bands):
        pw_bands['fildyn']=f'\'{self.prefix}\''
        for key in bands.keys():
            self.pw_bands[key] = bands[key]
 
    def set_zg(self, inputzg, inputazg):
        """
        Preparing EPW/ZG calculation
        """
        zg_inputzg['fildyn']=f'\'{self.prefix}.dyn\''
        zg_inputzg['flfrc']=f'\'{self.prefix}.fc\''

        for key in inputzg.keys():
            self.zg_inputzg[key] = inputzg[key]

        for key in inputazg.keys():
            self.zg_inputazg[key] = inputazg[key]

    def set_zg_o(self, zg):
        """ 
        keeping this as legacy in case!
        """
        zg_params['fildyn']=f'\'{self.prefix}.dyn\''
        zg_params['flfrc']=f'\'{self.prefix}.fc\''
        for key in zg.keys():
            self.zg_params[key] = zg[key]

    def set_eps(self, inputpp, energy_grid):
        for key in inputpp.keys():
           self.eps_inputpp[key]=inputpp[key]
        for key in energy_grid.keys():
           self.eps_energy_grid[key]=energy_grid[key]

    def set_epw(self, epwin):
        """
        Setting EPW calculation
        """
        self.filkf_file = None
        self._set_from_pw(epwin)

        if (self.epw_restart == True):
            self._set_epw_restart(epwin)        
        else:
            self._set_epw_start(epwin)        

        if (('refresh' in epwin.keys()) | (self.epw_refresh != None)):
            self._refresh_epw()

        if ('hard_refresh' in epwin.keys()):
            self._hard_refresh()

        if ('band_plot' in epwin.keys()):
            epwin = self._set_epw_band(epwin)

        if ('clean_transport' in epwin.keys()):
            self._clean_transport()


        if ('filkf' in epwin.keys()):
            self.filkf_file = epwin['filkf']
            self.filkf_file = self.filkf_file.replace('\'','') 
            self.transfer_file = [self.filkf_file]
        else:
            self.filkf_file = None
            self.epw_params['band_plot'] = None
            
        if ('filqf' in epwin.keys()):
            self.filqf_file=epwin['filqf']
            self.filqf_file=self.filqf_file.replace('\'','')
            self.transfer_file = [self.filqf_file]
        else:
            self.filqf_file = None
            self.epw_params['band_plot'] = None 

        if ('reset_transport' in epwin.keys()):
            self._reset_transport()

        if ('transport_calc' in epwin.keys()):
            self._set_epw_transport(epwin)

        if ('optics_calc' in epwin.keys()):
            self._set_epw_optics(epwin)
         
        dict1={'mass':self.pw_atomic_species['mass'],
               'nk1':self.nk_1,
               'nk2':self.nk_2,
               'nk3':self.nk_3,
               'nq1':self.ph_params['nq1'],
               'nq2':self.ph_params['nq2'],
               'nq3':self.ph_params['nq3']}

        self.epw_params.update(dict1)
        for key in epwin.keys():
            self.epw_params[key] = epwin[key] 

    def filkf(self,path=[[0.5,0.0,0.5],
                         [0.0,0.0,0.0],
                         [0.5,0.25,0.75],
                         [0.0,0.0,0.0]],
             length=[10,10,10], name='filkf.txt'):                    
        self.set_work()
        self._set_filkf(path, length, name)
        self.set_home()

    def _set_filkf(self,path=[[0.5,0.0,0.5],
                         [0.0,0.0,0.0],
                         [0.5,0.25,0.75],
                         [0.0,0.0,0.0]],
             length=[10,10,10], name='filkf.txt'):                    
        K=path 
        kx=[1,0,0]
        ky=[0,1,0]
        kz=[0,0,0]
        leng=length
        K=k_path(K,leng,kx,ky,kz)
        np.savetxt(str(self.filkf_file),K,fmt='%1.3f',
                  header=str(sum(length)-1*len(length))+' crystal', 
                  comments='')

    def _set_epw_restart(self,epwin):
        """
        Setting epw variables for a restart
        """
        self.epw_params.update({'epwread':'.true.',
                                'epbread':'.false.',
                                'epwwrite':'.false.',
                                'wannierize':'.false.'})        

    def _set_epw_start(self,epwin):
        """
        Setting epw variables for a restart
        """
        self.epw_params.update({'epwread':'.false.',
                                'epbread':'.false.',
                                'epwwrite':'.true.',
                                'wannierize':'.true.'})        
    def _set_epw_band(self,epwin):
        """
        sets default value for epw band calculation
        """
        if ('path' in epwin.keys()):
            path = epwin['path']            
        else:
            path = self._get_default_path()
        if ('length' in epwin.keys()):
            length = epwin['length']
        else:
            length = self._get_default_length(path)

        if ('filkf' in epwin.keys()):
            self.filkf_file = epwin['filkf']
            self.filkf_file = self.filkf_file.replace('\'','') 
        else:
            self.filkf_file = 'filkf.txt'
        self.transfer_file = [self.filkf_file]
            
        if ('filqf' in epwin.keys()):
            self.filqf_file = epwin['filqf']
            self.filqf_file = self.filqf_file.replace('\'','')
        else:
            self.filqf_file =  'filkf.txt'
        self.transfer_file = [self.filqf_file]
        self._set_filkf(path,length)

        self.epw_params['filkf'] = f'\'{self.filkf_file}\''
        self.epw_params['filqf'] = f'\'{self.filqf_file}\''

        epwin['path'] = None
        epwin['length'] = None 

        return(epwin)

    def _get_default_path(self):
        """
        should be able to get bandpath based on symmetry in future
        """
        path=[[0.5,0.0,0.5],
              [0.0,0.0,0.0],
              [0.5,0.25,0.75],
              [0.0,0.0,0.0]]
        return path

    def _get_default_length(self, path=[]):
        leng = []
        for i in range(len(path)-1):
            leng.append(51)
        print(np.shape(path))
        print(leng)
        return(leng)

 
    def _refresh_epw(self):
        """
        Minor refresh for EPW
        """
        for key in self.epw_params.keys():
            if(key == 'mass'):
                continue
            else:
                if (key not in ['lpolar','system_2d','elph','epwread','epwwrite','epbread','asr_typ','dvscf_dir','use_ws','prefix','iverbosity','outdir','nbndsub']):
                    self.epw_params[key]= None

    def _hard_refresh(self):
        """
        Hard reset for EPW
        """
        for key in self.epw_params.keys():
            if(key == 'mass'):
                continue
            else:
                if (key not in ['lpolar','system_2d','asr_typ','dvscf_dir','use_ws','prefix','iverbosity','outdir','nbndsub']):
                    self.epw_params[key]= None
        self.epw_params['elph'] = '.true.'
        self.epw_params['epwread'] = '.false.'
        self.epw_params['epwwrite'] = '.true.'
        self.epw_params['epbwrite'] = '.false.'

    def _clean_transport(self):
        """
        Clean transport 
        """
        os.system('rm -r ./epw/Fsparse* ')            
        os.system('rm -r ./epw/Fepmatkq* ')            
        os.system(f'rm -r ./epw/{self.prefix}.epmatkq1 ')            
        os.system(f'rm -r ./epw/{self.prefix}.epmatkqcb1 ')            
        os.system(f'rm -r ./epw/restart.fmt ')            
        os.system(f'rm -r ./epw/sparse* ')            
        self.epw_params['clean_transport'] = None

    def _reset_transport(self):
        """
        remove restart transport 
        """
        os.system(f'rm -r ./epw/restart.fmt ')            
        self.epw_params['reset_transport'] = None

    @decorated_warning_transport
    def _set_epw_transport(self,epwin):
        """
        sets parameters for a transport calculation
        """
        self.epw_params.update({'scattering':'.true.',
                        'int_mob':'.false.',
                        'carrier':'.true.',
                        'iterative_bte':'.true.',
                        'degaussw':0.0,
                        'ncarrier':'-1E13',
                        'fsthick':0.3})

        if (epwin['transport_calc'] == 'electron'):
            self.epw_params.update({'ncarrier':'1E13'})

        elif(epwin['transport_calc'] == 'hole'):
            self.epw_params.update({'ncarrier':'-1E13'})

        elif(epwin['transport_calc'] == 'intrinsic'):
            self.epw_params.update({'int_mob':'.true.'})
 
        if ('ncarrier' in epwin.keys()):
            self.epw_params['ncarrier'] = epwin['ncarrier']
            
        self.epw_params['transport_calc'] = None

    @decorated_warning_pw
    def _set_from_pw(self, epwin):
        """
        sets parameters from pw calculation
        """
        if ('assume_isolated' in self.pw_system.keys()):
            if (('system_2d' not in epw_params.keys()) & ('system_2d' not in epwin.keys())):
                self.epw_params['system_2d'] = '\'dipole_sp\''
            self.epw_params['lpolar'] = '.true.'

        if ('epsil' in self.ph_params.keys()):
            if (self.ph_params['epsil'] == '.true.'):
                self.epw_params['lpolar'] = '.true.'
 
    @decorated_warning_optics
    def _set_epw_optics(self,epwin):
        """
        sets parameters for an optics calculation
        """
        self.epw_params.update({'loptabs':'.true.',
                            'omegamin':0.005,
                            'omegamax':3.2,
                            'omegastep':0.05,
                            'degaussw':0.05,
                            'efermi_read':'.true.',
                            'fermi_energy':find_fermi(f'{self.scf_fold}/{self.scf_file}.out')+0.1})
        self.epw_params['optics_calc'] = None

    @property
    def nk_1(self):
        if 'grid' not in self.pw_kpoints.keys():    
            raise KeyError('grid keyword not found in save point')
        else:
            return(self.pw_kpoints['grid'][0])
            
    @property
    def nk_2(self):
        return(self.pw_kpoints['grid'][1]) 

    @property
    def nk_3(self):
        return(self.pw_kpoints['grid'][2]) 
       
