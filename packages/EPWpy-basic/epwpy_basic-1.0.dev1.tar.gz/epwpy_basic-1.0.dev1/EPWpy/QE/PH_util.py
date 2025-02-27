import numpy as np


class PH_properties:
    """
    This class comprises of PH properties
    attributes
    ..eps :: static dielectric constant
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
    def eps_ph(self):
        """
        Returns high-frequency dielectric matrix from DFPT
        """
        dielectric=get_dielectric_matrix(self.file)
        return(dielectric)

    @property
    def qpoints(self):
        """
        Returns q-points for Ph calculation
        """
        return(get_qpoints(self.file))
    @property
    def gkk(self):
        """
        Returns electron-phonon matrix as g(ibnd,jbnd,imode,ik,iq)
        """
        return(get_gkk(self.file))

def get_dielectric_matrix(ph_file):        
    T = 0
    i = 0
    dielectric = np.zeros((3,3), dtype = float) 
    with open(ph_file, 'r') as f:

        for line in f:

            if ('Dielectric constant in cartesian axis' in line):

                T = 1

            if ((T > 1) & (i < 3) & (len(line.split()) > 0)):
                dielectric[i,:] = np.array(line.split()[1:4]).astype(float)
                i +=1

            T = 2*T 
    f.close()
    return(dielectric)

def get_qpoints(ph_file):

    T = 0
    i = 0
    nqs = 0
    with open(ph_file, 'r') as f:

        for line in f:

            if ('Dynamical matrices for' in line):

                T = 1
            if (T == 2):

                nqs = int(line.split()[1])
                ph_qpoints = np.zeros((nqs,3),dtype=float)

            if ((T > 4) & (i < nqs) & (len(line.split()) > 0)):

                ph_qpoints[i,:3] = np.array(line.split()[1:4]).astype(float)
                i +=1
            T = 2*T
    f.close()
    return(ph_qpoints)
    

def get_gkk(ph_file):

    nq = []  
    nk = []
    q_arr = []
    k_arr = []
    g_mat = []
    band1=[]
    band2=[]
    mode = []
    kk = []
    qq = []
    t = 0
    iq = 0
    ik = 0
    with open(ph_file, 'r') as f:
        for line in f:
        
            if ('q coord' in line):
                Arr = line.split()[2:]
                t = 1
                if (Arr in q_arr):
                    pass
                else:
                    q_arr.append(Arr)
                    iq +=1
            if ('k coord' in line):
                Arr = line.split()[2:]
                if (Arr in k_arr):
                    pass
                else:
                    k_arr.append(Arr)
                    ik +=1
            t = t*2
            if ((t > 16) & ('-----------' in line)):
                t = 0

            if (t > 16):
                kk.append(ik)
                qq.append(iq)
                band1.append(int(line.split()[0]))
                band2.append(int(line.split()[1]))
                mode.append(int(line.split()[2]))
                g_mat.append(float(line.split()[-1]))                
    f.close()
    g = np.zeros((max(band1),max(band2),max(mode),len(k_arr),len(q_arr)),dtype = float)
    t = 0
    for i in range(len(g_mat)):
        g[band1[i]-1,band2[i]-1,mode[i]-1,kk[i]-1,qq[i]-1] = g_mat[i]

    return(g)

if __name__=="__main__":

    GKK = get_gkk('notebooks_basic/si/ph/ph_g.out')
    for i in range(4):
        for j in range(4):
            for k in range(6):
                print(GKK[i,j,k,0,0])
