import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../')
import EPWpy
from EPWpy import EPWpy
from EPWpy.Abinit.EPWpy_Abinit import py_Abinit
from EPWpy.Abinit.Abinit_util import *
from EPWpy.utilities import k_gen


QE='/workspace/Sabya/codes/q-e_fix/bin'
QE='/workspace/Sabya/codes/q-e_fix/bin'


silicon=EPWpy.EPWpy({'prefix':'\'si\'','structure_mp':"mp-149",'pseudo_auto': True,'ecutwfc':40,'ecutrho':160,'verbosity':'\'high\''},
        code=QE,env='mpirun')

silicon.pseudo_auto = True

silicon.abinit = py_Abinit(silicon,code = '/workspace/Sabya/Abinit/abinit/build3/src/98_main/',env='mpirun')

silicon.abinit.abi({'quadrupole':None,'common':{'pp_dirpath':'/workspace/Sabya/codes/EPW_py/TACC/EPWpy_develop/notebook_epw_bgw/examples/pseudo',
                                      'pseudo':['14si.fhi'],
                                      'nshiftk':4,
                                      'shiftk':np.array([[0.5,0.5,0.5],[0.5,0.0,0.0],[0.0,0.5,0.0],[0.0,0.0,0.5]])}},name='input')
silicon.abinit.prefix = 'blank'
silicon.abinit.pseudo = 'blank'
silicon.abinit.prepare(type_run = 'abinit',infile='input.abi')
#silicon.abinit.run(4,type_run = 'abinit',infile = 'input')
silicon.abinit.util = Abinit_utilities(folder = 'si/abinit',file='input')
silicon.abinit.util.quadrupole()

"""
silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
#silicon.prepare(4,type_run='scf')
silicon.run_serial=True
#silicon.run(4,'scf')

silicon.file='si/scf/scf.out'

silicon.get_QE_status()
#silicon.filkf(path=[[0.5,0.5,0.5],
 #       [0,0,0],[0.5,0.5,0.5]],length=[51,51],name='LGX.txt')
#
K=[[0.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.5, 0.25, 0.75]]
kx=[1,0,0]
ky=[0,1,0]
kz=[0,0,1]
leng=[11,11]
K=k_gen.k_path(K,leng,kx,ky,kz)
silicon.ph_qpoints['qpoints']=K

silicon.ph(phonons={'fildyn':'\'si.dyn\'',
                    'nq1':2,
                    'nq2':2,
                    'nq3':2,
                    'fildvscf':'\'dvscf\''},qpoints = {'nqs':22})
silicon.prepare(4,type_run='ph')
#silicon.run(4,'ph')
silicon.file='si/ph/ph.out'

silicon.ph_util = silicon.PH_utilities()
silicon.ph_util.file = 'si/ph/ph.out'

print(silicon.ph_util.eps_ph)
print(silicon.ph_util.qpoints)

silicon.get_QE_status()


silicon.nscf_file='nscf'

silicon.nscf(control={'calculation':'bands'}, kpoints={'grid':[4,4,4],'kpoints_type':'crystal'},system={'nbnd':20})
#silicon.prepare(4,type_run='nscf')
silicon.run_serial=True
#silicon.run(4,'nscf')
silicon.file='si/nscf/nscf.out'
silicon.get_QE_status()

"""
"""
silicon.epw(epwin={'wdata':['\'guiding_centres = .true.\'',
                            '\'dis_num_iter = 500\'',
                            '\'num_print_cycles  = 10\'',
                            '\'dis_mix_ratio = 1\'',
                            '\'use_ws_distance = T\''],
                            'dis_win_max':18,
                            'dis_froz_max':2,
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

#silicon.filkf(path=[[0.5,0.5,0.5],
 #       [0,0,0],[0.5,0.5,0.5]],length=[51,51],name='LGX.txt')
#silicon.prepare(20,type_run='epw1')
#silicon.run(20,'epw1')
silicon.file='si/epw/epw1.out'
silicon.get_EPW_status()

#silicon.env = 'mpirun'

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
                   'nkf1':4,
                   'nkf2':4,
                   'nkf3':4,
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
                   'nq3':2,
                   'refresh': None},
            name='epw2')
"""
silicon.prepare(20,type_run='epw2')
silicon.run(4,type_run='epw2')

silicon.file='si/epw/epw2.out'

silicon.get_EPW_status()

###### GW Calculation #######
silicon.code='/workspace/Sabya/codes/BGW/BerkeleyGW-3.1.0/bin'
"""
silicon.GW(GW={'nbnd':20})
#silicon.run(16,'GW')

silicon.epsilon(epsilon={'restart':' ', 'degeneracy_check_override':' '})
#silicon.run(16,'epsilon')


silicon.sigma(sigma={'band_index_min': 4,'band_index_max':12})
#silicon.run(16,'sigma')
"""
#silicon.code='/workspace/Sabya/codes/BGW/BerkeleyGW-3.1.0/bin'
#

#silicon.run(16,'epsilon')


#Pb=EPW_py({'nat':1,'calculation':'scf','atomic_species':['pb'],'pseudo':['pb_s.UPF'],'mass':[207.2],'atoms':['pb'],'ntyp':1,'ibrav':2,'celldm(1)':9.27,'ecutwfc':30.0,
 #       'occupations':'smearing','smearing':'mp','degauss':0.025,'atomic_pos':np.array([[0.0,0.0,0.0]])},system='pb')



#silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
#silicon.prepare_scf()
#silicon.run(4)

#Pb.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
#Ge.prep_scf()
#silicon.ph()

#silicon.run(4,type_run='ph')

#silicon.write_q2r(q2r={'fildyn':'si.dyn','flfrc':'si.fc','zasr':'simple'},name='q2r')

#silicon.nscf(kpoints={'grid':[6,6,6],'type': 'crystal'})
#silicon.run(4,type_run='nscf')


#silicon.epw(epwin={'wdata':['\'bands_plot = .true.\'','\'begin kpoint_path\'','L 0.50 0.00 0.00 G 0.0','G 0.00 0.00 0.00 X 0.5',
#    'end kpoint_path','bands_plot_format = gn','guiding_centres = .true.','dis_num_iter      = 50',
#    'num_print_cycles  = 10','dis_mix_ratio     = 1','use_ws_distance = T']},name='epw1')
#silicon.run(4,type_run='epw1')


#silicon.epw(epwin={'wannierize': '.false.','indabs':'.true.','nkf1':6,'nkf2':6,'nkf3':6},name='epw2',)

#silicon.run(4,type_run='epw2')




