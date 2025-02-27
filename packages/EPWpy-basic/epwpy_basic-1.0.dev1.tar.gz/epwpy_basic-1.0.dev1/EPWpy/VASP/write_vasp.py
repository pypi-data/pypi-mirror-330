#
from __future__ import annotations
import numpy as np
import os
from EPWpy.utilities.check_util import datatyp
from EPWpy.structure.lattice import lattice

class write_vasp_files:
    """
    ** This class performs VASP file writing
    **
    ** This is mostly an internally used class
    and should not be called externally
    **
    """ 
    def __init__(self, incar_params, kpoint_params):

        self.vasp_params = incar_params
        self.vasp_kpoint_params = kpoint_params


    def write_INCAR(self,name='INCAR'):
        forbidden_keys = ['WANNIER90_WIN']
        with open(str(name),'w') as f:
            for key in self.vasp_params.keys():
                if ((self.vasp_params[key] != None) & (key not in forbidden_keys)):
                    f.write(str(key)+' = '+str(self.vasp_params[key]))
                    f.write('\n')
            if ('WANNIER90_WIN' in self.vasp_params.keys()):
                f.write('WANNIER90_WIN =\"\n')
                for data in self.vasp_params['WANNIER90_WIN']:
                    f.write(f'{data}\n')
                f.write('\"\n')            
                            
        f.close()

    def write_KPOINTS(self,name='KPOINTS'):
        forbidden_keys = ['extra_lines']
        with open(str(name),'w') as f:
            f.write('kpoints file \n')
            for key in self.vasp_kpoint_params.keys():
                if (key == 'len'):
                    f.write(str(self.vasp_kpoint_params[key])+'\n')
                elif (key == 'center'):
                    f.write(str(self.vasp_kpoint_params[key])+'\n')
                    if ('extra_lines' in self.vasp_kpoint_params.keys()):
                        for data in self.vasp_kpoint_params['extra_lines']:
                            f.write(str(data)+'\n')
                elif (key == 'grid'):
                    for data in self.vasp_kpoint_params[key]:
                        f.write(str(data))
                        f.write('\n')                        
                else:
                    if (key not in forbidden_keys):
                        f.write(str(self.vasp_kpoint_params[key]))
                        f.write('\n')
      

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

