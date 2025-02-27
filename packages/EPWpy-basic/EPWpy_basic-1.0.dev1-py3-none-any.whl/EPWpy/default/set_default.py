import numpy as np
from EPWpy.default.default import *
from EPWpy.utilities.printing import *

class set_default_vals:

    def __init__(self):
        """
        This class sets the default values for EPWpy
        -------------------
        """
 
    def default_values(self):
        """
        Putting default values in respective dictionaries

        --------------------
        """
        self.run_serial = False
        self.pw_control = pw_control
        self.pw_system = pw_system        
        self.pw_electrons = pw_electrons
        self.pw_ions = pw_ions
        self.pw_cell = pw_cell
        self.iondynamics = iondynamics
        self.celldynamics = celldynamics
        self.pw_atomic_species = pw_atomic_species
        self.pw_atomic_positions = pw_atomic_positions
        self.pw_kpoints = pw_kpoints
        self.pw_cell_parameters = pw_cell_parameters
        self.epw_params = epw_params
        self.pw_system['nat'] = len(pw_atomic_positions['atomic_pos'][:,0])
        self.pw_system['ntyp'] = len(pw_atomic_species['atomic_species'])
        self.pw_atomic_species['atoms'] = self.pw_system['nat']
        self.ph_params = ph_params
        self.ph_qpoints = ph_qpoints
        self.q2r_params = q2r_params
        self.zg_inputzg = zg_inputzg
        self.zg_inputazg = zg_inputazg
        self.eps_inputpp = eps_inputpp
        self.eps_energy_grid = eps_energy_grid
        self.pw_bands = pw_bands
        self.nscf_supercond = nscf_supercond
        self.matdyn_input=matdyn_input
        self.matdyn_kpoints=matdyn_kpoints
        self.phdos_input=phdos_input
        self.dos_input=dos_input
        self.pdos_input=pdos_input
        self.wannier_params = wannier_params
        self.pw2wann_params = pw2wann_params
        self.card_params = card_params
        self.cards = cards

    def default_checks(self, type_input):
        #if (self.verbosity > 2):
         #   print('Mass length: ', len(self.pw_atomic_species['mass']))

        if (len(self.pw_atomic_species['pseudo']) == 0):
            type_input.update({'pseudo_auto': True})

        if (self.pw_system['ecutwfc'] == None):
           self.pw_system['ecutwfc']  = self.get_ecutwfc()

        if (len(self.pw_atomic_species['mass']) == 0):
           self.pw_atomic_species['mass']  = self.get_mass()

        return(type_input) 

    @decorated_structure
    def set_values(self,type_input):
        """ 
        Fills default keys with values provided by user 
        """
        for key in type_input.keys():
            if key in self.pw_control:
                self.pw_control[key] = type_input[key]
            if key in self.pw_system:
                self.pw_system[key] = type_input[key]
            if key in self.pw_electrons:
                self.pw_electrons[key] = type_input[key]
            if key in self.pw_ions:
                self.pw_ions[key] = type_input[key]
            if key in self.pw_cell:
                self.pw_cell[key] = type_input[key]
            if key in self.pw_atomic_species:
                self.pw_atomic_species[key] = type_input[key]
            if key in self.pw_atomic_positions:
                self.pw_atomic_positions[key] = type_input[key]
            if key in self.pw_kpoints:
                self.pw_kpoints[key] = type_input[key]
            if key in self.pw_cell_parameters:
                self.pw_system['ibrav']=0
                self.pw_cell_parameters[key] = type_input[key]
        if (self.pw_system['ibrav'] == 0):
            self.pw_system['celldm(1)']=' '
            del self.pw_system['celldm(1)']
                
        for key in type_input.keys():
            if key in self.ph_params:
                self.ph_params[key] = type_input[key]  
        for key in type_input.keys():
            if key in self.epw_params:
                self.epw_params[key] = type_input[key]
        for key in type_input.keys():
            if key in self.q2r_params:
                self.q2r_params[key] = type_input[key]
        for key in type_input.keys():
#            if key in self.zg_params:
 #               self.zg_params[key] = type_input[key]
            if key in self.zg_inputzg:
                self.zg_inputzg[key] = type_input[key]
        for key in type_input.keys():
            if key in self.zg_inputazg:
                self.zg_inputazg[key] = type_input[key]
        for key in type_input.keys():
            if key in self.eps_inputpp:
               self.eps_inputpp[key] = type_input[key]
        for key in type_input.keys():
            if key in self.eps_energy_grid:
               self.eps_energy_grid[key] = type_input[key]
        for key in type_input.keys():
            if key in self.pw_bands:
                self.pw_bands[key] = type_input[key]
        for key in type_input.keys():
            if key in self.nscf_supercond:
                self.nscf_supercond[key] = type_input[key]
        for key in type_input.keys():
            if key in self.matdyn_input:
                self.matdyn_input[key]=type_input[key]
        for key in type_input.keys():
            if key in self.phdos_input:
                self.phdos_input[key]=type_input[key]
        for key in type_input.keys():
            if key in self.dos_input:
                self.dos_input[key]=type_input[key]
        for key in type_input.keys():
            if key in self.pdos_input:
                self.pdos_input[key]=type_input[key]

        self.prefix=self.pw_control['prefix']
        self.prefix=self.prefix.replace('\'','')
 
        if ('structure' in type_input.keys()):
            self.structure = type_input['structure'] 
            self.import_struct(type_input)

        if ('structure_mp' in type_input.keys()):
            self.matid = type_input['structure_mp']       
            self.import_struct(type_input)
        if ('read_config' in type_input.keys()):
            self.read_config(type_input)

        type_input = self.default_checks(type_input)
        self.pseudo_typ = 'PBE-FR-PDv0.4'
        self.pseudo_orbitals = ['','_r','-sp_r','-d_r','-s_r','-sp','-d','-s']
        self.pseudo_end = 'upf'
        if ('pseudo_auto' in type_input.keys()):
            if ('pseudo_type' in type_input.keys()):
                print('setting pseudo type to:', type_input['pseudo_type'])
                self.pseudo_typ = type_input['pseudo_type']
            if ('pseudo_orbitals' in type_input.keys()):
                self.pseudo_orbitals = type_input['pseudo_orbitals']
            
            self.atomic_species = self.pw_atomic_species['atomic_species']
            pseudo, pseudo_dir = self.get_pseudo()
            self.pw_control['pseudo_dir']='\''+pseudo_dir+'\''
            self.pw_atomic_species['pseudo'] = pseudo
        self.pseudo = self.pw_atomic_species['pseudo'] 

    def read_config(self, type_input):
        """
        Reads a configure file to build EPWpy calculation
        """
        pass

#    @decorated_structure
    def import_struct(self,type_input):
        self.pw_system['ibrav'] = 0
        if ('structure_mp' in type_input.keys()):
            self.get_poscar()            
            self.structure = f'POSCAR_{self.matid}'
        atomic_pos,lattice_vec,atoms,atomic_species,natoms, lattice_constant = self.get_atom()


        self.pw_system['celldm(1)'] = 1# lattice_constant
        self.pw_system['nat'] = sum(natoms)
        self.pw_system['ntyp'] = len(natoms)
        self.pw_atomic_species['atomic_species'] = atomic_species
        self.pw_atomic_species['nat_species'] = natoms 
        self.pw_atomic_positions={'num':pw_system['nat'],
                   'atomic_pos':atomic_pos,'atoms':atoms,'atomic_position_type':'crystal'}
        self.pw_cell_parameters['lattice_vector'] = lattice_vec[:,:]*lattice_constant
        del self.pw_system['celldm(1)']
        self.pw_cell_parameters['cell_type'] = 'angstrom'

        if(len(self.pw_atomic_species['mass']) < len(atomic_species)) :
            self.pw_atomic_species['mass']= self.get_mass()

        self.print_struct()

    def print_struct(self):

        for key in self.pw_cell_parameters.keys():
            if(key == 'lattice_vector'):
                for i,lattice_vector in enumerate(self.pw_cell_parameters[key]):
                    print(f'lattice vector({i+1}): ',end=" ")
                    print(lattice_vector)

        for key in self.pw_atomic_positions.keys():
            if(key == 'atomic_pos'):
                for i,atomic_pos in enumerate(self.pw_atomic_positions[key]):
                    atom=self.pw_atomic_positions['atoms'][i]
                    print(f'atom({i+1}): {atom}',end=" ")
                    print(atomic_pos)

