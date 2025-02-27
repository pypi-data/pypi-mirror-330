import numpy as np


class PW_properties:
    """
    This class comprises of PW properties
    attributes
    ..nbnd :: number of bands
    ..nbnd_energy :: number of bands in a given energy range
    ..lattice_vec :: cell parameters from PW calculation
    ..fermi_level :: fermi level or highest occupied band
    ..atomic_positions :: atomic positions in an array
    ..band_scf :: scf bandstructure array  
    """
    def __init__(self, file: str, 
                       energy_range: float = None
                        ):
        self.file = file
        self.energy_range = energy_range
    
    @property
    def nbnd(self) -> int:

        bands = band_scf(self.file)
        return(len(bands[0,:]))

    @property
    def nbnd_energy(self) -> int:
        if (energy_range == None):
            raise Exception("Energy range not specified for obtaining bands")
        else:
            nbnd_energy,_=obtain_bands(self.energy_range,self.file)
        return(nbnd_energy)

    @property
    def lattice_vec(self) -> None:
        return(obtain_cell_parameters(self.file)) 
    
    @property
    def atomic_positions(self) -> None:
    
        _,atomic_positions,*_=read_scf(self.file)
        return(atomic_positions)

    @property
    def atomic_positions_relax(self) -> None:
    
        _,atomic_positions=obtain_atomic_positions(self.file)
        return(atomic_positions)

    @property
    def species(self):

        species,*_ = read_scf(self.file)
        return(species)

    @property
    def Structure(self) -> dict:
        Structure={'lattice': self.lattice_vec,
                   'species': self.species,
                   'coords':  self.atomic_positions}
        return(Structure) 

    @property
    def efermi(self) -> None:
        return(find_fermi(file=self.file))

    @property
    def total_energy(self) -> None:
        return(find_total_energy(file = self.file))
                
def find_total_energy(file='scf/scf.out'):
    """ 
    Finds total energy
    """
    with open(file,'r') as f:
        for line in f:
            if 'total energy' in line:
                tot=float(line.split()[-2])
                break
    return(tot)

def find_fermi(file='scf/scf.out'):
    """ Finds fermi level """

    with open(file,'r') as f:

        for line in f:
            if 'highest occupied level (ev)' in line:
                fermi=float(line.split()[-1])
                break

            if 'Fermi energy' in line:
                fermi=float(line.split()[-2])
                break

    return(fermi)

def obtain_bands(energy_range,file='nscf/nscf.out',arr=None,type_c=1):
    """ 
    Returns total number of bands in energy_range provided 
    """

    if (type_c == 1):
        band = band_scf(file)
    else:
        band = arr
    tot=0
    band_ind=[]
    for i in range(len(band[:,0])):
        if((max(band[i,:]) > energy_range[0]) & (min(band[i,:]) < energy_range[1])):
            tot +=1
            band_ind.append(i) 
    return(tot,band_ind)   

def obtain_cell_parameters(file='scf/relax.out'):
    """ Returns cell parameters """
    A=np.zeros((3,3),dtype=float)
    with open(file,'r') as f:
        for line in f:
            if ' a(1)' in line: 
                print(line.split())
                A[0,:]=np.array(line.split()[3:6]).astype(float)        
            if ' a(2)' in line:
                A[1,:]=np.array(line.split()[3:6]).astype(float)        
            if ' a(3)' in line:
                A[2,:]=np.array(line.split()[3:6]).astype(float)        
            if 'celldm(1)' in line:
                a=float(line.split()[1])
    bohr2ang = 0.529177  
    return(A*a*bohr2ang)

def obtain_atomic_positions(natoms,file='nscf/nscf.out'):
    """ 
    Returns atomic positions and species 
    """
    species=[]
    atom_pos=np.zeros((natoms,3),dtype=float)    
    with open(file,'r') as f:
        t = 0
        atomn = 0
        for line in f:
            if (('ATOMIC_POSITIONS' in line) | ((t > 0) & (t < 2))):
                t += 1
                species=[]
            if (t >=2):
                if (atomn < natoms):
                    species.append(line.split()[0])
                    atom_pos[atomn,:]=np.array(line.split()[1:]).astype(float)
                    atomn +=1
                else:
                    t = 0
                    atomn = 0
    return(species,atom_pos)
          
def band_scf(fname):
    """ Returns bandstructure obtained from bands calculation """

    Band=[]
    t=0
    Band_tmp=[]
    dec=1000
    with open(fname,'r') as f:
        AA=[]
        KK=[]
        for line in f:
            L=line.split()
            if(len(L)>2):

                if((L[0]=='Writing')&(L[2]=='to')):
                    dec=1000
            if((len(line.split())>1) & (dec==0)):    

                if(line.split()[0] !='k'):

                    for i in range(len(line.split())):
                        try: 
                            AA.append(float(line.split()[i]))
                        except ValueError:
                            continue

                elif((line.split()[0]=='k') & (len(AA)>0)):
                    Band.append(AA)    
                    AA=[]
                    KK=[]
            L=line.split()
            if(len(L)>2):
                if((L[0]=='End')&(L[2]=='band')):
                    dec=0
    if(len(AA)>0):
        Band.append(AA)
    Band=np.array(Band)
    return(Band)

def get_conduction_min(Band_scf,E_f,thr = 0.1,gap=10):
    # Assumption is that no material with a gap larger than 10 and smaller than 0.1 is used
    _,Bnd_scf  = obtain_bands([E_f+thr,E_f+gap],file=' ', arr=Band_scf.T, type_c = 2)
    return(Bnd_scf[0],np.argmin(Band_scf[:,Bnd_scf[0]]))

def get_valence_max(Band_scf,E_f,thr = 0.1, gap = 1):
    # Assumption is that no material with a gap larger than 10 and smaller than 0.1 is used
    _,Bnd_scf  = obtain_bands([E_f-gap,E_f+thr],file=' ', arr=Band_scf.T, type_c = 2)
    return(Bnd_scf[-1],np.argmax(Band_scf[:,Bnd_scf[-1]]))

def read_scf(filename):
    """ 
    Reads the SCF file 
    """
    atomic_labels = []
    atomic_positions = []
    cell_param = []
    add_param = {}
    reading_positions = False
    reading_cell_parameters = False

    with open(filename, "r") as file:
        for line in file:
            if "ATOMIC_POSITIONS " in line:
                reading_positions = True
            elif "CELL_PARAMETERS " in line:
                reading_cell_parameters = True
            elif reading_positions:
                line = line.strip()
                if line:
                    words = line.split()
                    atomic_label = words[0]
                    positions = np.array([float(w) for w in words[1:]])
                    atomic_labels.append(atomic_label)
                    atomic_positions.append(positions)
            elif reading_cell_parameters:
                line = line.strip()
                if line:
                    words = line.split()
                    cell_param.append([float(w) for w in words])
            else:
                if "nat" in line:
                    nat_value = line.split("=")[1].strip()
                    nat = int(nat_value)
                elif "ntyp" in line:
                    ntyp_value = line.split("=")[1].strip()
                    ntyp = int(ntyp_value)
                elif "ecutwfc" in line:
                    ecutwfc_value = line.split("=")[1].strip()
                    ecutwfc = float(ecutwfc_value)
    add_param["nat"] = nat
    add_param["ntyp"] = ntyp
    add_param["ecutwfc"] = ecutwfc

    return(atomic_labels, np.array(atomic_positions), np.array(cell_param), add_param)

