import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from EPWpy.error_handling import error_handler
try:
    from mayavi import mlab
    from mayavi.mlab import *
    from tvtk.api import tvtk
except ModuleNotFoundError:
    error_handler.error_mayavi()    
    #print('The mayavi package not found\nTo visualize polarons in EPWpy, install mayavi')
    #print('Perform')

def plot_Ank_Bqv(mode, pathfile, sympoints, file):

    # Read kpath file
    kpath = np.loadtxt(pathfile, skiprows=1)

    # Read Ank file
    ik, ibnd, ek0, ReAnk, ImAnk, AbsAnk = np.loadtxt(file, unpack=True, skiprows=1)

    # Separate data in different bands
    nbnd=np.array(max(ibnd)).astype(int)
    maxik=np.array(max(ik)).astype(int)
    Ak=np.zeros((maxik,nbnd))
    ek=np.zeros((maxik,nbnd))
    iklist=np.zeros((maxik,nbnd))
    for i in range(maxik):
        for ibnd in range(nbnd):
            Ak[i][ibnd]=AbsAnk[i*nbnd+ibnd]
            ek[i][ibnd]=ek0[i*nbnd+ibnd]
            iklist[i][ibnd]=i

    # Get vbm and bandwidth
    vbm=max(ek[:,nbnd-1])
    bandwidth=vbm-min(ek[:,0])

    ## Plot bands
    f, ax = plt.subplots(figsize=(8,4))
    ax.plot(iklist, ek, color='blue')

    # Plot Ank
    if (mode=='Ank'):
        scatterlabel = r'$|A_{n\mathbf{k}}|$'
    else:
        scatterlabel = r'$|B_{\mathbf{q}\nu}|$'
    #
    if (mode=='Ank'):
        ax.scatter(iklist, ek, 100*Ak, color='gold', edgecolors='gray', alpha=0.8, label=scatterlabel)
    else:
        ax.scatter(iklist, ek, 50*Ak, color='gold', edgecolors='gray', alpha=0.8, label=scatterlabel)

    # Define high-symmetry points
    W=[0.5,0.75,0.25]
    L=[0.0,0.5,0.0]
    G=[0.0,0.0,0.0]
    X=[0.5,0.5,0.0]
    K=[0.375,0.75,0.375]
    sympoints=[W,L,G,X,W,K]
    # Plot high-symmetry points
    
    if (mode=='Ank'):
        for i in range(len(kpath)):
            for k in sympoints:
                if (np.linalg.norm(kpath[i][0:3]-k)<1E-6):
                    # Plot dashed line
                    ax.plot([iklist[i][0],iklist[i][0]],[-bandwidth-0.15*bandwidth,0.1*bandwidth],'--',color='gray',linewidth=0.7)
                    # Name the symmetry point
                    if (k == W):
                        ax.text(iklist[i][0]-3.0,-bandwidth-0.2*bandwidth,r'$\mathrm{W}$',fontsize=25)
                    if (k == L):
                        ax.text(iklist[i][0]-3.0,-bandwidth-0.2*bandwidth,r'$\mathrm{L}$',fontsize=25)
                    if (k == G):
                        ax.text(iklist[i][0]-3.0,-bandwidth-0.2*bandwidth,r'$\Gamma$',fontsize=25)
                    if (k == X):
                        ax.text(iklist[i][0]-3.0,-bandwidth-0.2*bandwidth,r'$\mathrm{X}$',fontsize=25)
                    if (k == K):
                        ax.text(iklist[i][0]-3.0,-bandwidth-0.2*bandwidth,r'$\mathrm{K}$',fontsize=25)
    else:
        for i in range(len(kpath)):
            for k in sympoints:
                if (np.linalg.norm(kpath[i][0:3]-k)<1E-6):
                    # Plot dashed line
                    ax.plot([iklist[i][0],iklist[i][0]],[0.0,vbm+0.1*vbm],'--',color='gray',linewidth=0.7)
                    # Name the symmetry point
                    if (k == W):
                        ax.text(iklist[i][0]-3.0,-0.1*vbm,r'$\mathrm{W}$',fontsize=25)
                    if (k == L):
                        ax.text(iklist[i][0]-3.0,-0.1*vbm,r'$\mathrm{L}$',fontsize=25)
                    if (k == G):
                        ax.text(iklist[i][0]-3.0,-0.1*vbm,r'$\Gamma$',fontsize=25)
                    if (k == X):
                        ax.text(iklist[i][0]-3.0,-0.1*vbm,r'$\mathrm{X}$',fontsize=25)
                    if (k == K):
                        ax.text(iklist[i][0]-3.0,-0.1*vbm,r'$\mathrm{K}$',fontsize=25)
        

    # Set tick params etc.
    if (mode=='Ank'):
        ax.set_ylim(-bandwidth-0.1*bandwidth,0.1*bandwidth)
    else:
        ax.set_ylim(0.0,vbm+0.1*vbm)
    #
    ax.set_xlim((min(iklist[:,0]),max(iklist[:,0])))
    ax.set_xticklabels([])
    ax.tick_params(axis='x', color='black', labelsize='0', pad=0, length=0, width=0)  
    ax.tick_params(axis='y', color='black', labelsize='18', pad=5, length=5, width=1)  
    #
    if (mode=='Ank'):
        ax.set_ylabel(r'$E-E_{\mathrm{VBM}} ~ (\mathrm{eV})$', fontsize=25, labelpad=10)
    else:
        ax.set_ylabel(r'$\omega_{\mathbf{q}\nu} ~ (\mathrm{meV})$', fontsize=25, labelpad=10)
    #
    ax.legend(loc='upper right', fontsize=25)
    
    
def plot_EvsNk(ucell_volume, Nk, Eform):
    
    # Start figure
    fig, ax = plt.subplots(figsize=(8,4))

    # Plot Eform
    ax.scatter(1/(Nk*ucell_volume**(1/3)), Eform, s=50, marker='o', color='darkred', edgecolors='black')

    # Perform linear fit and plot
    mf, bf = np.polyfit(1/(Nk*ucell_volume**(1/3)), Eform, 1)
    xlist = np.linspace(0.0, np.max(1/(Nk*ucell_volume**(1/3))), 100)
    print("Extrapolation to isolated polaron formation energy = ", "%.3f" % bf, "eV")
    ax.plot(xlist, mf*xlist+bf, '--', color='gray')

    # Set tick params etc.
    ax.set_xlabel(r'Inverse supercell size ($\mathrm{bohr}^{-1}$)',fontsize=20)
    ax.set_ylabel('Formation energy (eV)',fontsize=20, labelpad=5)
    ax.tick_params(axis='x', color='black', labelsize='20', pad=5, length=5, width=2)
    ax.tick_params(axis='y', color='black', labelsize='20', pad=5, length=5, width=2, right=True)
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(axis='y', which='minor', color='black', labelsize='20', pad=5, length=3, width=1.2, right=True)
    ax.set_xlim(0.0, np.max(1/(Nk*ucell_volume**(1/3)))+0.01)
    #ax.set_title('LiF hole polaron', fontsize=20)

    #plt.savefig("E_vs_nk.pdf")
    plt.show()
    plt.close()


def plot_dtau(x,y,z,u,v,w,mat,connections):
    """
    For plotting dtau using psir_plrn.xsf
    """
    mlab.figure('EPWpy', bgcolor=(0, 0, 0), size=(650, 650))
    mlab.clf()
    prev_mat = mat[0]
    n=2
    colr=[(1,0,0),(0,1,1),(1,1,1)]
    matn = []
    for i in range(len(mat)):
        if (prev_mat == mat[i]):
            matn.append(n)
        else:
            prev_mat = mat[i]
            n +=1

            matn.append(n)

    matn = np.array(matn)
        

    src = mlab.points3d(x,y,z, matn, scale_factor=0.5, resolution=10)
    src.mlab_source.dataset.lines = np.array(connections)

    tube = mlab.pipeline.tube(src, tube_radius=0.15)
    tube.filter.radius_factor = 1.
    #tube.filter.vary_radius = 'vary_radius_by_scalar'
    mlab.pipeline.surface(tube, color=(0.8, 0.8, 0))
    mlab.quiver3d(x, y, z, u, v, w)
    #mlab.show()

def plot_psir_plrn(Data):
    """
    For plotting dtau using psir_plrn.xsf
    """
    mat = Data['mat']
    x   = Data['x']
    y   = Data['y']
    z   = Data['z']
    u   = Data['u']
    v   = Data['v']
    w   = Data['w']
    Dense = Data['Dense']
    Grid  = Data['Grid']
    pts   = Data['pts']
    Density = Data['Density']
    connections = Data['connections']

    if ('in_notebook' in Data.keys()):
        if('backend' in Data.keys()):
            mlab.init_notebook(backend = Data['backend'])
        else:
            mlab.init_notebook()
 
    mlab.figure('EPWpy', bgcolor=(0, 0, 0), size=(650, 650))
    #mlab.clf()
 
    prev_mat = mat[0]
    n=2
    colr=[(1,0,0),(0,1,1),(1,1,1)]
    matn = []
    for i in range(len(mat)):
        if (prev_mat == mat[i]):
            matn.append(n)
        else:
            prev_mat = mat[i]
            n +=1

            matn.append(n)

    matn = np.array(matn)

    src = mlab.points3d(x,y,z, matn, scale_factor=0.5, resolution=10)
    src.mlab_source.dataset.lines = np.array(connections)

    tube = mlab.pipeline.tube(src, tube_radius=0.15)
    tube.filter.radius_factor = 1.
    mlab.pipeline.surface(tube, color=(0.8, 0.8, 0))

    Density = np.array(Density)
    sg = tvtk.StructuredGrid(dimensions=Grid[:,:,:,0].shape, points=pts)
    sg.point_data.scalars = Density.ravel()
    d = mlab.pipeline.add_dataset(sg)

    iso = mlab.pipeline.iso_surface(d,color=(0.5, 0.5, 0))
    iso.contour.number_of_contours = 500

    
    src = mlab.points3d(x,y,z, matn, scale_factor=0.5, resolution=10)
    src.mlab_source.dataset.lines = np.array(connections)

    ax1 = mlab.axes(nb_labels=4,
                 extent=[np.amin(Grid[:,:,:,0]),np.amax(Grid[:,:,:,0]),
                         np.amin(Grid[:,:,:,1]),np.amax(Grid[:,:,:,1]),
                         np.amin(Grid[:,:,:,2]),np.amax(Grid[:,:,:,2]), ],
               )

    mlab.outline(ax1)
    if ('in_notebook' in Data.keys()):
        return(mlab.quiver3d(x, y, z, u, v, w))
    else:
        mlab.quiver3d(x, y, z, u, v, w)
        mlab.show()

