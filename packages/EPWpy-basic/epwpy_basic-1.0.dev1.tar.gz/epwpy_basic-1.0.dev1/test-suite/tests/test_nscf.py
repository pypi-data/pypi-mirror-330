import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
print(str(os.getcwd())+'../EPWpy/')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest


   
def test_nscf():
    benchmark=6.1269
    cwd=os.getcwd()
    system = 'nscf' 
    try:
        silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            env='mpirun', system = 'nscf')
    except:
        silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            env='mpirun --allow-run-as-root -np')
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
    HUMO=extract_HUMO(cwd+f'/{system}/nscf/nscf.out')
    del silicon    
    T_F=match_benchmark(benchmark,HUMO)
    assert(T_F)==True

