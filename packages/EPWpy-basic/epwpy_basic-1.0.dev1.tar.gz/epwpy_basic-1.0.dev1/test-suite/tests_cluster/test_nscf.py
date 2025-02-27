import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest

   
def test_nscf():
    benchmark=6.1269
    cwd=os.getcwd()
    QE=cwd+'/build/q-e/bin'
    system = 'nscf'
    silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np', system = system)
    silicon.run_serial=True 
    silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')
    silicon.nscf(kpoints={'grid':[6,6,6],'kpoints_type': 'crystal'})
    silicon.prepare(1,type_run='nscf')
    silicon.run(1,type_run='nscf')
  
    cwd=os.getcwd()
    HUMO=extract_HUMO(cwd+f'/{system}/nscf/nscf.out')
    
    T_F=match_benchmark(benchmark,HUMO)
    assert(T_F)==True






