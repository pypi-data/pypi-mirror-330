import numpy as np
import time
from alive_progress import alive_bar
import sys

def decorated_init_print(func):
    def inner(*args, **kwargs):

        if ('name' in kwargs.keys()):
            print('inside', kwargs[name])

        func(*args,**kwargs)
    return inner

def decorated_status(func):
    def inner(*args, **kwargs):

        for i in range(30): print('--',end=" ") 
        print()
        func(*args,**kwargs)
        print()
        for i in range(30): print('--',end=" ")
        print() 
    return inner


def decorated_progress(func):
    def inner(*args, **kwargs):
        if ('name' in kwargs.keys()):
            definition = kwargs['name']        
        else:
            definition = 'scf'
 
        for i in range(11): print('--',end=" ") 
        print(f' Calculation: {definition} ',end=" ") 
        for i in range(11): print('--',end=" ") 
        print() 
        with alive_bar(2, title = f'Running {definition}', force_tty=True, monitor = False) as bar:  # your expected total
            bar()
            time.sleep(0.005)
            func(*args,**kwargs)    
            bar()                 # call `bar()` at the end
        print()
        for i in range(30): print('--',end=" ") 
        print() 
    return inner

def decorated_structure(func):
    def inner(*args, **kwargs):
        if ('name' in kwargs.keys()):
            definition = kwargs['name']        
        else:
            definition = 'random'
 
        for i in range(12): print('--',end=" ") 
        print('Structure Info',end=" ")
        for i in range(13): print('--',end=" ") 
        print() 
        func(*args,**kwargs)    
        for i in range(30): print('--',end=" ") 
        print()
    return inner

def decorated_warning(func):
    def inner(*args, **kwargs):
        try:
            warn = args[0].__dict__['epw_refresh']
            if (warn !=None):
                for i in range(13): print('--',end=" ") 
                print('Warning',end=" ")
                for i in range(14): print('--',end=" ")             
                print()
                print('Refreshing EPW input (remove refresh from epw_save.json if not needed)')
                for i in range(30): print('--',end=" ") 
                print()
 
        except KeyError:
            pass
        func(*args,**kwargs)    
    return inner

def decorated_exit(func):
    def inner(*args, **kwargs):
        for i in range(13): print('--',end=" ") 
        print(' Exit ',end=" ")
        for i in range(14): print('--',end=" ")             
        print()
        func(*args,**kwargs)    
        for i in range(30): print('--',end=" ") 
        print()
        sys.exit()
    return inner

def decorated_info(func):
    def inner(*args, **kwargs):
        for i in range(13): print('--',end=" ") 
        print(' Info ',end=" ")
        for i in range(14): print('--',end=" ")             
        print()
        func(*args,**kwargs)    
        for i in range(30): print('--',end=" ") 
        print()
    return inner

def decorated_warning_pw(func):
    def inner(*args, **kwargs):
        func(*args,**kwargs)    
        try:
            X=args[0].__dict__['epw_params']['lpolar']
            try:
                Y=args[0].__dict__['epw_params']['system_2d']
            except KeyError:
                pass
            for i in range(13): print('--',end=" ") 
            print('Info',end=" ")
            for i in range(14): print('--',end=" ")             
            print()
            print('Based on previous pw and ph calculations some parameters are set below')
            print(f'lpolar: ', args[0].__dict__['epw_params']['lpolar'],'(related to epsil in ph)')
            try:
                print(f'system_2d: ', args[0].__dict__['epw_params']['system_2d'],'related to assume_isolated in pw')
            except KeyError:
                pass
            for i in range(30): print('--',end=" ") 
            print()
        except KeyError:
            pass
    return inner

def decorated_warning_transport(func):
    def inner(*args, **kwargs):
        func(*args,**kwargs)    
        try:
            for i in range(13): print('--',end=" ") 
            print('Info',end=" ")
            for i in range(14): print('--',end=" ")             
            print()
            print('You have chosen transport calculation with values below')
            print(f'ncarrier: ', args[0].__dict__['epw_params']['ncarrier'])
            print(f'int_mob: ', args[0].__dict__['epw_params']['int_mob'])
            print(f'scattering: ', args[0].__dict__['epw_params']['scattering'])
            print(f'degaussw: ', args[0].__dict__['epw_params']['degaussw'],'(adaptive smearing)')
            for i in range(30): print('--',end=" ") 
            print()
        except KeyError:
            pass
    return inner

def decorated_warning_optics(func):
    def inner(*args, **kwargs):
        func(*args,**kwargs)    
        try:
            for i in range(13): print('--',end=" ") 
            print('Info',end=" ")
            for i in range(14): print('--',end=" ")             
            print()
            print('You have chosen optics calculation with values below')
            print(f'loptabs: ', args[0].__dict__['epw_params']['loptabs'])
            print(f'omegamax: ', args[0].__dict__['epw_params']['omegamax'],' eV')
            print(f'omegamin: ', args[0].__dict__['epw_params']['omegamin'],' eV')
            print(f'omegastep: ', args[0].__dict__['epw_params']['omegastep'],' eV')
            print(f'efermi_read: ', args[0].__dict__['epw_params']['efermi_read'])
            print(f'fermi_energy: ', args[0].__dict__['epw_params']['fermi_energy'],' eV')
            for i in range(30): print('--',end=" ") 
            print() 
        except KeyError:
            pass
    return inner

