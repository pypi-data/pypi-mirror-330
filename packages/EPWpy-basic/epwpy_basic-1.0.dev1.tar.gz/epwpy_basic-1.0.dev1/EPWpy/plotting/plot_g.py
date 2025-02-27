import numpy as np
import matplotlib.pyplot as plt
from EPWpy.plotting.default_params import *


@set_plots
def plot_gkk_mode_q(ibnd,jbnd,g,ik = 0,**kwargs):

    default_kw = {}
    for key in default_kwargs().keys():
        if (key not in kwargs):
            if (default_kwargs()[key] !=None):
                default_kw[key] = default_kwargs()[key]

        else:
            default_kw[key] = kwargs[key]


    x=kwargs['x']
    if(x == None):
        x=np.linspace(0,1,len(g[ibnd,jbnd,0,0,:]))

    for data in (g[ibnd,jbnd,:,ik,:]):
        plt.plot(x,data, color=kwargs['color'],**default_kw)

@set_plots
def plot_gkk_mode_k(ibnd,jbnd,g,iq = 0,**kwargs):

    default_kw = {}
    for key in default_kwargs().keys():
        if (key not in kwargs):
            if (default_kwargs()[key] !=None):
                default_kw[key] = default_kwargs()[key]

        else:
            default_kw[key] = kwargs[key]


    x=kwargs['x']

    if(x == None):
        x=np.linspace(0,1,len(g[ibnd,jbnd,0,:,0]))

    for data in (g[ibnd,jbnd,:,:,iq]):
        plt.plot(x,data, color=kwargs['color'], **default_kw)


if __name__=="__main__":


    plot_gkk('epw.out')

