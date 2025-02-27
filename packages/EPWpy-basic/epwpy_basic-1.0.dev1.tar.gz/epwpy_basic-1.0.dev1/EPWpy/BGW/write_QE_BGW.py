import numpy as np
import os
#from os import *

class write_QE_BGW_files:
   
    def __init__(self,write):

        self.write=write
    
    def write_scf_QE(self,control={},system={},electrons={},ions={},cell={},name='scf'):
     
        #print(name)        
        with open(str(name)+'.in','w') as f:

            f.write('&CONTROL\n')

            for key in self.pw_control.keys():
                if(key not in control.keys()):
                    f.write(str(key)+' = '+str(self.pw_control[key]))
                    f.write('\n')
            for key in control.keys():
                    f.write(str(key)+' = '+str(control[key]))
                    f.write('\n')                        

            f.write('/\n')
            f.write('&SYSTEM\n')
            for key in self.pw_system.keys():
                if(key not in system.keys()):
                    if(self.pw_system[key] != None):
                        f.write(str(key)+' = '+str(self.pw_system[key]))
                        f.write('\n')
            for key in system.keys():
                    f.write(str(key)+' = '+str(system[key]))
                    f.write('\n')

            f.write('/\n')

            f.write('&ELECTRONS\n')
            for key in self.pw_electrons.keys():
                if(key not in electrons.keys()):
                    f.write(str(key)+' = '+str(self.pw_electrons[key]))
                    f.write('\n')
            for key in electrons.keys():
                    f.write(str(key)+' = '+str(electrons[key]))
                    f.write('\n') 
            f.write('/\n')

            if(self.iondynamics==True):
                f.write('&IONS\n') 
                for key in self.pw_ions.keys():
                    if(key not in ions.keys()):
                        f.write(str(key)+' = '+str(self.pw_ions[key]))
                        f.write('\n')
                for key in ions.keys():
                        f.write(str(key)+' = '+str(ions[key]))
                        f.write('\n')
                f.write('/\n')
            if(self.celldynamics==True):
                f.write('&CELL\n') 
                for key in self.pw_cell.keys():
                    if(key not in cell.keys()):
                        f.write(str(key)+' = '+str(self.pw_cell[key]))
                        f.write('\n')
                for key in cell.keys():
                        f.write(str(key)+' = '+str(cell[key]))
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
        f.close()


