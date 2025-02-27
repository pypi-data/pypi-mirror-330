import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest

    
def test_ph():
    benchmark=33.887168940
    cwd=os.getcwd()
    QE=cwd+'/build/q-e/bin'
    system = 'ph'
    silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np', system = system)
    silicon.run_serial=True 
    
    silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')
    silicon.ph(phonons={'nq1':2,'nq2':2,'nq3':2,'fildvscf':'\'dvscf\''})
    silicon.prepare(1,type_run='ph')
    silicon.run(1,type_run='ph')
    
    cwd=os.getcwd()
    eps=extract_dielectric(cwd+f'/{system}/ph/ph.out')

    T_F=match_benchmark(benchmark,eps)
    assert(T_F)==True




