import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc
from matplotlib import rcParams

def color_pallette():
    colors={'airforceblue':[0.36, 0.54, 0.66],
               'antiquefuchsia':[0.57, 0.36, 0.51],
               'asparagus':[0.53, 0.66, 0.42],
               'beaver':[0.62, 0.51, 0.44],
               'bole':[0.47, 0.27, 0.23],
               'cadet':[0.33, 0.41, 0.47],
               'camouflagegreen':[0.47, 0.53, 0.42],
               'charcoal':[0.21, 0.27, 0.31],
               'darkcerulean':[0.03, 0.27, 0.49],
               'darkelectricblue':[0.33, 0.41, 0.47],
               'darkolivegreen':[0.33, 0.42, 0.18],
               'deepchestnut':[0.73, 0.31, 0.28],
               'feldgrau':[0.3, 0.36, 0.33],
               'frenchlilac':[0.53, 0.38, 0.56],
               'glaucous':[0.38, 0.51, 0.71],
               'lapislazuli':[0.15, 0.38, 0.61]}
    return(colors)

def default_kwargs():

    default_kwargs={'linewidth':2.0,
                    'linestyle':'-',
                    'alpha':1.0,
                    'marker': None,
                    'markerstyle':None}

    return(default_kwargs)

def default_for_kwargs():

    default_kwargs={'draw_arrow':False,
                    'grid':True,
                    'figsize':(5.0,5.0),
                    'fname':'plot',
                    'format':'pdf',
                    'fontsize':16,
                    'first': True}
    return(default_kwargs)


def set_plots(func):

    def inner(*args,**kwargs):
        
        

        for key in default_for_kwargs().keys():
            if (key not in kwargs.keys()):
                kwargs[key] = default_for_kwargs()[key]

        font = kwargs['fontsize']

        if ('style' in kwargs.keys()):

            if (kwargs['style'] == 'tex'):
                rc('text',usetex=True)
                rc('font',family='serif')
                mpl.rcParams['axes.linewidth'] = 1.5
                rcParams.update({'figure.autolayout': True}) 
                font = 16
             
        if (kwargs['first'] == True):
            fig = plt.figure(figsize=kwargs['figsize'])
        
        if (kwargs['grid'] == True):
            plt.grid()

        if ('xlabel' not in kwargs.keys()):
            plt.xlabel('Wavevector', fontsize = font)        
        else:
            plt.xlabel(kwargs['xlabel'], fontsize = font) 

        if ('ylabel' not in kwargs.keys()):
            plt.ylabel('$E$ [eV]',fontsize=font)        
        else:
            plt.ylabel(kwargs['ylabel'], fontsize = font)

        if ('xticks' not in kwargs.keys()): 
            plt.xticks(fontsize = font)
        else:
            if('xtick_pos' not in kwargs.keys()):
                leng = np.linspace(0,1,len(kwargs['xticks']))
            else:
                leng = kwargs['xtick_pos']
            kwargs['leng']=leng
            plt.xticks(leng,kwargs['xticks'],fontsize=font)

        if ('yticks' not in kwargs.keys()):
            plt.yticks(fontsize = font)
        else:
            if('ytick_pos' not in kwargs.keys()):
                pass
            else:
                lengy = kwargs['ytick_pos']
                kwargs['lengy'] = lengy

        if ('color' not in kwargs.keys()):
            kwargs['color'] = 'k'
        
        else:
            if(kwargs['color'] == 'EPWpy'):
                print(color_pallette()['asparagus'])
                kwargs['color'] = color_pallette()['asparagus']
 
        if ('color_c' not in kwargs.keys()):
            kwargs['color_c'] = 'k'
        
        else:
            if(kwargs['color_c'] == 'EPWpy'):
                print(color_pallette()['asparagus'])
                kwargs['color_c'] = color_pallette()['asparagus']
            
        if ('color_v' not in kwargs.keys()):
            kwargs['color_v'] = 'k'
        
        else:
            if(kwargs['color_v'] == 'EPWpy'):
                kwargs['color_v'] = color_pallette()['bole']
             
        if ('x' not in kwargs.keys()):            
            kwargs['x']=None

        func(*args,**kwargs)

        if ('legend' in kwargs.keys()):
            plt.legend(kwargs['legend'],fontsize = font-2, loc = 0)

        filename = kwargs['fname']
        frmt = kwargs['format']
 
        #plt.savefig(f'{filename}.{frmt}',dpi=200,format=kwargs['format'])
    #plt.show()
    #plt.close()    
    return inner

