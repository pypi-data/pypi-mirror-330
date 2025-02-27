import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
print(str(os.getcwd())+'../EPWpy/')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest


def test_scf():
    benchmark=-16.87986980
    cwd=os.getcwd()
    system = 'scf' 
    try:
        silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            env='mpirun',system = 'scf')
    except:
        silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            env='mpirun --allow-run-as-root -np')
    silicon.run_serial=True 
 
    silicon.scf(electrons={'conv_thr':'1E-11'},
                kpoints={'kpoints':[[3,3,3]]},
                control={'calculation':'\'scf\''})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')

    cwd=os.getcwd()
   
    tot_energy=extract_total_energy(cwd+f'/{system}/scf/scf.out')
    T_F=match_benchmark(benchmark,tot_energy)
    del silicon
    assert(T_F)==True
    

