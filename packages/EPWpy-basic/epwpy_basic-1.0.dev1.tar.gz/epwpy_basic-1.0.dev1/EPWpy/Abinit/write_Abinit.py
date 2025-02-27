#
from __future__ import annotations
import numpy as np
import os
from EPWpy.utilities.check_util import datatyp
from EPWpy.structure.lattice import lattice

class write_Abinit_files:
    """
    ** This class performs QE file writing
    **
    ** This is mostly an internally used class
    and should not be called externally
    **
    """ 
    def __init__(self, abinit_params):

        self.control = abinit_params['control']
        self.cell = abinit_params['cell']
        self.atom = abinit_params['atom']
        self.band = abinit_params['band']
        self.kpoints = abinit_params['kpoints']
        
        self.electron = abinit_params['electron']
        self.pseudo = abinit_params['pseudo']
        self.common = abinit_params['common']

    def write_abi(self,name='scf'):
        forbidden_keys = ['ngkpt','shiftk',None,'pseudo']     
        with open(str(name)+'.abi','w') as f:


            for key in self.control.keys():
                if (self.control[key] != None):
                    f.write(str(key)+'  '+str(self.control[key]))
                    f.write('\n')

            
            f.write(f'acell {self.cell["acell"]}\n')
            f.write('rprim ')            
            for i in range(len(np.array(self.cell['rprim'])[:,0])):
                for j in range(len(np.array(self.cell['rprim'])[0,:])):
                    f.write(str(np.array(self.cell['rprim'])[i,j])+ '  ')
                f.write('\n')
                f.write('      ')            
            f.write('\n')
            
            f.write(f'ntypat {self.atom["ntypat"]}\n')
            f.write(f'znucl ')
            for i in range(len(self.atom['znucl'])): 
                f.write(str(self.atom['znucl'][i]))
                f.write(' ')
            f.write('\n')

            f.write(f'natom {self.atom["natom"]}\n') 
            f.write('typat ')
            for i in range(len(self.atom['typat'])): 
                f.write(str(self.atom['typat'][i]))
                f.write(' ')
            f.write('\n')

            f.write(f'{self.atom["type"]} \n')
            f.write('    ')
            for i in range(len(self.atom["atomic_pos"][:,0])):
                for j in range(3):
                    f.write(str(self.atom["atomic_pos"][i,j]))
                    f.write(' ')
                f.write('\n')
                f.write('        ')

            for key in self.band.keys():
                if (self.band[key] != None):
                    f.write(str(key)+'  '+str(self.band[key]))
                    f.write('\n')
            
            f.write(f'ngkpt {self.kpoints["ngkpt"]}\n')
            for key in self.kpoints.keys():
                if (key not in forbidden_keys):
                    if (self.kpoint[key] != None):
                        f.write(str(key)+'  '+str(self.kpoints[key]))
                        f.write('\n')
    
            if ('shiftk' in self.kpoints.keys()):
                f.write(f'shiftk ')
                for i in range(len(self.kpoints["shiftk"][:,0])):
                    for j in range(3):
                        f.write(self.kpoints["shiftk"][i,j])
                        f.write(' ')
                    f.write('\n')
                    f.write('       ')

            for key in self.electron.keys():
                if (self.electron[key] != None):
                    f.write(str(key)+'  '+str(self.electron[key]))
                    f.write('\n')

            for key in self.common.keys():
                if (datatyp(self.common[key]) == 'array'):
                    f.write(f'{key} ')
                    for i in range(len(self.common[key][:,0])):
                        for j in range(len(self.common[key][0,:])):
                            f.write(str(self.common[key][i,j]))
                            f.write(' ')
                        f.write('\n')
                        f.write('       ')
                    f.write('\n')
                else:
                    f.write(str(key)+'  '+str(self.common[key]))
                    f.write('\n')

            for key in self.pseudo.keys():
                if (key not in forbidden_keys):
                    data = self.pseudo[key]
                    f.write(f'{key} \"{data}\"')
                    f.write('\n') 
  
            f.write('pseudos \"') 
            for i in range(int(self.atom['ntypat'])):
                f.write(' ')
                f.write(self.pseudo['pseudo'][i])
            f.write(' \"')
                              
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

