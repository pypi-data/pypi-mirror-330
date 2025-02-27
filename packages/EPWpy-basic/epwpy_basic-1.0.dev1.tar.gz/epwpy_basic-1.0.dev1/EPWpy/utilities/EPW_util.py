""" For epw related utilities """
import numpy as np

class EPW_properties:
    """
    This class comprises of EPW properties
    attributes\n
    ..dtau :: polaron displacement\n
    ..gkk :: electron-phonon matrix
    """
    def __init__(self, file: str, 
                       energy_range: float = None
                        ):
        self.file = file
        self.energy_range = energy_range
    
    @property
    def dtau(self):
        """
        Returns polaron displacement
        """
        return(read_dtau(self.file))

    @property
    def psir_plrn(self):
        """
        Returns polaron wavefunction
        """
        return(read_psir_plrn(self.file))
    @property
    def gkk(self):
        """
        Returns electron-phonon matrix as g(ibnd,jbnd,imode,ik,iq)
        """
        return(get_gkk(self.file))


def get_connections(x,y,z, bond_leng = 3.5):

    connections = list()

    for i in range(len(x)):
        for j in range(len(x)):

            dist = np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2+(z[i]-z[j])**2)
            if(dist < bond_leng):
                connections.append((i,j))
    return(connections)

def read_dtau(filein):
    """
    reads the dtau
    """
    t = 0
    data=[]
    x=[]
    y=[]
    z=[]
    u=[]
    v=[]
    w=[]
    ilength = np.zeros((3,1),dtype=int)
    nline = 1000
    mat = []
    with open(filein, 'r') as f:

        for line in f:

            if (t == 10):
                nline = int(line.split()[0])
                print(nline)
            if((t>10) & (t<=10+nline)):
                mat.append(int(line.split()[0]))
                x.append(float(line.split()[1]))
                y.append(float(line.split()[2]))
                z.append(float(line.split()[3]))
                u.append(float(line.split()[4]))
                v.append(float(line.split()[5]))
                w.append(float(line.split()[6]))

            t +=1
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    u = np.array(u)
    v = np.array(v)
    w = np.array(w)
    mat = np.array(mat)
    connections = np.array(get_connections(x,y,z))
   
    return(x,y,z,u,v,w,connections,mat)

def read_psir_plrn(filein, bond_leng = 2.5):
    """
    reads the psir_plrn
    """
    t = 0
    data=[]
    x=[]
    y=[]
    z=[]
    u=[]
    v=[]
    w=[]
    ilength = np.zeros((3,1),dtype=int)
    lattice_vec = np.zeros((3,3),dtype = float)
    nline = 1000
    mat = []
    grid = list()
    Density=[]
    base =1e12
    base2=2e12
    mat = []
    with open(filein, 'r') as f:
        for line in f:
            if ((t > 5) & (t<9)):
                print(line.split())
                lattice_vec[t-6,:] = np.array(line.split()[:]).astype(float)

            if (t == 10):
                nline = int(line.split()[0])
                print(nline)

            if ((t>10) & (t<=10+nline)):
               # print(line.split()[0])
                mat.append(int(line.split()[0]))
                x.append(float(line.split()[1]))
                y.append(float(line.split()[2]))
                z.append(float(line.split()[3]))
                u.append(float(line.split()[4]))
                v.append(float(line.split()[5]))
                w.append(float(line.split()[6]))

            if (t == 10+nline+6):
                base = 10+nline+10
                for d in line.split():
                    grid.append(int(d))
                base2 = grid[0]*grid[1]*grid[2]

            if ((t > base) & (t < base+base2-1)): 
                try:
                    for data in line.split():
                        Density.append(float(data))    
                except ValueError:
                    break
            #dd +=1
            t +=1

    Dense = np.zeros((grid[0],grid[1],grid[2]),dtype =  float)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    u = np.array(u)
    v = np.array(v)
    w = np.array(w)
    mat = np.array(mat)

    Grid = np.zeros((grid[0],grid[1],grid[2],3),dtype = float)
    xx,yy,zz = np.mgrid[0:1:int(grid[0])*1j,0:1:grid[1]*1j,0:1:grid[2]*1j]

    t = 0
    pts = []
    #print(np.shape(Dense))
    #print(len(Density))
    for i in range(grid[0]):
        for j in range(grid[1]):
            for k in range(grid[2]):
                Grid[i,j,k,:] = lattice_vec[0,:]*xx[i,j,k]+lattice_vec[1,:]*yy[i,j,k]+lattice_vec[2,:]*zz[i,j,k]
                Dense[i,j,k] = Density[t]
                pts.append(Grid[i,j,k,:])
                t +=1

            
    connections = np.array(get_connections(x,y,z, bond_leng = bond_leng))
    Data = {'mat':mat,
            'x':x,
            'y':y,
            'z':z,
            'u':u,
            'v':v,
            'w':w,
            'Dense':Dense,
            'Grid':Grid,
            'pts':pts,
            'Density':Density,
            'connections':connections}

    return(Data)


def read_wfc(filein):
    """
    reads the psir_plrn
    """
    t = 0
    data=[]
    x=[]
    y=[]
    z=[]
    u=[]
    v=[]
    w=[]
    ilength = np.zeros((3,1),dtype=int)
    nline = 1000
    mat = []
    with open(filein, 'r') as f:
        for line in f:
            if (t == 10):
                nline = int(line.split()[0])
                print(nline)
            if((t>10) & (t<=10+nline)):
                mat.append(int(line.split()[0]))
                x.append(float(line.split()[1]))
                y.append(float(line.split()[2]))
                z.append(float(line.split()[3]))
                u.append(float(line.split()[4]))
                v.append(float(line.split()[5]))
                w.append(float(line.split()[6]))

            t +=1
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    u = np.array(u)
    v = np.array(v)
    w = np.array(w)
    mat = np.array(mat)
    connections = np.array(get_connections(x,y,z))
    return(x,y,z,u,v,w,connections,mat)

def read_cube_file(filein, bond_leng = 3.5):
    """
    Read a .cube file and return the scalar field data, grid dimensions, 
    atomic positions, origin, and axis vectors.
    """
    Data = {}
    with open(filein, 'r') as f:
        lines = f.readlines()

    # Skip the first two comment lines
    i = 2
    num_atoms, origin_x, origin_y, origin_z = map(float, lines[i].split())  # Number of atoms and origin
    num_atoms = int(num_atoms)
    i += 1

    # Read the grid dimensions and voxel information
    grid_info = []
    for _ in range(3):
        grid_info.append(list(map(float, lines[i].split())))
        i += 1

    # Extract grid dimensions and axis vectors
    n_points_x, n_points_y, n_points_z = abs(int(grid_info[0][0])), abs(int(grid_info[1][0])), abs(int(grid_info[2][0]))
    spacing_x, spacing_y, spacing_z = grid_info[0][1], grid_info[1][1], grid_info[2][1]
    axis_x = np.array(grid_info[0][1:4])  # Axis vector for X
    axis_y = np.array(grid_info[1][1:4])  # Axis vector for Y
    axis_z = np.array(grid_info[2][1:4])  # Axis vector for Z
    
    # Atoms data
    atomic_positions = []
    for _ in range(num_atoms):
        parts = lines[i].split()
        atom_number = int(parts[0])   # Atom number
        charge = float(parts[1])      # Atom charge
        x, y, z = map(float, parts[2:])  # Atomic position
        atomic_positions.append((atom_number, charge, x, y, z))
        i += 1

    # Bonds
    connections = np.array(get_connections(np.array(atomic_positions)[:,2],np.array(atomic_positions)[:,3],np.array(atomic_positions)[:,4], bond_leng))
 
    # Read the scalar field data
    scalar_data = []
    expected_num_values = n_points_x * n_points_y * n_points_z

    # Collect scalar data in a list of lists
    while i < len(lines):
        line = lines[i].split()
        if len(line) > 0:
            scalar_data.append(line)
        i += 1

    # Flatten the scalar data and ensure correct number of values
    scalar_data = [float(value) for sublist in scalar_data for value in sublist]

    # Check if the scalar data contains the expected number of values
    scalar_data_size = len(scalar_data)
    if scalar_data_size != expected_num_values:
        print(f"Warning: Expected {expected_num_values} scalar data points, but found {scalar_data_size}.")
        # Pad the data with NaN if it is smaller than expected
        if scalar_data_size < expected_num_values:
            padding = [np.nan] * (expected_num_values - scalar_data_size)
            scalar_data.extend(padding)
        # Truncate if there are more values than expected
        elif scalar_data_size > expected_num_values:
            scalar_data = scalar_data[:expected_num_values]
    
    # Reshape the scalar data into a 3D grid
    scalar_data = np.array(scalar_data).reshape((n_points_z, n_points_y, n_points_x))

    # Return all extracted data
    Data = {'scalar_data': scalar_data,
            'grid_shape': (n_points_x, n_points_y, n_points_z),
            'spacing':  (spacing_x, spacing_y, spacing_z),
            'origin':  (origin_x, origin_y, origin_z),
            'atomic_positions': atomic_positions,
            'connections': connections,
            'axis_x': axis_x, 'axis_y': axis_y, 'axis_z': axis_z}

    return Data

def read_gkk(filn, nbnd, nq, nk, nmode):
    """ Read the g matrix """
    G=np.zeros((nbnd,nbnd,nmode,nk,nq),dtype=float)
    t=0
    iq=0
    with open(filn,'r') as f:
        k=0
        q=0
        flag = 0
        read=0
        for line in f:
            if ('ik ' in line): 
                k +=1
                if (k == nk+1):
                    k = 1
            if ('iq ' in line):
                q +=1
                if (q == nq+1):
                    q = 1
            if (('-----' in line) & (k > 0)):
                flag = 1 

            if (('-----' in line) & (flag >= 2)):
                read = 0
                flag = 0

            if ((flag >= 2) & (len(line.split())>0)):
                #print(line.split())
                try:
                    ibnd=int(line.split()[0])-1
                    jbnd=int(line.split()[1])-1
                    imode=int(line.split()[2])-1

                    G[ibnd,jbnd,imode,k-1,q-1] = float(line.split()[-1])
                    flag +=1
                except ValueError:
                    flag = 0
            if (flag >= 1):
                flag +=1
 
    f.close()
    return(G)

def get_gkk(epw_file):

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
    with open(epw_file, 'r') as f:
        for line in f:
        
            if ('iq' in line):
                Arr = line.split()[2:]
                t = 1
                if (Arr in q_arr):
                    pass
                else:
                    q_arr.append(Arr)
                    iq +=1
            if ('ik' in line):
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

    g = read_gkk(epw_file, max(band1),len(q_arr),len(k_arr),max(mode))
    return(g)


def read_ibndmin(file):
    """ Reads the minimum bands used"""
    with open(file, 'r') as f:
        for line in f:
            if('ibndmin' in line):
                ibndmin = int(line.split()[2])
    f.close()
    return(ibndmin)
 
def read_ibndmax(file):
    """ Reads the maximum number of bands """
    with open(file, 'r') as f:
        for line in f:
            if('ibndmax' in line):
               ibndmax = int(line.split()[2])
    f.close()
    return(ibndmax)



 
def read_grr(filn, nbnd, nq, nmode):

    pass



if __name__=="__main__":
    #from plot_g import *
    import matplotlib.pyplot as plt

    G=get_gkk('notebooks_basic/si/epw/epw1.out')
    print(np.shape(G))
    #plot_gkk(4,4,G[:,:,:,0,:])
    #plt.show()
    

 #   print(np.shape(G))
 #   print(G) 
