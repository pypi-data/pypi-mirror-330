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


def plot_band_eig(fname):
    Band=[]
    t=0
    Band_tmp=[]
    with open(fname,'r') as f:
        AA=[]
        KK=[]
        for line in f:
            if(len(line.split())>1):

                if((len(line.split())>3) & (line.split()[0] !='k') & (line.split()[0] !='&plot')):
                    for i in range(len(line.split())):
                        try:
                            AA.append(float(line.split()[i]))
                        except ValueError:
                            continue

                elif(((len(line.split())==3) | (line.split()[0]=='k')) & (len(AA)>0)):
                    Band.append(AA)
                    AA=[]
                    KK=[]
        if (len(AA) > 0):
            Band.append(AA)
    Band=np.array(Band)
    return(Band)



def plot_band_scf(fname):
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
    #print(np.shape(Band))
    return(Band)

@set_plots
def plot_xy(*args,**kwargs):
    """
    plotting function for a general xy
    """

    for key in default_kwargs().keys():
        if (key not in kwargs):
            if (default_kwargs()[key] !=None):
                default_kw[key] = default_kwargs()[key]

        else:
            default_kw[key] = kwargs[key]


    x=args[0]
    y=args[1]

    for i in range(len(Band[0,:])):

            plt.plot(x,Band[:,i],color=kwargs['color'],**default_kw)

@set_plots
def plot_band_prod(*args,**kwargs):

    Band=args[0]
    ef0=kwargs['ef0']
    x=kwargs['x']
    t=0
    val=-100000
    val_k=0
    con=100000
    con_k=0
    con_b=0
    con_b2=0
    con_k2=0
    val_b=0
    low=0#44
    high=8
    default_kw = {}
    kwargs['fname']='bandstructure'
    for key in default_kwargs().keys():
        if (key not in kwargs):
            if (default_kwargs()[key] !=None):
                default_kw[key] = default_kwargs()[key]

        else:
            default_kw[key] = kwargs[key]

    if(x == None):
        x=np.linspace(0,1,len(Band[:,0]))

    for i in range(len(Band[0,:])):

        for j in range(len(Band[:,i])):
            if((Band[j,i]-ef0>=val) and (Band[j,i]<ef0)):
               val=Band[j,i]-ef0
               val_k=x[j]
               val_b=i
               con_b2=j
            if((Band[j,i]-ef0<=con) and (Band[j,i]>ef0)):
               con=Band[j,i]-ef0
               con_k=x[j]
               con_b=i
    for i in range(len(Band[0,:])):
        if(i>val_b):

            l1 = plt.plot(x,Band[:,i]-ef0,color=kwargs['color_c'],**default_kw)
        else:

            l1 = plt.plot(x,Band[:,i]-ef0,color=kwargs['color_v'],**default_kw)

    if (kwargs['draw_arrow'] == True):
        plt.scatter(con_k,con,color='r',s=100.0)
        plt.scatter(val_k,val,color='black',s=100.0)
        plt.arrow(val_k,val,(con_k-val_k),(con-val),width=0.01,length_includes_head=True,head_width=0.1)

@set_plots
def plot_band_freq(*args,**kwargs):
    Band=args[0]#['Band']
    x=kwargs['x']

    if(x == None):
        x=np.linspace(0,1,len(Band[:,0]))

    for i in range(len(Band[0,:])):

            plt.plot(x,Band[:,i],color=kwargs['color'])

def read_exp(file):
    EXP=[]
    with open (file,'r') as f:
        for line in f:
            EXP_temp=[]
            for i in range(len(line.split())-2):
                try:
                    EXP_temp.append(float(line.split()[i]))
                except ValueError:
                    EXP_temp.append(1e-3)
                    print('nothing')
            if(len(EXP_temp)>0):
               EXP.append(EXP_temp)
    f.close()

    EXP=np.array(EXP)
    Exp_energy=(2*c*hbar*(math.pi/(EXP[:,0]*1*10**-7)))
    Exp_alpha=EXP[:,1]
    return(Exp_energy,Exp_alpha)

def open_sup(file):
    A=[]
    with open(file,'r') as f:
        next(f)
        for line in f:
            A.append(np.array(line.split()).astype(float))
    return(np.array(A))

