import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
print(str(os.getcwd())+'../EPWpy/')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest

def test_epw():

    benchmark= 74027.34689441035
    cwd=os.getcwd()
    QE=cwd+'/build/q-e/bin'   
    system_n = 'epw_indabs'
    silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np', system = system_n)
    
    silicon.run_serial=True 
    silicon.scf(electrons={'conv_thr':'1E-11'},
                kpoints={'kpoints':[[3,3,3]]},
                control = {'calculation':'\'scf\''})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')
    silicon.ph(phonons={'nq1':2,'nq2':2,'nq3':2})
    silicon.prepare(1,type_run='ph')
    silicon.run(1,type_run='ph')
    silicon.nscf(kpoints={'grid':[4,4,4],'kpoints_type': 'crystal'},control={'calculation':'\'bands\''},system={'nbnd':12})
    silicon.prepare(1,type_run='nscf')
    silicon.run(1,type_run='nscf')
    
    silicon.epw(epwin={'wdata':['guiding_centres = .true.',
                            'dis_num_iter = 100',
                            'num_print_cycles  = 10',
                            'dis_mix_ratio = 1',
                            'use_ws_distance = T'],
                            'proj':['\'Si : sp3\''],
                            'band_plot':'.true.',
                            'filkf':'\'LGX.txt\'',
                            'filqf':'\'LGX.txt\'',
                            'eig_read':'false',
                            'calc_nelec_wann':'.false.',    
                            'nk1':4,
                            'nk2':4,
                            'nk3':4,
                            'nq1':2,
                            'nq2':2,
                            'nq3':2},
            name='epw1')
    silicon.filkf(path=[[0.5,0.5,0.5],
           [0,0,0],[0.5,0.5,0.5]],length=[51,51],name='LGX.txt')
    silicon.prepare(1,type_run='epw1')

    silicon.run(1,'epw1')
 
    silicon.epw(epwin={'elph':'.true.',
                   'epbwrite':'.false.',
                   'epbread':'.false.',
                   'epwwrite': '.false.',
                   'epwread':'.true.',
                   'etf_mem': '1',
                   'wannierize':'.false.',
                   'omegamin':0.05,
                   'omegamax':4.0,
                   'omegastep':0.05,
                   'lindabs':'.true.',
                   'eig_read':'.false.',
                   'nkf1':6,
                   'nkf2':6,
                   'nkf3':6,
                   'nqf1':2,
                   'nqf2':2,
                   'nqf3':2,  
                   'mp_mesh_k':'.true.',
                   'efermi_read':'.true.',
                   'fermi_energy':6.5,
                   'lpolar':'.true.',
                   'fsthick': 5.5,
                   'temps':300 ,
                   'degaussw':0.1,
                   'nk1':4,
                   'nk2':4,
                   'nk3':4,
                   'nq1':2,
                   'nq2':2,
                   'nq3':2},
            name='epw2')

    silicon.prepare(1,type_run='epw2')

    silicon.run(1,type_run='epw2')

    cwd=os.getcwd()

    silicon.file=cwd+f'/{system_n}/epw/epw2.out'
    silicon.get_EPW_status()
 
    eps=extract_epsilon(cwd+f'/{system_n}/epw/epsilon2_indabs_300.0K.dat')
    eps_sum=np.sum(eps[:,1])
    T_F=match_benchmark(benchmark,eps_sum,thr=1E4)
    if(T_F == False):
        print('difference in benchmark data',abs(eps_sum-benchmark))
        print('epw run data',abs(eps_sum))
 
    assert(T_F)==True







