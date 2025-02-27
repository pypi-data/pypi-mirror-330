import os
import sys
import subprocess
sys.path.insert(0,str(os.getcwd())+'/../')
print(str(os.getcwd())+'../EPWpy/')
from EPWpy import EPWpy
from EPWpy import *
from test_extract import *
import pytest
    

def test_ZG():

    benchmark= 0.007751
    cwd=os.getcwd()
#    QE='/home1/07369/mzach/codes/q-e_dev_2024/bin/'
    QE=cwd+'/build/q-e/bin'  # path_to_qe/bin 
    prefix = 'ZG_si'
    T = 300
    dim1=3
    dim2=3
    dim3=3
    flfrc='\'ZG_si.fc\''
# prepare input
    silicon=EPWpy.EPWpy({'prefix':f'\'{prefix}\'','structure':'silicon.poscar','pseudo_auto': True,'ecutwfc':20,'ecutrho':80,'verbosity':'\'high\''},
            code=QE,env='mpirun --allow-run-as-root -np', system = prefix)
#   scf
    silicon.run_serial=True
    silicon.scf(electrons={'conv_thr':'1E-11'},
                kpoints={'kpoints':[[3,3,3]]},
                control = {'calculation':'\'scf\''})
    silicon.prepare(1,type_run='scf')
    silicon.run(1,'scf')
    silicon.ph(phonons={'nq1':2,'nq2':2,'nq3':2,'fildvscf':'\' \''})
    silicon.prepare(1,type_run='ph')
    silicon.run(1,type_run='ph')
#   q2r
    silicon.q2r(q2r={'fildyn':'\''+str(prefix)+'.dyn\'',
                 'flfrc':flfrc,
                 'zasr':'\'crystal\''})
    silicon.prepare(1,type_run='q2r')
    silicon.run(1,type_run='q2r')
#   ZG
    silicon.zg(zg={'flfrc':flfrc,'T':T,'dim1':dim1,'dim2':dim2,'dim3':dim3,'error_thresh':'0.2','niters':'4000'},azg={})
    silicon.prepare(1,type_run='zg')
    silicon.run(1,type_run='zg')
#   Benchmark
    os.chdir('./'+str(prefix)+'/zg/')
#
    command = f"grep 'Exact' zg.out | tail -1 | awk '{{print $3}}'"
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    print(output)
    Ex_anis_displ = float(output.stdout.strip())
    print("Exact Anisotropic Displacmenet Tensor:", Ex_anis_displ)
    T_F=match_benchmark(benchmark,Ex_anis_displ,thr=3E-3)
    if(T_F == False):
        print('difference in benchmark data',abs(Ex_anis_displ-benchmark))
        print('ZG run data (exact)',abs(Ex_anis_displ))
    assert(T_F)==True
#
#   Benchmark: Check the ZG anisotropic displacement tensor vs exact value
    command = f"grep 'ZG_conf' zg.out | tail -1 | awk '{{print $3}}'"
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    
    ZG_anis_displ = float(output.stdout.strip())
    print("ZG Anisotropic Displacmenet Tensor:", ZG_anis_displ)
    T_F=match_benchmark(Ex_anis_displ,ZG_anis_displ,thr=5E-2)
    if(T_F == False):
        print('difference between exact and ZG data',abs(Ex_anis_displ-ZG_anis_displ))
        print('ZG run data',abs(ZG_anis_displ))
    assert(T_F)==True
