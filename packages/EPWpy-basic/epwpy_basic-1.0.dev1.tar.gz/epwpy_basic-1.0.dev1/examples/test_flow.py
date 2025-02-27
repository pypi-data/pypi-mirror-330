#%autoreload 2
import matplotlib.pyplot as plt
from matplotlib import rc
from alive_progress import *
import time
import sys
import numpy as np
import math
import os
import subprocess
sys.path.insert(0,str(os.getcwd())+'/../')
#sys.path.insert(0,str(os.getcwd())+'/../EPWpy/plotting/')
import EPWpy
from EPWpy import EPWpy
from EPWpy.plotting import plot_bands
from EPWpy.QE.PW_util import *

####Constants########
nr=3.3
hbar=6.6*10**-16
c=3*10**10
font=16

folder='./'
cores='4'
prefix='si'
pseudo='/workspace/Sabya/codes/EPW_py/TACC/notebook_epw_bgw/notebooks_basic/pseudos'
######Define the directory of installation##############
QE = '/workspace/Sabya/beast_mnt/codes/EPW_develop/q-e/bin'
########################################################

silicon=EPWpy.EPWpy({'prefix':prefix,'restart_mode':'\'from_scratch\'','ibrav':2,'nat':2,'calculation':'\'scf\'',
                  'atomic_species':['Si'],'mass':[28.0855],
                  'atoms':['Si','Si'],'ntyp':1,'pseudo':['Si.upf'],'ecutwfc':'40','ecutrho':'160',
                  'celldm(1)':'10.262','verbosity':'high','pseudo_auto':True,                 
                 },env='mpirun')

silicon.run_serial = True

silicon.scf(control={'calculation':'\'scf\''},
            electrons={'conv_thr':'1E-13'},
            kpoints={'kpoints':[[3,3,3]],'kpoints_type':'automatic'},name='scf')

silicon.ph(phonons={'fildyn':'\'si.dyn\'',
                    'nq1':2,
                    'nq2':2,
                    'nq3':2,
                    'fildvscf':'\'dvscf\''})

silicon.nscf(system={'nbnd':12},
             kpoints={'grid':[4,4,4],'kpoints_type': 'crystal'})

silicon.dont_do = ['ph']#,'epw1']

silicon.epw(epwin={'wdata':['guiding_centres = .true.',
                            'dis_num_iter = 500',
                            'num_print_cycles  = 10',
                            'dis_mix_ratio = 1',
                            'use_ws_distance = T'],
                            'proj':['\'Si : sp3\''],
                            'etf_mem':1,
                            'num_iter':500,
                            'band_plot':'.true.',
                            'ncarrier':'1E14',
                            'fsthick':2.0,
                            'nkf1':10,
                            'nkf2':10,
                            'nkf3':10,
                            'nqf1':10,
                            'nqf2':10,
                            'nqf3':10,
                            'calc_nelec_wann':'.false.'},name='epw1')

silicon.run(4,type_run='transport')
