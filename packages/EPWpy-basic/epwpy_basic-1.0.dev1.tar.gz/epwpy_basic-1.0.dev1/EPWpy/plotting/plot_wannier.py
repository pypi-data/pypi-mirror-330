import numpy as np
from EPWpy.error_handling import error_handler
try:
    from mayavi import mlab
    from mayavi.modules.iso_surface import IsoSurface
    from tvtk.api import tvtk
except ModuleNotFoundError:
    error_handler.error_mayavi()    
    #print('The mayavi package not found\nTo visualize polarons in EPWpy, install mayavi')
    #print('Perform')



def plot_isosurface_from_cube_file(Data):
    """
    Take data read from .cube file, 
    and plot two isosurfaces: one positive at 10% of max value, and one negative at the same value but negative.
    Plot atomic positions as well.
    """
    # Take the data
    scalar_data = Data['scalar_data']
    grid_shape = Data['grid_shape']
    spacing = Data['spacing']
    origin = Data['origin']
    atomic_positions = Data['atomic_positions']
    axis_x = Data['axis_x']
    axis_y = Data['axis_y']
    axis_z = Data['axis_z']
    connections = Data['connections']
    if ('verbosity' in Data.keys()):
        verbosity = Data['verbosity']

    # Initializing mayavi with a backend

    if ('in_notebook' in Data.keys()):
        if('backend' in Data.keys()):
            mlab.init_notebook(backend = Data['backend'])
        else:
            mlab.init_notebook()
 
    # Initialize figure
    mlab.figure(size=(800, 600))

    # Extract grid dimensions and spacings
    n_points_x, n_points_y, n_points_z = grid_shape
    spacing_x, spacing_y, spacing_z = spacing

    # Create a 3D grid for the coordinates
    x_indices = np.arange(n_points_x)
    y_indices = np.arange(n_points_y)
    z_indices = np.arange(n_points_z)

    # Compute the grid points based on axis vectors and spacings
    X = origin[0] + x_indices[:, None, None] * axis_x[0] + y_indices[None, :, None] * axis_y[0] + z_indices[None, None, :] * axis_z[0]
    Y = origin[1] + x_indices[:, None, None] * axis_x[1] + y_indices[None, :, None] * axis_y[1] + z_indices[None, None, :] * axis_z[1]
    Z = origin[2] + x_indices[:, None, None] * axis_x[2] + y_indices[None, :, None] * axis_y[2] + z_indices[None, None, :] * axis_z[2]

    # Flatten the coordinate arrays
    coords = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).T

    # Create a StructuredGrid in tvtk
    structured_grid = tvtk.StructuredGrid(dimensions=(n_points_x, n_points_y, n_points_z))
    structured_grid.points = coords  # Assign the flattened coordinates to the grid

    # Assign the scalar field to the grid as point data
    structured_grid.point_data.scalars = scalar_data.flatten()
    structured_grid.point_data.scalars.name = 'ScalarField'

    # Find the maximum value in the scalar field data
    max_value = np.max(scalar_data)

    # Set the isosurface values for positive and negative contours
    iso_value = 0.1 * max_value
    print(f"Positive isosurface contour set to: {iso_value} (10% of max value: {max_value})")

    # Create an iso_surface pipeline from the structured grid (positive)
    iso_pos = mlab.pipeline.iso_surface(structured_grid, contours=[iso_value], colormap='Oranges', opacity=0.8)

    # Create an iso_surface pipeline from the structured grid (positive)
    iso_neg = mlab.pipeline.iso_surface(structured_grid, contours=[-iso_value], colormap='Blues', opacity=0.8)


    # Plot atomic positions with jmol colors and atomic radius-based size
    length = len(np.array(atomic_positions))
    X = []
    Y = []
    Z = []
    for i,atom in enumerate(atomic_positions):
        atom_number, charge, x, y, z = atom
        # Get jmol color for the atomic number
        color = jmol_colors.get(atom_number, (0.5, 0.5, 0.5))  # Default to gray if not in map
        # Get atomic radius (if available) and adjust the size accordingly
        radius =  atomic_radii.get(atom_number, 50*pm2bohr)  # Default to 50 pm if not in the map
        size = (radius / 2) # Scale size for visibility
        # Print atomic info for the user
        if (verbosity > 2):
            print(f"Atom: {atom_number}, Position: ({x}, {y}, {z}), Radius: {radius} bohr")
        X.append(x)
        Y.append(y)
        Z.append(z)
        src =  mlab.points3d(x, y, z, color=color, scale_factor=size)               
 
    src =  mlab.points3d(X, Y, Z, color=(0,0,0), scale_factor=0.0)#size)               
    src.mlab_source.dataset.lines = np.array(connections)
    tube = mlab.pipeline.tube(src, tube_radius=0.15)
    tube.filter.radius_factor = 1.
    mlab.pipeline.surface(tube, color=(0.8, 0.8, 0))
 
    if ('in_notebook' in Data.keys()):
       return(src)#mlab.points3d(x, y, z, color=color, scale_factor=size))
    else:
        mlab.show()


"""


    for i,atom in enumerate(atomic_positions):
        print(atom)
        atom_number, charge, x, y, z = atom
        # Get jmol color for the atomic number
        color = jmol_colors.get(atom_number, (0.5, 0.5, 0.5))  # Default to gray if not in map
        # Get atomic radius (if available) and adjust the size accordingly
        radius = atomic_radii.get(atom_number, 50*pm2bohr)  # Default to 50 pm if not in the map
        size = radius / 2 # Scale size for visibility
        # Print atomic info for the user
        print(f"Atom: {atom_number}, Position: ({x}, {y}, {z}), Radius: {radius} bohr")

 
        if (i == length - 1):
            if ('in_notebook' in Data.keys()):
                src =  mlab.points3d(x, y, z, color=color, scale_factor=size)               
                src.mlab_source.dataset.lines = np.array(connections)
                tube = mlab.pipeline.tube(src, tube_radius=0.15)
                tube.filter.radius_factor = 1.
                mlab.pipeline.surface(tube, color=(0.8, 0.8, 0))
                return(src)#mlab.points3d(x, y, z, color=color, scale_factor=size))
        else:
            mlab.points3d(x, y, z, color=color, scale_factor=size) 
    # Show the plot
    if ('in_notebook' in Data.keys()):
        pass
    else:
        mlab.show()

"""

# jmol color mapping for elements (atomic number -> RGB color tuple) (from https://jmol.sourceforge.net/jscolors/)
jmol_colors = {
    1:	 (255/255,255/255,255/255),  # H
    2:	 (217/255,255/255,255/255),  # He
    3:	 (204/255,128/255,255/255),  # Li
    4:	 (194/255,255/255,  0/255),  # Be
    5:	 (255/255,181/255,181/255),  # B
    6:	 (144/255,144/255,144/255),  # C
    7:	 ( 48/255, 80/255,248/255),  # N
    8:	 (255/255, 13/255, 13/255),  # O
    9:	 (144/255,224/255, 80/255),  # F
    10:	 (179/255,227/255,245/255),  # Ne
    11:	 (171/255, 92/255,242/255),  # Na
    12:	 (138/255,255/255,  0/255),  # Mg
    13:	 (191/255,166/255,166/255),  # Al
    14:	 (240/255,200/255,160/255),  # Si
    15:	 (255/255,128/255,  0/255),  # P
    16:	 (255/255,255/255, 48/255),  # S
    17:	 ( 31/255,240/255, 31/255),  # Cl
    18:	 (128/255,209/255,227/255),  # Ar
    19:	 (143/255, 64/255,212/255),  # K
    20:	 ( 61/255,255/255,  0/255),  # Ca
    21:	 (230/255,230/255,230/255),  # Sc
    22:	 (191/255,194/255,199/255),  # Ti
    23:	 (166/255,166/255,171/255),  # V
    24:	 (138/255,153/255,199/255),  # Cr
    25:	 (156/255,122/255,199/255),  # Mn
    26:	 (224/255,102/255, 51/255),  # Fe
    27:	 (240/255,144/255,160/255),  # Co
    28:	 ( 80/255,208/255, 80/255),  # Ni
    29:	 (200/255,128/255, 51/255),  # Cu
    30:	 (125/255,128/255,176/255),  # Zn
    31:	 (194/255,143/255,143/255),  # Ga
    32:	 (102/255,143/255,143/255),  # Ge
    33:	 (189/255,128/255,227/255),  # As
    34:	 (255/255,161/255,  0/255),  # Se
    35:	 (166/255, 41/255, 41/255),  # Br
    36:	 ( 92/255,184/255,209/255),  # Kr
    37:	 (112/255, 46/255,176/255),  # Rb
    38:	 (  0/255,255/255,  0/255),  # Sr
    39:	 (148/255,255/255,255/255),  # Y
    40:	 (148/255,224/255,224/255),  # Zr
    41:	 (115/255,194/255,201/255),  # Nb
    42:	 ( 84/255,181/255,181/255),  # Mo
    43:	 ( 59/255,158/255,158/255),  # Tc
    44:	 ( 36/255,143/255,143/255),  # Ru
    45:	 ( 10/255,125/255,140/255),  # Rh
    46:	 (  0/255,105/255,133/255),  # Pd
    47:	 (192/255,192/255,192/255),  # Ag
    48:	 (255/255,217/255,143/255),  # Cd
    49:	 (166/255,117/255,115/255),  # In
    50:	 (102/255,128/255,128/255),  # Sn
    51:	 (158/255, 99/255,181/255),  # Sb
    52:	 (212/255,122/255,  0/255),  # Te
    53:	 (148/255,  0/255,148/255),  # I
    54:	 ( 66/255,158/255,176/255),  # Xe
    55:	 ( 87/255, 23/255,143/255),  # Cs
    56:	 (  0/255,201/255,  0/255),  # Ba
    57:	 (112/255,212/255,255/255),  # La
    58:	 (255/255,255/255,199/255),  # Ce
    59:	 (217/255,255/255,199/255),  # Pr
    60:	 (199/255,255/255,199/255),  # Nd
    61:	 (163/255,255/255,199/255),  # Pm
    62:	 (143/255,255/255,199/255),  # Sm
    63:	 ( 97/255,255/255,199/255),  # Eu
    64:	 ( 69/255,255/255,199/255),  # Gd
    65:	 ( 48/255,255/255,199/255),  # Tb
    66:	 ( 31/255,255/255,199/255),  # Dy
    67:	 (  0/255,255/255,156/255),  # Ho
    68:	 (  0/255,230/255,117/255),  # Er
    69:	 (  0/255,212/255, 82/255),  # Tm
    70:	 (  0/255,191/255, 56/255),  # Yb
    71:	 (  0/255,171/255, 36/255),  # Lu
    72:	 ( 77/255,194/255,255/255),  # Hf
    73:	 ( 77/255,166/255,255/255),  # Ta
    74:	 ( 33/255,148/255,214/255),  # W
    75:	 ( 38/255,125/255,171/255),  # Re
    76:	 ( 38/255,102/255,150/255),  # Os
    77:	 ( 23/255, 84/255,135/255),  # Ir
    78:	 (208/255,208/255,224/255),  # Pt
    79:	 (255/255,209/255, 35/255),  # Au
    80:	 (184/255,184/255,208/255),  # Hg
    81:	 (166/255, 84/255, 77/255),  # Tl
    82:	 ( 87/255, 89/255, 97/255),  # Pb
    83:	 (158/255, 79/255,181/255),  # Bi
    84:	 (171/255, 92/255,  0/255),  # Po
    85:	 (117/255, 79/255, 69/255),  # At
    86:	 ( 66/255,130/255,150/255),  # Rn
    87:	 ( 66/255,  0/255,102/255),  # Fr
    88:	 (  0/255,125/255,  0/255),  # Ra
    89:	 (112/255,171/255,250/255),  # Ac
    90:	 (  0/255,186/255,255/255),  # Th
    91:	 (  0/255,161/255,255/255),  # Pa
    92:	 (  0/255,143/255,255/255),  # U
    93:	 (  0/255,128/255,255/255),  # Np
    94:	 (  0/255,107/255,255/255),  # Pu
    95:	 ( 84/255, 92/255,242/255),  # Am
    96:	 (120/255, 92/255,227/255),  # Cm
    97:	 (138/255, 79/255,227/255),  # Bk
    98:	 (161/255, 54/255,212/255),  # Cf
    99:	 (179/255, 31/255,212/255),  # Es
    100: (179/255, 31/255,186/255),  # Fm
    101: (179/255, 13/255,166/255),  # Md
    102: (189/255, 13/255,135/255),  # No
    103: (199/255,  0/255,102/255),  # Lr
    104: (204/255,  0/255, 89/255),  # Rf
    105: (209/255,  0/255, 79/255),  # Db
    106: (217/255,  0/255, 69/255),  # Sg
    107: (224/255,  0/255, 56/255),  # Bh
    108: (230/255,  0/255, 46/255),  # Hs
    109: (235/255,  0/255, 38/255),  # Mt
}

# Atomic radius in picometers (from https://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page))
pm2bohr = 0.0188972599
atomic_radii = {
    1 :  53*pm2bohr,  # H
    2 :  31*pm2bohr,  # He
    3 : 167*pm2bohr,  # Li
    4 : 112*pm2bohr,  # Be
    5 :  87*pm2bohr,  # B
    6 :  67*pm2bohr,  # C
    7 :  56*pm2bohr,  # N
    8 :  48*pm2bohr,  # O
    9 :  42*pm2bohr,  # F
    10:  38*pm2bohr,  # Ne
    11: 190*pm2bohr,  # Na
    12: 145*pm2bohr,  # Mg
    13: 118*pm2bohr,  # Al
    14: 111*pm2bohr,  # Si
    15:  98*pm2bohr,  # P
    16:  88*pm2bohr,  # S
    17:  79*pm2bohr,  # Cl
    18:  71*pm2bohr,  # Ar
    19: 243*pm2bohr,  # K
    20: 194*pm2bohr,  # Ca
    21: 184*pm2bohr,  # Sc
    22: 176*pm2bohr,  # Ti
    23: 171*pm2bohr,  # V
    24: 166*pm2bohr,  # Cr
    25: 161*pm2bohr,  # Mn
    26: 156*pm2bohr,  # Fe
    27: 152*pm2bohr,  # Co
    28: 149*pm2bohr,  # Ni
    29: 145*pm2bohr,  # Cu
    30: 142*pm2bohr,  # Zn
    31: 136*pm2bohr,  # Ga
    32: 125*pm2bohr,  # Ge
    33: 114*pm2bohr,  # As
    34: 103*pm2bohr,  # Se
    35:  94*pm2bohr,  # Br
    36: 202*pm2bohr,  # Kr
    37: 265*pm2bohr,  # Rb
    38: 219*pm2bohr,  # Sr
    39: 212*pm2bohr,  # Y
    40: 206*pm2bohr,  # Zr
    41: 198*pm2bohr,  # Nb
    42: 190*pm2bohr,  # Mo
    43: 183*pm2bohr,  # Tc
    44: 178*pm2bohr,  # Ru
    45: 173*pm2bohr,  # Rh
    46: 169*pm2bohr,  # Pd
    47: 165*pm2bohr,  # Ag
    48: 161*pm2bohr,  # Cd
    49: 156*pm2bohr,  # In
    50: 145*pm2bohr,  # Sn
    51: 133*pm2bohr,  # Sb
    52: 123*pm2bohr,  # Te
    53: 115*pm2bohr,  # I
    54: 216*pm2bohr,  # Xe
    55: 298*pm2bohr,  # Cs
    56: 253*pm2bohr,  # Ba
    57: 226*pm2bohr,  # La
    58: 210*pm2bohr,  # Ce
    59: 247*pm2bohr,  # Pr
    60: 206*pm2bohr,  # Nd
    61: 205*pm2bohr,  # Pm
    62: 238*pm2bohr,  # Sm
    63: 231*pm2bohr,  # Eu
    64: 233*pm2bohr,  # Gd
    65: 225*pm2bohr,  # Tb
    66: 228*pm2bohr,  # Dy
    67: 226*pm2bohr,  # Ho
    68: 226*pm2bohr,  # Er
    69: 222*pm2bohr,  # Tm
    70: 222*pm2bohr,  # Yb
    71: 217*pm2bohr,  # Lu
    72: 208*pm2bohr,  # Hf
    73: 200*pm2bohr,  # Ta
    74: 193*pm2bohr,  # W
    75: 188*pm2bohr,  # Re
    76: 185*pm2bohr,  # Os
    77: 180*pm2bohr,  # Ir
    78: 177*pm2bohr,  # Pt
    79: 174*pm2bohr,  # Au
    80: 171*pm2bohr,  # Hg
    81: 156*pm2bohr,  # Tl
    82: 180*pm2bohr,  # Pb
    83: 143*pm2bohr,  # Bi
    84: 135*pm2bohr,  # Po
    85: 202*pm2bohr,  # At
    86: 220*pm2bohr,  # Rn
    87: 348*pm2bohr,  # Fr
}
