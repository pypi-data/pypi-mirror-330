#
from __future__ import annotations
import numpy as np
import os
from EPWpy.utilities.check_util import datatyp

class write_QE_files:
    """
    ** This class performs QE file writing
    **
    ** This is mostly an internally used class
    and should not be called externally
    **
    """ 
    def __init__(self,write):

        self.write=write
    
    def write_scf(self,name='scf'):
     
        with open(str(name)+'.in','w') as f:

            f.write('&CONTROL\n')

            for key in self.pw_control.keys():
                if (self.pw_control[key] != None):
                    f.write(str(key)+' = '+str(self.pw_control[key]))
                    f.write('\n')

            f.write('/\n')
            f.write('&SYSTEM\n')
            for key in self.pw_system.keys():
                if(self.pw_system[key] != None):
                    f.write(str(key)+' = '+str(self.pw_system[key]))
                    f.write('\n')
                if (str(key) == 'ecutwfc') and (self.pw_system['ecutwfc'] == None):
                    f.write(str(key)+' = '+str(self.get_ecutwfc()))
                    f.write('\n')
            f.write('/\n')

            f.write('&ELECTRONS\n')
            for key in self.pw_electrons.keys():
                if (self.pw_electrons[key] !=None):
                    f.write(str(key)+' = '+str(self.pw_electrons[key]))
                    f.write('\n')
            f.write('/\n')
 
            if(self.iondynamics==True):
                f.write('&IONS\n') 
                for key in self.pw_ions.keys():
                    if (self.pw_ions[key] !=None):
                        f.write(str(key)+' = '+str(self.pw_ions[key]))
                        f.write('\n')
                f.write('/\n')
            if(self.celldynamics==True):
                f.write('&CELL\n') 
                for key in self.pw_cell.keys():
                    if (self.pw_cell[key] != None):
                        f.write(str(key)+' = '+str(self.pw_cell[key]))
                        f.write('\n')
                f.write('/\n')
            f.write('ATOMIC_SPECIES\n')
            for i in range(len(self.pw_atomic_species['atomic_species'])):
                f.write(self.pw_atomic_species['atomic_species'][i])
                f.write(' ')                
                f.write(str(self.pw_atomic_species['mass'][i]))
                f.write(' ')                
                f.write(self.pw_atomic_species['pseudo'][i])
                f.write(' ')                
                f.write('\n')
 
            f.write('ATOMIC_POSITIONS ')
            f.write(self.pw_atomic_positions['atomic_position_type'])
            f.write('\n')

            for i in range(len(self.pw_atomic_positions['atoms'])):#self.default_pw_atomic_positions['num']):
                f.write(self.pw_atomic_positions['atoms'][i])
                f.write(' ')
                for j in range(3):
                    f.write(str((self.pw_atomic_positions['atomic_pos'][i,j])))
                    f.write(' ')
                f.write('\n')
            f.write('\n')

            f.write('K_POINTS ')
            f.write(self.pw_kpoints['kpoints_type'])
            if(self.pw_kpoints['kpoints_type']!='automatic'):
                f.write('\n')
                f.write(' ')
                f.write(str(len(self.pw_kpoints['kpoints'])))

            f.write('\n')
            for i in range(len(self.pw_kpoints['kpoints'])):
                for j in range(len(np.array(self.pw_kpoints['kpoints'])[i,:])):
                    f.write(str(np.array(self.pw_kpoints['kpoints'])[i,j]))
                    f.write(' ')
                if(self.pw_kpoints['kpoints_type']=='automatic'):
                    for j in range(3):
                        f.write(str(np.array(self.pw_kpoints['shift'])[i,j]))
                        f.write(' ')

                f.write('\n')
            f.write('\n')
            if(int(self.pw_system['ibrav'])==0):
                f.write('CELL_PARAMETERS ')
                f.write(self.pw_cell_parameters['cell_type']+'\n')
                for i in range(len(np.array(self.pw_cell_parameters['lattice_vector'])[:,0])):
                    for j in range(len(np.array(self.pw_cell_parameters['lattice_vector'])[0,:])):

                        f.write(str(np.array(self.pw_cell_parameters['lattice_vector'])[i,j])+ '  ')
                    f.write('\n')
            if (len(self.card_params) != 0):
                 for card in self.card_params:
                    f.write(card)
                    f.write('\n')
                    for key in self.card_params[card].keys():
                        f.write(str(key)+' '+str(self.card_params[card][key]))
                        f.write('\n')
                        
        f.close()

    def write_ph(self, name='ph'):
        prefix=self.prefix.replace('\'','')
        self.ph_params['fildyn']='\''+str(prefix)+'.dyn\''
        with open(str(name)+'.in','w') as f:
            f.write('&inputph\n')
            for key in self.ph_params.keys():
                f.write(str(key)+' = '+str(self.ph_params[key]))
                f.write('\n')
            f.write('\n')
            f.write('/\n')
            if (len(self.ph_qpoints) != 0):
                nqs = self.ph_qpoints['nqs']
                f.write(f'{nqs}\n')
                for i in range(len(self.ph_qpoints['qpoints'])):
                    for j in range(len(np.array(self.ph_qpoints['qpoints'])[i,:])):
                        f.write(str(np.array(self.ph_qpoints['qpoints'])[i,j]))
                        f.write(' ')
 
                    f.write('\n')
        f.close()

    def write_q2r(self, name='q2r'):

        with open(str(name)+'.in','w') as f:
            f.write('&input\n')
            for key in self.q2r_params.keys():
                f.write(str(key)+' = '+str(self.q2r_params[key]))
                f.write('\n')
            f.write('/')            
        f.close()

    def write_bands(self,bands={},name='bands'):
        with open(str(name)+'.in','w') as f:

            f.write('&BANDS\n')
            for key in self.pw_bands.keys():
                if(key not in bands.keys()):
                    f.write(str(key)+' = '+str(self.pw_bands[key]))
                    f.write('\n')
            for key in bands.keys():
                    f.write(str(key)+' = '+str(bands[key]))
                    f.write('\n')
            f.write('/')
            
    def write_nscf2supercond(self,nscf2supercond={},name='nscf2supercond'):
        with open(str(name)+'.in','w') as f:

            f.write('&BANDS\n')
            for key in self.nscf_supercond.keys():
                if(key not in nscf2supercond.keys()):
                    f.write(str(key)+' = '+str(self.nscf_supercond[key]))
                    f.write('\n')
            for key in nscf2supercond.keys():
                    f.write(str(key)+' = '+str(nscf2supercond[key]))
                    f.write('\n')
            f.write('/')
            
    def write_matdyn(self,matdyn={},name='matdyn'):
        with open(str(name)+'.in','w') as f:

            f.write('&input\n')
            for key in self.matdyn_input.keys():
                if (key not in matdyn.keys()):
                    if(key=='mass'):
                        for i in range(len(self.matdyn_input[key])):
                            f.write('amass('+str(i+1)+') = '+str(self.matdyn_input[key][i]))
                            f.write('\n')
                    else:
                        f.write(str(key)+' = '+str(self.matdyn_input[key]))
                        f.write('\n')
            for key in matdyn.keys():
                    f.write(str(key)+' = '+str(matdyn[key]))
                    f.write('\n')

            f.write('/\n')

            if ('dos' not in matdyn or matdyn['dos'] == '.false.'):
                f.write(str(len(self.matdyn_kpoints['kpoints'])))
                f.write('\n')
                for i in range(len(self.matdyn_kpoints['kpoints'])):
                    for j in range(len(np.array(self.matdyn_kpoints['kpoints'])[i,:])):
                        f.write(str(np.array(self.matdyn_kpoints['kpoints'])[i,j]))
                        f.write(' ')
                    f.write('\n')
        f.close()
        
        
    def write_phdos(self,phdos={},name='phdos'):
        with open(str(name)+'.in','w') as f:
            f.write('&input\n')
            for key in self.phdos_input.keys():
                if (key not in phdos.keys()):
                    if(key=='mass'):
                        for i in range(len(self.phdos_input[key])):
                            f.write('amass('+str(i+1)+') = '+str(self.phdos_input[key][i]))
                            f.write('\n')
                    else:
                        f.write(str(key)+' = '+str(self.phdos_input[key]))
                        f.write('\n')
            for key in phdos.keys():
                    f.write(str(key)+' = '+str(phdos[key]))
                    f.write('\n')

            f.write('/\n')
        f.close()

    def write_dos(self, dos={}, name='dos'):
        with open(str(name)+'.in','w') as f:
            f.write('&dos\n')
            for key in self.dos_input.keys():
                if (key not in dos.keys()):
                    f.write(str(key)+' = '+str(self.dos_input[key]))
                    f.write('\n')
            for key in dos.keys():
                    f.write(str(key)+' = '+str(dos[key]))
                    f.write('\n')

            f.write('/\n')
        f.close()
        
    def write_pdos(self, pdos={}, name='pdos'):
        with open(str(name)+'.in','w') as f:
            f.write('&projwfc\n')
            for key in self.pdos_input.keys():
                if (key not in pdos.keys()):
                    f.write(str(key)+' = '+str(self.pdos_input[key]))
                    f.write('\n')
            for key in pdos.keys():
                    f.write(str(key)+' = '+str(pdos[key]))
                    f.write('\n')

            f.write('/\n')
        f.close()

    def write_matdyn(self,matdyn={},name='matdyn'):
        with open(str(name)+'.in','w') as f:

            f.write('&input\n')
            for key in self.matdyn_input.keys():
                if (key not in matdyn.keys()):
                    if(key=='mass'):
                        for i in range(len(self.matdyn_input[key])):
                            f.write('amass('+str(i+1)+') = '+str(self.matdyn_input[key][i]))
                            f.write('\n')
                    else:
                        f.write(str(key)+' = '+str(self.matdyn_input[key]))
                        f.write('\n')
            for key in matdyn.keys():
                    f.write(str(key)+' = '+str(matdyn[key]))
                    f.write('\n')

            f.write('/\n')

            if ('dos' not in matdyn or matdyn['dos'] == '.false.'):
                f.write(str(len(self.matdyn_kpoints['kpoints'])))
                f.write('\n')
                for i in range(len(self.matdyn_kpoints['kpoints'])):
                    for j in range(len(np.array(self.matdyn_kpoints['kpoints'])[i,:])):
                        f.write(str(np.array(self.matdyn_kpoints['kpoints'])[i,j]))
                        f.write(' ')
                    f.write('\n')
        f.close()
        
        
    def write_phdos(self,phdos={},name='phdos'):
        with open(str(name)+'.in','w') as f:
            f.write('&input\n')
            for key in self.phdos_input.keys():
                if (key not in phdos.keys()):
                    if(key=='mass'):
                        for i in range(len(self.phdos_input[key])):
                            f.write('amass('+str(i+1)+') = '+str(self.phdos_input[key][i]))
                            f.write('\n')
                    else:
                        f.write(str(key)+' = '+str(self.phdos_input[key]))
                        f.write('\n')
            for key in phdos.keys():
                    f.write(str(key)+' = '+str(phdos[key]))
                    f.write('\n')

            f.write('/\n')
        f.close()

    def write_dos(self, dos={}, name='dos'):
        with open(str(name)+'.in','w') as f:
            f.write('&dos\n')
            for key in self.dos_input.keys():
                if (key not in dos.keys()):
                    f.write(str(key)+' = '+str(self.dos_input[key]))
                    f.write('\n')
            for key in dos.keys():
                    f.write(str(key)+' = '+str(dos[key]))
                    f.write('\n')

            f.write('/\n')
        f.close()
        
    def write_pdos(self, pdos={}, name='pdos'):
        with open(str(name)+'.in','w') as f:
            f.write('&projwfc\n')
            for key in self.pdos_input.keys():
                if (key not in pdos.keys()):
                    f.write(str(key)+' = '+str(self.pdos_input[key]))
                    f.write('\n')
            for key in pdos.keys():
                    f.write(str(key)+' = '+str(pdos[key]))
                    f.write('\n')

            f.write('/\n')
        f.close()

    def write_zg(self, name='zg'):
        with open(str(name)+'.in','w') as f:

            f.write('&input\n')
            for key in self.zg_inputzg.keys():
                f.write(str(key)+' = '+str(self.zg_inputzg[key]))
                f.write('\n')
            f.write('/\n')
            if (len(self.zg_inputazg) > 0):
                f.write('&A_ZG\n')
                for key in self.zg_inputazg.keys():
                    f.write(str(key)+' = '+str(self.zg_inputazg[key]))
                    f.write('\n')
                f.write('/')

        f.close()

    def write_eps(self, name='eps'):
        with open(str(name)+'.in','w') as f:

            f.write('&inputpp\n')
            for key in self.eps_inputpp.keys():
                f.write(str(key)+' = '+str(self.eps_inputpp[key]))
                f.write('\n')
            f.write('/\n')
            f.write('&energy_grid\n')
            for key in self.eps_energy_grid.keys():
                f.write(str(key)+' = '+str(self.eps_energy_grid[key]))
                f.write('\n')
            f.write('/')

        f.close()

    def write_epw(self, name='epw'):
#        print(os.getcwd(),name)        
        with open(str(name)+'.in', 'w') as f:
            f.write('&inputepw')
            f.write('\n')
 
            for key in self.epw_params.keys():
                if (datatyp(self.epw_params[key]) != None):
                    if (key == 'mass'):
                        for i in range(len(self.epw_params[key])):
                            f.write('amass('+str(i+1)+') = '+str(self.epw_params[key][i]))
                            f.write('\n')

                    elif (key == 'wdata'):
                        for i in range(len(self.epw_params[key])):
                            f.write(f'wdata({i+1}) = ')
                            f.write(f'\'{self.epw_params[key][i]}\'')
                            f.write('\n')

                    elif (key == 'proj'):
                        for i in range(len(self.epw_params[key])):
                            f.write('proj('+str(i+1)+') = '+self.epw_params[key][i])
                            f.write('\n')
                    else:
                        if (self.epw_params[key] !=None):
                            f.write(str(key)+' = '+str(self.epw_params[key]))
                            f.write('\n')
                #else:

                 #   print(datatyp(self.epw_params[key]), key, self.epw_params[key], type(self.epw_params[key]))
            f.write('/\n')
        f.close()

    def write_wann(self, name='.win'):
        prefix=self.prefix.replace('\'','')
        with open(prefix+'.'+name,'w') as f:
            for key in self.wannier_params.keys():
                if(key == 'projections'):
                    if(self.wannier_params['projections'] !='auto_projections'):
                        f.write('begin projections\n')
                        for proj in self.wannier_params['projections']:
                            for data in (np.array(proj).astype(str)):
                                f.write(str(data)+' ')
                            f.write('\n')
                        f.write('end projections\n')
                    else:
                        f.write('projections = auto_projections')    
                        self.wannier_params['scdm_proj']='.true.'
 
                elif(key == 'atomic_positions'):
                    f.write('begin atoms_frac\n')
                    for i in range(len(self.wannier_params['atomic_positions'][:,0])):
                        f.write(self.pw_atomic_positions['atoms'][i]+' ')
                        for j in range(3):
                            f.write(str(self.wannier_params['atomic_positions'][i,j])+' ')
                        f.write('\n')
                    f.write('end atoms_frac\n\n')
                elif(key == 'kpoints'):
                    f.write('mp_grid : ')
                
                    for nk in self.grid:
                        f.write(str(nk)+' ')
                    f.write('\n')
                    f.write('begin kpoints\n')
                    self.k = np.array(self.k)
                    for l in range(len(self.k[:,0])):
                        for j in self.k[l,:3]:
                            f.write(str(j)+' ')
                        f.write('\n')
                    f.write('end kpoints\n\n')
                elif(key == 'cell_parameters'):
                    f.write('begin unit_cell_cart\n') 
                    for i in range(len(self.wannier_params['cell_parameters'][:,0])):
                        for j in (self.wannier_params['cell_parameters'][i,:]):           
                            f.write(str(j) + ' ')
                        f.write('\n')
                    f.write('end unit_cell_cart\n')
                elif(key == 'string'):
                    for string in self.wannier_params[key]: 
                        f.write(str(string)+'\n')

                else:
                    f.write(str(key)+' = '+str(self.wannier_params[key]))
                f.write('\n')
        f.close()
        with open(prefix+'.pw2wan','w') as f:
            f.write('&inputpp\n')
            f.write('prefix = '+str(self.prefix))
            f.write('\n') 
            for key in self.pw2wann_params:
                f.write(str(key)+' = '+str(self.pw2wann_params[key]))
                f.write('\n')
            f.write('/')

