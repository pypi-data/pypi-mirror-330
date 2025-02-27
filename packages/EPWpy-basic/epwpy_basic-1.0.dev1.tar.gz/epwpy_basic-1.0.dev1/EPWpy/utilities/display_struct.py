import numpy as np
import urllib.request as urlreq
from EPWpy.utilities.EPW_util import get_connections
from EPWpy.default.default_colors import *
from EPWpy.error_handling import error_handler

try:
    from mayavi import mlab
    from mayavi.modules.iso_surface import IsoSurface
    from tvtk.api import tvtk
except ImportError:
    error_handler.error_mayavi()
#    print('The mayavi package not found\nTo visualize crystals in EPWpy, install mayavi')
try:
    import plotly
    import plotly.graph_objs as go
    from dash import Dash, dcc, html, Input, Output, callback
    import dash_bio as dashbio
    from dash_bio.utils import xyz_reader
except ImportError:
    error_handler.error_dash()
#    print('Dash-bio not found\nDash-bio not needed unless you want to use molecular view (not-recommended)')



def get_preset_view():   
    preset={
        'resolution': 400,
        'ao': 0.1,
        'outline': 1,
        'atomScale': 0.25,
        'relativeAtomScale': 0.33,
        'bonds': True
        }
    return(preset)

def read_xyz():
    with open('xyz','r') as f:
        data = f.read()#.replace('\n', '')
    return(data)


def display_atoms(atom_pos):

    plotly.offline.init_notebook_mode()

    # Configure the trace.
    trace = go.Scatter3d(
        x=atom_pos[:,0],  # <-- Put your data instead
        y=atom_pos[:,1],  # <-- Put your data instead
        z=atom_pos[:,2],  # <-- Put your data instead
        mode='markers',
        marker={
            'size': 10,
            'opacity': 0.8,
        }
    )

    # Configure the layout.
    layout = go.Layout(
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    data = [trace]

    plot_figure = go.Figure(data=data, layout=layout)

    # Render the plot.
    plotly.offline.iplot(plot_figure)
    #plot_figure.show()

def display_molecule(view={}):#atom_pos):

    plotly.offline.init_notebook_mode()


    app = Dash(__name__)


    data = read_xyz()
    #print(data)
    
    if (len(view) == 0):
        set_view = get_preset_view()
    else:
        set_view = view

    data = xyz_reader.read_xyz(datapath_or_datastring=data, is_datafile=False)

    app.layout = html.Div([
        dcc.Dropdown(
            id='default-speck-preset-views',
            options=[
                {'label': 'Ball and stick', 'value': 'stickball'},
                {'label': 'Default', 'value': 'default'}
           ],
            value='stickball'
        ),
        dashbio.Speck(
        id='default-speck',
        data=data,
        view=set_view
        #presetView = 'stickball'
        ),
        ])
    #print(data)

    #app.run(debug=True)
    #app.run(jupyter_mode="external",port=1234)
    return(app)

#try:
 #   @callback(
  #      Output('default-speck', 'presetView'),
   #     Input('default-speck-preset-views', 'value##'))
#except NameError:
 #   pass    

def update_preset_view(preset_name):
    return preset_name


def display_crystal(data, view = {}, bond_length=3.5):
    """
    Displays a crystal structure using the provided data and visualization parameters.

    Args:
        data (dict): The crystal structure data, typically in the form of an atomic 
                      structure object or a compatible data format.
        view (dict, optional): A dictionary specifying the viewing parameters, such as 
                               camera angle, zoom level, or rendering style. Defaults to an empty dictionary.
        bond_length (float, optional): The maximum bond length threshold for visualizing 
                                       atomic bonds. Defaults to 3.5.

    Returns:
        None: Displays the crystal structure visualization.

    Example:
        >>> display_crystal(my_crystal_data, view={'angle': 45}, bond_length=4.0)
    """
    # Take the data
    atomic_positions = data['positions']
    mat = data['mat']
    connections = get_connections(atomic_positions[:,0],atomic_positions[:,1],atomic_positions[:,2], bond_length)
    #print(connections)
    bond_color = (0.8,0.8,0)
    if ('bond_color' in view.keys()):
        bond_color = view['bond_color']

    bond_radius = 0.15
    if ('bond_radius' in view.keys()):
        bond_radius = view['bond_radius']

    if ('verbosity' in data.keys()):
        verbosity = data['verbosity']

    # Initializing mayavi with a backend

    if ('in_notebook' in view.keys()):
        if('backend' in view.keys()):
            mlab.init_notebook(backend = view['backend'])
        else:
            mlab.init_notebook()
 
    # Initialize figure
    mlab.figure('EPWpy',bgcolor=(1,1,1),size=(800, 600))

    # Plot atomic positions with jmol colors and atomic radius-based size
    length = len(np.array(atomic_positions))
    X = []
    Y = []
    Z = []
    for i,atom in enumerate(atomic_positions):
        x, y, z = atom
        # Get atomic number
        atom_number = atomic_number.get(mat[i], 12)
        #print(atom)
        # Get jmol color for the atomic number
        color = jmol_colors.get(atom_number, (0.5, 0.5, 0.5))  # Default to gray if not in map
        # Get atomic radius (if available) and adjust the size accordingly
        radius =  atomic_radii.get(atom_number, 50*pm2bohr)  # Default to 50 pm if not in the map
        size = (radius / 2) # Scale size for visibility
        # Print atomic info for the user
        #if (verbosity > 2):
         #   print(f"Atom: {atom_number}, Position: ({x}, {y}, {z}), Radius: {radius} bohr")
        X.append(x)
        Y.append(y)
        Z.append(z)
        src =  mlab.points3d(x, y, z, color=color, scale_factor=size)               
 
    src =  mlab.points3d(X, Y, Z, color=(0,0,0), scale_factor=0.0)#size)               
    src.mlab_source.dataset.lines = np.array(connections)
    tube = mlab.pipeline.tube(src, tube_radius = bond_radius)
    tube.filter.radius_factor = 1.
    mlab.pipeline.surface(tube, color= bond_color)

 
    if ('in_notebook' in view.keys()):
       return(src)#mlab.points3d(x, y, z, color=color, scale_factor=size))
    else:
        mlab.show()

if __name__ == '__main__':
    #app = Dash(__name__)
    draw_molecule()

    #app.run(debug=True)

