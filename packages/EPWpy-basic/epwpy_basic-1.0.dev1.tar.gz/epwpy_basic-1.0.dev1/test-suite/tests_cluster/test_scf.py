import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest

def test_scf():
    benchmark=-16.87986980
    cwd=os.getcwd()

    QE=cwd+'/build/q-e/bin'
    system = 'scf'
    silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np', system = system)
    silicon.run_serial=True 
 
    silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')

    cwd=os.getcwd()
   
    tot_energy=extract_total_energy(cwd+f'/{system}/scf/scf.out')
    T_F=match_benchmark(benchmark,tot_energy,thr=1E-3)
    if(T_F == False):
        print('difference in benchmark data',abs(tot_energy-benchmark))
        print('QE run data',abs(tot_energy))

    assert(T_F)==True



