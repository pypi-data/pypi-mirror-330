import numpy as np
import os
import sys
sys.path.insert(0,str(os.getcwd())+'/../EPWpy/')
print(str(os.getcwd())+'../EPWpy/')
from EPWpy import *



QE='/workspace/Sabya/codes/q-e_fix/bin'
QE='/workspace/Sabya/codes/q-e_fix/bin'


silicon=EPWpy({'prefix':'\'si\'',
               'pseudo_auto': True,
               'ecutwfc':40,
               'ecutrho':160,
               'verbosity':'\'high\'',
               'lattice_vector':np.array([[0.00000000000000, 2.23203165901699, 2.23203165901699],
                                       [2.23203165901699, 0.00000000000000, 2.23203165901699],
                                       [2.23203165901699, 2.23203165901699, 0.00000000000000]]),
               'atomic_pos':np.array([[0.00000000000000,0.00000000000000, 0.00000000000000],     
                                     [0.25000000000000, 0.25000000000000, 0.25000000000000]]),
               'cell_type': 'angstrom',
               'atoms':['Si','Si'],'mass':[28.08], 'atomic_species':['Si']},
               code=QE,env='mpirun')





for key in silicon.pw_atomic_positions:
    print(key,silicon.pw_atomic_positions[key])

silicon.pw_atomic_positions['atomic_pos'] +=np.array([[0.001,0.0,0.0],[0.0,0.001,0.0]])

for key in silicon.pw_atomic_positions:
    print('updated atomic attributes:', key,silicon.pw_atomic_positions[key])



for key in silicon.pw_cell_parameters:
    print(key,silicon.pw_cell_parameters[key])


#silicon.ph()

#

silicon.scf(electrons={'conv_thr':'1E-11'},kpoints={'kpoints':[[3,3,3]]})
silicon.prepare(4,type_run='scf')
silicon.run_serial=True
silicon.run(4,'scf')
silicon.file='si/scf/scf.out'
silicon.get_QE_status()

"""
silicon.file='si/scf/scf.out'

silicon.get_QE_status()

silicon.ph(phonons={'fildyn':'\'si.dyn\'',
                    'nq1':2,
                    'nq2':2,
                    'nq3':2,
                    'fildvscf':'\'dvscf\''})
silicon.prepare(4,type_run='ph')
#silicon.run(4,'ph')
silicon.file='si/ph/ph.out'

silicon.get_QE_status()




silicon.nscf(control={'calculation':'bands'},kpoints={'grid':[4,4,4],'kpoints_type':'crystal'},system={'nbnd':20})
silicon.prepare(4,type_run='nscf')
silicon.run_serial=True
#silicon.run(4,'nscf')
silicon.file='si/nscf/nscf.out'
silicon.get_QE_status()



silicon.epw(epwin={'wdata':['\'guiding_centres = .true.\'',
                            '\'dis_num_iter = 500\'',
                            '\'num_print_cycles  = 10\'',
                            '\'dis_mix_ratio = 1\'',
                            '\'use_ws_distance = T\''],
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
#silicon.prefix='si'
silicon.filkf(path=[[0.5,0.5,0.5],
        [0,0,0],[0.5,0.5,0.5]],length=[51,51],name='LGX.txt')
silicon.prepare(20,type_run='epw1')
#silicon.run(20,'epw1')
silicon.file='si/epw/epw1.out'
silicon.get_EPW_status()


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
                   'nkf1':8,
                   'nkf2':8,
                   'nkf3':8,
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
silicon.prepare(20,type_run='epw2')
#silicon.run(20,type_run='epw2')

silicon.file='si/epw/epw2.out'
silicon.get_EPW_status()
"""
#silicon.code='/workspace/Sabya/codes/BGW/BerkeleyGW-3.1.0/bin'

#silicon.GW(GW={'nbnd':20})

#silicon.epsilon(epsilon={'restart':' ', 'degeneracy_check_override':' '})
#silicon.run(16,'GW')

#silicon.run(16,'epsilon')
#

#silicon.sigma(sigma={'band_index_min': 4,'band_index_max':12})

#silicon.code='/workspace/Sabya/codes/BGW/BerkeleyGW-3.1.0/bin'
#

#silicon.run(16,'epsilon')
#silicon.run(16,'sigma')


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




