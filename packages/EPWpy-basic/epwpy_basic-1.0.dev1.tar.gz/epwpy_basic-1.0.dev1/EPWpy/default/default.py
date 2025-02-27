####################################default values ###########################################
import numpy as np

pw_control={'calculation': '\'scf\'','verbosity':'\'low\'', 
   'restart_mode':'\'from_scratch\'','outdir': '\'./\'',
   'pseudo_dir':'\'./\'','prefix':'\'si\''}

pw_system={'ibrav':2,'celldm(1)':10.8,'celldm(2)':None,'celldm(3)':None, 'nat':2,'ntyp': 1,
                   'ecutwfc':None,'ecutrho':None,
                   'occupations':None, 'smearing':None, 'degauss':None}



pw_electrons={'conv_thr':'1E-12','diagonalization':'\'david\'' }
pw_ions={'ion_dynamics':'\'bfgs\''}
pw_cell={'cell_dynamics':'\'bfgs\'','press':0.0}
pw_bands={'prefix':'\'si\'',
                  'outdir':pw_control['outdir'],
                   'filband': '\'bands.dat\'',
                   'lsym': '.false.'}
nscf_supercond={'prefix':'\'si\'',
            'outdir':pw_control['outdir'],
            'filband': '\'bands.dat\''}

iondynamics=False
celldynamics=False
pw_atomic_species={'pseudo':[],'mass':[],'atomic_species':[]}
atomic_pos=np.zeros((pw_system['nat'],3),dtype=float)
atomic_pos[0,:]=0.00
atomic_pos[1,:]=0.25    
kpoints=np.array([[6.0,6.0,6.0]])
shift=np.array([[0 ,0 ,0]])
atoms=np.array(['si','si'])

pw_atomic_positions={'num':pw_system['nat'],
   'atomic_pos':atomic_pos,'atoms':atoms,'atomic_position_type':'alat'} 

pw_kpoints={'kpoints_type':'automatic','shift':shift,'kpoints':kpoints}

pw_cell_parameters={'cell_type': 'alat', 'lattice_vector':np.array([['0.000 0.000 0.000'],
    ['0.000 0.000 0.00'],['0.000 0.000 0.000']])}

pw_system['nat']=len(pw_atomic_positions['atomic_pos'][:,0])
pw_system['ntyp']=len(pw_atomic_species['atomic_species'])
ph_params={'prefix':pw_control['prefix'],'fildyn': str(pw_control['prefix'])+'.dyn\'',
                'ldisp': '.true.','fildvscf':'\'dvscf\'','nq1':2,'nq2':2,'nq3':2,'tr2_ph':'1.0d-14'}

nk1=ph_params['nq1']
nk2=ph_params['nq2']
nk3=ph_params['nq3']
nq1=ph_params['nq3']
nq2=ph_params['nq3']
nq3=ph_params['nq3']

ph_qpoints ={}

epw_params={'prefix':pw_control['prefix'],'mass':pw_atomic_species['mass'],
        'outdir':pw_control['outdir'],'elph':'.true.','epbwrite':'.false.','epbread':'.false.',
        'epwwrite':'.true.','epwread':'.false.','etf_mem':1,'nbndsub':8,
        'use_ws':'.true.','wannierize':'.true.','num_iter':5000,'iprint': 2,'dis_win_max':None,'dis_froz_max':None,
        'fsthick':1.2, 'temps':1,'degaussw':0.005,'dvscf_dir':'\'./save\'','band_plot':'.false.','nk1': nk1,
        'nk2':nk2,'nk3':nk3,'nq1':nq1,'nq2':nq2,'nq3':nq3}
card_params = {}

q2r_params={'fildyn': '\'si.dyn\'','flfrc': '\'si.fc\'','zasr':'\'crystal\''}

zg_inputzg={'flfrc':'\'SPECIFY\'','asr':q2r_params['zasr'],
    'flscf':'\'scf.in\'','T':0.00,'dim1':3,'dim2':3,'dim3':3,'compute_error':'.true.','synch':'.true.','error_thresh':0.4,
    'niters':3000,'incl_qA':'.true.','ASDM':'.false.'}
zg_inputazg={}

eps_inputpp={'prefix':pw_control['prefix'],'outdir':pw_control['outdir'],'calculation':'\'eps\''}
eps_energy_grid={'smeartype':'\'gauss\'','intersmear':'0.03','wmin':'0.2','wmax':'4.5','nw':'600','shift':'0.0'}

wannier_params={'num_iter':100}
pw2wann_params={'outdir':'\'./\'','write_amn':'.true.','write_mmn':'.true.','write_unk':'.false.'}

BGW_init={'nbnd':100,'shift':[0.0,0.0,0.001],'grid_co':[6,6,6],'grid_fi':[6,6,6]}
BGW_epsilon={'frequency_dependence': 0,'epsilon_cutoff':25}
BGW_sigma={'screening_semiconductor': ' '}
BGW_kernel={'screening_semiconductor': ' '}
BGW_absorption={}
BGW_sig2wan={'spin':1,'eqp':1}
nbnd_BGW=BGW_init['nbnd']
BGW_pw2bgw={'real_or_complex':2,'wfng_flag':'.true.','wfng_file':'wfn.cplx','wfng_kgrid':'.true.','rhog_flag':'.true.','rhog_file':'rho.cplx',
                    'vxcg_flag':'.false.','vxcg_file':'vxc.cplx','vxc_flag':'.true.','vxc_file':'vxc.dat','vxc_diag_nmin': 1,'vxc_diag_nmax':nbnd_BGW,
                    'vxc_offdiag_nmin':0,'vxc_offdiag_nmax':0,'wfng_dk1':0,'wfng_dk2':0,'wfng_dk3':0}

matdyn_input={'asr': '\'crystal\'',
                      'mass':pw_atomic_species['mass'],
                      'flfrc':q2r_params['flfrc'],
                      'flfrq':str(pw_control['prefix'][:-1])+'.freq\'',
                      'q_in_band_form': '.true.',
                      'q_in_cryst_coord': '.true.',
                      'dos': '.false.'}
matdyn_kpoints={}

phdos_input={'asr': '\'crystal\'',
                      'mass':pw_atomic_species['mass'],
                      'flfrc':q2r_params['flfrc'],
                      'flfrq':str(pw_control['prefix'][:-1])+'.freq\'',
                      'dos': '.true.'}
abinit_params = {}

vasp_params = {'ENCUT':500, 'ISMEAR':0,'SIGMA':0.01,'PREC':'accurate'}
vasp_kpoint_params = {'len':0,'center':'Gamma','grid':['4 4 4']}

dos_input={'prefix':pw_control['prefix']}
pdos_input={'prefix':pw_control['prefix']}
cards = {}
