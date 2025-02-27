import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../EPWpy/')
print(str(os.getcwd())+'../EPWpy/')
from EPWpy import *
from test_extract import *
import pytest


def test_scf():
    benchmark=-16.88017346
    cwd=os.getcwd()
    try:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun -np')
    except:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np')
    silicon.run_serial=True 
 
    silicon.scf(electrons={'conv_thr':'1E-11'},
                kpoints={'kpoints':[[3,3,3]]},
                control={'calculation':'\'scf\''})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')

    cwd=os.getcwd()
   
    tot_energy=extract_total_energy(cwd+'/si/scf/scf.out')
    T_F=match_benchmark(benchmark,tot_energy)
    del silicon
    assert(T_F)==True
    
def test_nscf():
    benchmark=6.1269
    cwd=os.getcwd()
 
    try:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun -np')
    except:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np')
    silicon.run_serial=True 
 
    silicon.scf(electrons={'conv_thr':'1E-11'},
                kpoints={'kpoints':[[3,3,3]]},
                control={'calculation':'\'scf\''}) 
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')
    silicon.nscf(kpoints={'grid':[6,6,6],'kpoints_type': 'crystal'})
    silicon.prepare(1,type_run='nscf')
    silicon.run(1,type_run='nscf')
  
    cwd=os.getcwd()
    HUMO=extract_HUMO(cwd+'/si/nscf/nscf.out')
    del silicon    
    T_F=match_benchmark(benchmark,HUMO)
    assert(T_F)==True

    
def test_ph():
    benchmark=33.887647624
    cwd=os.getcwd()
 
    try:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun -np')
    except:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np')
    silicon.run_serial=True 
 
    silicon.scf(electrons={'conv_thr':'1E-11'},
                kpoints={'kpoints':[[3,3,3]]},
                control={'calculation':'\'scf\''}) 

    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')
    silicon.ph(phonons={'nq1':2,'nq2':2,'nq3':2})
    silicon.prepare(1,type_run='ph')
    silicon.run(1,type_run='ph')

    cwd=os.getcwd()
    eps=extract_dielectric(cwd+'/si/ph/ph.out')
    del silicon    
    T_F=match_benchmark(benchmark,eps)
    assert(T_F)==True

def test_epw():

    benchmark = 137610.5959

    cwd=os.getcwd()
    QE=cwd+'/build/q-e/bin'
    QE='/workspace/Sabya/codes/q-e_fix/bin'   
    try:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun -np')
    except:
        silicon=EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np')
    silicon.run_serial=True 
    silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]},
                control={'calculation':'\'scf\''}) 
 
    silicon.prepare(1,type_run='scf')
    silicon.run(4,'scf')
    silicon.ph(phonons={'nq1':2,'nq2':2,'nq3':2})
    silicon.prepare(1,type_run='ph')
    silicon.run(4,type_run='ph')
    silicon.nscf(kpoints={'grid':[4,4,4],'kpoints_type': 'crystal'},control={'calculation':'\'bands\''},system={'nbnd':12})
    silicon.prepare(1,type_run='nscf')
    silicon.run(4,type_run='nscf')
    
    silicon.epw(epwin={'wdata':['\'guiding_centres = .true.\'',
                            '\'dis_num_iter = 100\'',
                            '\'num_print_cycles  = 10\'',
                            '\'dis_mix_ratio = 1\'',
                            '\'use_ws_distance = T\''],
                            'dis_win_max':'18',
                            'dis_froz_max':'10',
                            'nbndsub': '8',
                            'proj':['\'Si : sp3\''],
                            'band_plot':'.true.',
                            'filkf':'\'LGX.txt\'',
                            'filqf':'\'LGX.txt\'',
                            'eig_read':'false',    
                            'nk1':4,
                            'nk2':4,
                            'nk3':4,
                            'nq1':2,
                            'nq2':2,
                            'nq3':2},
            name='epw1')
#    silicon.prefix='si'
    silicon.filkf(path=[[0.5,0.5,0.5],
           [0,0,0],[0.5,0.5,0.5]],length=[51,51])
    silicon.prepare(1,type_run='epw1')

    silicon.run(4,'epw1')

    silicon.epw(epwin={'elph':'.true.',
                   'epbwrite':'.false.',
                   'epbread':'.false.',
                   'epwwrite': '.false.',
                   'epwread':'.true.',
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

    silicon.run(4,type_run='epw2')

    cwd=os.getcwd()
    eps=extract_epsilon(cwd+'/si/epw/epsilon2_indabs_300.0K.dat')
    eps_sum=np.sum(eps[:,1])
    T_F=match_benchmark(benchmark,eps_sum,thr=1E-2)
    if(T_F == False):
        print('difference in benchmark data',abs(eps_sum-benchmark))
    assert(T_F)==True




