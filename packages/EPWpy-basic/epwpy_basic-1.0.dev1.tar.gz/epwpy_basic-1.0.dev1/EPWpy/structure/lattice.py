import numpy as np
import requests
import os
from EPWpy.structure.position_atoms import *
from EPWpy.utilities.printing import *
from EPWpy.utilities.display_struct import display_crystal
from EPWpy.error_handling import error_handler
try:
    from mp_api.client import MPRester
except ImportError:
    error_handler.error_mp()
#    print('The mp-api not found\n, To directly use the mp-api ID for structure download, install mp-api')


class lattice:
    """ 
    lattice class 
    """
    def __init__(self, data):
        self.data = data

    def get_atom(self):
        """
        Gets atomic attributes from a poscar structure file
        """
        atom_pos,atom_pos2,lattice_vec,mat,materials,natoms,a = main_extract([0.0,0.0],self.structure,T=1)
        return(atom_pos,lattice_vec,mat,materials,natoms,a)

    def atom_cart(self):
        """
        Gets atomic positions in cartesian co-ordinate
        """
        atom_pos,atom_pos2,lattice_vec,mat,materials,natoms,a = main_extract([0.0,0.0],self.structure,T=1)
        return(atom_pos2)

    def get_xyz(self,supercell=[]):
        """ 
        Writes a xyz file
        """
        atom_pos,lattice_vec,mat,materials,natoms,a = self.get_atom()   
        atom_pos2 = self.atom_cart()
        if(len(supercell) !=0):
            atom_pos2,natoms,mat = get_supercell(atom_pos2,natoms,mat,lattice_vec,a,supercell)
        gen_xyz(atom_pos2,natoms,mat)
       
    def get_supercell(self,supercell=[]):
        """
        returns the co-ordinates for supercell
        """
        atom_pos,lattice_vec,mat,materials,natoms,a = self.get_atom()   
        atom_pos2 = self.atom_cart()
        if(len(supercell) !=0):
            atom_pos2,natoms,mat = get_supercell(atom_pos2,natoms,mat,lattice_vec,a,supercell)
        return(atom_pos2,natoms,mat)
 
    def display_lattice_legacy(self,supercell=[],view={}):
        """
        Display lattice
        """ 
        self.get_xyz(supercell)
        return(display_molecule(view))#self.atom_cart())

    def display_lattice(self,supercell=[],view={},bond_length = 3.5):
        """
        Display lattice
        """ 
        atom_pos2, natoms, mat = self.get_supercell(supercell)
        Data= {'positions':atom_pos2,'mat':mat}
     #   print ('supercell: ',supercell) 
        return(display_crystal(Data, view = view, bond_length=bond_length))#self.atom_cart())


    def get_poscar(self):
        """
        Gets the structure file from materials project
        """
        with MPRester("TOljhDNo0yfz6PF69vOTH5Br2PaTcsbI") as mpr:
            docs = mpr.materials.summary.search(material_ids=[f'{self.matid}'], fields=["structure"])
            structure = docs[0].structure
            # -- Shortcut for a single Materials Project ID:
            structure = mpr.get_structure_by_material_id(f'{self.matid}')
            structure.to(fmt="POSCAR", filename=f'POSCAR_{self.matid}')

          
    def get_pseudo(self,name='pseudo'):
        """
        Automatically download pseudopotential from pseudodojo
        """
        try:
            os.mkdir('pseudo')
        except OSError:
            pass
            #print('pseudo folder found')
        cwd=os.getcwd()
        pseudos=[]                  
        for atoms in self.atomic_species:
            response = self.get_response(atoms) 
            with open(f'./pseudo/{atoms}_r.{self.pseudo_end}', 'w') as f:
                for line in response.text:
                    f.write(line)
            pseudos.append(f'{atoms}_r.{self.pseudo_end}')
        return(pseudos, str(cwd)+'/pseudo/')

    def get_ecutwfc(self):
        atom_list = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V",
                    "Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh",
                    "Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb",
                    "Bi","Po"]
        ecut_list = ["36","45","37","44","38","41","42","42","42","34","44","42","20","18","22","26","29","33","37","34","39","42",
                    "42","47","48","45","48","49","46","42","40","39","42","43","23","26","23","34","36","33","41","40","42","42",
                    "44","41","41","51","35","36","40","40","35","34","25","22","29","29","37","36","37","34","42","38","33","31",
                    "28","33","32"]
        cutoff_array = []
        for atoms in self.pw_atomic_species['atomic_species']:
            atom_index = atom_list.index(atoms)
            atom_cutoff = ecut_list[atom_index]
            cutoff_array.append(int(atom_cutoff))
        ecutwfc = max(cutoff_array)
        return ecutwfc

    def get_mass(self):
        mass_dict = {'H' : 1.008,'He' : 4.003, 'Li' : 6.941, 'Be' : 9.012,\
                 'B' : 10.811, 'C' : 12.011, 'N' : 14.007, 'O' : 15.999,\
                 'F' : 18.998, 'Ne' : 20.180, 'Na' : 22.990, 'Mg' : 24.305,\
                 'Al' : 26.982, 'Si' : 28.086, 'P' : 30.974, 'S' : 32.066,\
                 'Cl' : 35.453, 'Ar' : 39.948, 'K' : 39.098, 'Ca' : 40.078,\
                 'Sc' : 44.956, 'Ti' : 47.867, 'V' : 50.942, 'Cr' : 51.996,\
                 'Mn' : 54.938, 'Fe' : 55.845, 'Co' : 58.933, 'Ni' : 58.693,\
                 'Cu' : 63.546, 'Zn' : 65.38, 'Ga' : 69.723, 'Ge' : 72.631,\
                 'As' : 74.922, 'Se' : 78.971, 'Br' : 79.904, 'Kr' : 84.798,\
                 'Rb' : 84.468, 'Sr' : 87.62, 'Y' : 88.906, 'Zr' : 91.224,\
                 'Nb' : 92.906, 'Mo' : 95.95, 'Tc' : 98.907, 'Ru' : 101.07,\
                 'Rh' : 102.906, 'Pd' : 106.42, 'Ag' : 107.868, 'Cd' : 112.414,\
                 'In' : 114.818, 'Sn' : 118.711, 'Sb' : 121.760, 'Te' : 126.7,\
                 'I' : 126.904, 'Xe' : 131.294, 'Cs' : 132.905, 'Ba' : 137.328,\
                 'La' : 138.905, 'Ce' : 140.116, 'Pr' : 140.908, 'Nd' : 144.243,\
                 'Pm' : 144.913, 'Sm' : 150.36, 'Eu' : 151.964, 'Gd' : 157.25,\
                 'Tb' : 158.925, 'Dy': 162.500, 'Ho' : 164.930, 'Er' : 167.259,\
                 'Tm' : 168.934, 'Yb' : 173.055, 'Lu' : 174.967, 'Hf' : 178.49,\
                 'Ta' : 180.948, 'W' : 183.84, 'Re' : 186.207, 'Os' : 190.23,\
                 'Ir' : 192.217, 'Pt' : 195.085, 'Au' : 196.967, 'Hg' : 200.592,\
                 'Tl' : 204.383, 'Pb' : 207.2, 'Bi' : 208.980, 'Po' : 208.982,\
                 'At' : 209.987, 'Rn' : 222.081, 'Fr' : 223.020, 'Ra' : 226.025,\
                 'Ac' : 227.028, 'Th' : 232.038, 'Pa' : 231.036, 'U' : 238.029,\
                 'Np' : 237, 'Pu' : 244, 'Am' : 243, 'Cm' : 247, 'Bk' : 247,\
                 'Ct' : 251, 'Es' : 252, 'Fm' : 257, 'Md' : 258, 'No' : 259,\
                 'Lr' : 262, 'Rf' : 261, 'Db' : 262, 'Sg' : 266, 'Bh' : 264,\
                 'Hs' : 269, 'Mt' : 268, 'Ds' : 271, 'Rg' : 272, 'Cn' : 285,\
                 'Nh' : 284, 'Fl' : 289, 'Mc' : 288, 'Lv' : 292, 'Ts' : 294,\
                 'Oh' : 294}

        mass_array = []
        for atoms in self.pw_atomic_species['atomic_species']:
            atom_mass = mass_dict[atoms]
            mass_array.append(float(atom_mass))
        return mass_array

    def get_response(self, atoms):
        pseudo_type = self.pseudo_typ
        end = self.pseudo_end
        """
        Get the response from pseudodojo website
        """ 
        for orbital in self.pseudo_orbitals:
            url = f'https://raw.githubusercontent.com/PseudoDojo/ONCVPSP-{pseudo_type}/master/{atoms}/{atoms}{orbital}.{end}'#/As/As-d_r.upf
            print(url) 
            response = requests.get(url)
            if (response.ok == True):
                found = f'ONCVPSP-{pseudo_type}/{atoms}{orbital}.{end}' 
                break               
        if(response.ok == False):
            print(f'pseudo not found for {atoms} in pseudodojo, please download manually')
            print(f'Add tags pseudo_dir:<location of pseudo> and pseudo:[\'each species\'] in EPWpy object')
        else:
            print(f'pseudo found at pseudodojo : {found}')
        return(response)

def get_supercell(atom_pos2,natoms,mat,lattice_vec,a,supercell):
    """
    Builds supercell of a certain size
    """
    Nx = supercell[0]
    Ny = supercell[1]
    Nz = supercell[2]

    matn = []
    natoms = []
    atom_posn = np.zeros((len(atom_pos2[:,0])*Nx*Ny*Nz,3), dtype = float)
    p=0

    for t in range(len(atom_pos2[:,0])):
        for i in range(Nx):
            for j in range(Ny):
                for k in range(Nz):
       
                    atom_posn[p,:] = atom_pos2[t,:]+a*(i*lattice_vec[0,:]+j*lattice_vec[1,:]+k*lattice_vec[2,:])
                    matn.append(mat[t])
                    natoms.append(1)
                    p +=1
    return(atom_posn,natoms,matn)

                    
