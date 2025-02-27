import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../EPWpy/')
sys.path.insert(0,'/scratch1/05193/sabyadk/Si_transport/Si_161616/EPWpy2/epwpy/')
from EPWpy import *
from EPWpy import EPWpy
from EPWpy.utilities import Band,k_gen
from EPWpy.QE.PW_util import *
from scipy import *
import scipy.optimize as sco
#import matplotlib.pyplot as plt

def read_kpt(file):
   
    with open(file,'r') as f:

        for line in f:
            if len(line.split()) < 2:
                print(line.split())
                size=int(line.split()[0])
                A=np.zeros((size,4),dtype=float)
                t = 0
            if len(line.split()) > 2:

                A[t,:]=np.array(line.split()).astype(float)   
                t += 1
    return(A)


    
QE='/workspace/Sabya/codes/q-e_fix/bin'
QE='/workspace/Sabya/codes/q-e_fix/bin'
QE='/work2/05193/sabyadk/shared/q-e/q-e/bin'
#/workspace/Sabya/codes/EPW_5.9s/q-e/bin'
nband = 30


pseudo_dir = '\'/scratch1/05193/sabyadk/Si_transport/Si_161616/\'' 
silicon=EPWpy.EPWpy({'prefix':'\'hBN\'','pseudo_dir':pseudo_dir , 'pseudo':['Si-PBE.upf'], 'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\'','celldm(1)':10.262,'atoms':['Si','Si'],
        'atomic_species':np.array(['Si']),'atomic_position_type':'{crystal}','atomic_pos':np.array([[0.0, 0.0, 0.0],[-0.25, 0.75, -0.25]]),'mass':[28.0855],'ntyp':1},
        code=QE,env='mpirun ',system='hBN')
silicon.run_serial=True
 
silicon.scf(electrons={'conv_thr':'1E-13'},kpoints={'kpoints':[[20,20,20]]})
#silicon.prepare(4,type_run='scf')
silicon.run_serial=True
#silicon.run(48,'scf')
silicon.file='hBN/scf/scf.out'
silicon.get_QE_status()

silicon.nscf(control={'calculation':'bands'},kpoints={'grid':[6,6,6],'kpoints_type':'crystal'},system={'nbnd':nband}) 
silicon.prepare(4,type_run='nscf')
silicon.run_serial=True
#silicon.run(48,'nscf')
silicon.file='hBN/nscf/nscf.out'
silicon.get_QE_status()


silicon.ph(phonons={'fildyn':'\'hBN.dyn\'',
                    'nq1':6,
                    'nq2':6,
                    'nq3':6,
                    'fildvscf':'\'dvscf\'',
                    'epsil':'.true.'})
#silicon.prepare(2,type_run='ph')
#silicon.run(192,'ph',parallelization='-nk 16')

silicon.file='hBN/ph/ph.out'

K=[[0.0, 0.0, 0.0], [0.33, 0.33, 0.0], [0.5, 0.5, 0.0], [0.0, 0.0, 0.0],[0.33,0.33,0.5]]
kx=[1,0,0]
ky=[0,1,0]
kz=[0,0,1]
leng=[81,81,81,81]#,81,81,81,81,81,81]
K=k_gen.k_path(K,leng,kx,ky,kz)
silicon.pw_kpoints['kpoints']=K
silicon.pw_kpoints['kpoints_type']='crystal'
silicon.scf(control={'calculation':'bands'},system={'nbnd':52},name='bs')
#silicon.prepare(4,type_run='bs')
silicon.run_serial=True
#silicon.run(16,'bs')
#silicon.file='hBN/bs/bs.out'
#silicon.get_QE_status()

silicon.GW(GW={'nbnd':60})
silicon.epsilon(epsilon={'restart':' ', 'degeneracy_check_override':' '})
#silicon.run(48,'GW')

silicon.code='/work2/05193/sabyadk/frontera/codes_EPW/BGW/BerkeleyGW-3.0.1/bin/'
#
#silicon.epsilon(epsilon={'restart':' ', 'degeneracy_check_override':' '})
#silicon.run(192,'epsilon')


silicon.sigma(sigma={'degeneracy_check_override':' ',
                     'no_symmetries_q_grid':' ',
                     'screened_coulomb_cutoff':20.0, 
                     'band_index_min': 1,
                     'band_index_max':12})
silicon.run(192,'sigma')
silicon.scf_fold = 'scf'
silicon.scf_file = 'scf.out'

silicon.run(1,'sigma2wan')

silicon.kernel(kernel={})
#silicon.run(192,'kernel')

os.system('cp hBN/GW/sigma/eqp1.dat  hBN/GW/absorption/eqp_co.dat')

silicon.absorption(absorption={'number_val_bands_fine':2,
                                'number_cond_bands_fine':2,
                                'diagonalization':' ',
                                'screening_semiconductor':' ',
                                'eqp_co_corrections':' ',
                                'use_momentum':' ',
                                'gaussian_broadening':' ',
                                'degeneracy_check_override':' ',
                                'energy_resolution': 0.02})
silicon.run(192,'absorption')

silicon.code=QE      

silicon.epw(epwin={'wdata':['dis_num_iter = 100',
                            'num_print_cycles  = 10'],
                            'bands_skipped':'\'exclude_bands 1:4\'',
                            'nbndsub':12,
                            'use_ws': '.true.',
                            'dis_win_max':  38.631838702602536,
                            'dis_win_min': -3.36809999999999,
                            'dis_froz_min': 6.631900000000001,
                            'dis_froz_max':  12.955617654257395,
                            'proj': ["'Si: l= -5, mr= 1,2,6'", "'Si: l= -5, mr= 3,4,5'"],
                            'band_plot':'.true.',
                            'filkf':'\'LGX.txt\'',
                            'filqf':'\'LGX.txt\'',
                            'elph':'.true.',
                            'eig_read':'false',
                            'num_iter': 100,    
                            'etf_mem':0,
                            'fsthick':6.0,
                            'epwread':'.false.',
                            'epwwrite':'.true.',
                            'lpolar': '.true.'},
            name='epw1')
 
silicon.filkf(path=[[0.0, 0.0, 0.0], [0.33, 0.33, 0.0], [0.5, 0.5, 0.0], [0.0, 0.0, 0.0],[0.33,0.33,0.5]],length=[81,81,81,81],name='LGX.txt')
silicon.prepare(20,type_run='epw1')
silicon.run(192,'epw1')
silicon.file='hBN/epw/epw.out'
silicon.get_EPW_status()


silicon.epw(epwin={ 'wannierize': '.false.',
                            'nbndsub':12,
                            'epwread': '.true.',
                            'epwwrite':'.false.',
                            'scattering':'.true.',
                            'int_mob':'.false.',
                            'carrier':'.true.',
                            'ncarrier':'1E13',
                            'iterative_bte':'.true.',
                            'mob_maxiter':'500',
                            'temps':'100,150,200,250,300,350,400,450,500',
                            'nstemp':9,
                            'fsthick':'0.2',
                            'etf_mem':'3',
                            'degaussw':'0.0',
                            'use_ws': '.true.',
                            'nkf1':60,
                            'nkf2':60,
                            'nkf3':60,
                            'nqf1':60,
                            'nqf2':60,
                            'nqf3':60,
                            'mp_mesh_k':'.true.',
                            'elph':'.true.',
                            'eig_read':'false',
                            'efermi_read':'.true.',
                            'fermi_energy':6.78,
                            'clean_transport':None, 
                            'iverbosity':3,
                            'mob_maxfreq':90,     
                            'mob_nfreq':300,                       
                            'lpolar':'.true.'},
                            name='epw2')
silicon.prepare(20,type_run='epw2')
silicon.run(192,'epw2')
silicon.file='hBN/epw/epw2.out'
silicon.get_EPW_status()



