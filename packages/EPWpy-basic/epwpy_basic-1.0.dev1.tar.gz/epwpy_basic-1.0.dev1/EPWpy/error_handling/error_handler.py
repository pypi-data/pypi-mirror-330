import numpy as np
from EPWpy.utilities.read_QE import *
from EPWpy.utilities.printing import *
import sys

class job_status:

    def __init__(self):
        """
        This class is meant to handle errors and return job status for EPWpy
        """

    @decorated_status    
    def get_QE_status(self):
        """This function obtains if the QE code has finished normally"""
        out=read_scf_out(self.file,"JOB DONE")   
        if(out==True):
            print('Calculation finished normally in '+str(self.file))
        else:
            print('Error in calculation '+str(self.file))
            self.print_out() 
        return(out)

    @decorated_status    
    def get_EPW_status(self):
        """This function obtaines if the EPW code has finished normally"""
        out = read_scf_out(self.file,"functionality-dependent EPW.bib file.")
        if(out == True):
            print('Calculation finished normally in '+str(self.file))
        else:
            print('Error in calculation '+str(self.file))
            self.print_out() 
        return(out)

    @decorated_status    
    def get_Wannier_PP_status(self, string='none'):
        """ This function obtaines if wannier code has finished normally """
        out = read_scf_out(self.file, "nnkp written.")
        if(out == True):
            print('Calculation finished normally in '+str(self.file))
        else:
            print('Error in calculation '+str(self.file))
       #     self.print_out() 
        return(out)

    @decorated_exit
    def EPWpy_exit(self,error_message='Unknown error'):
        print(error_message)

    @decorated_info
    def EPWpy_info(self, message='Unknown info',data={}):
        print(message)
        if (len(data) != 0):
            for key in data.keys():
                D = data[key]
                print(f'{key}: {D}')

    def print_out(self):
        with open(self.file,'r') as f:
            for line in f:
                print(line)

@decorated_info
def error_mayavi():
    print('Mayavi not found')
    print('To Visualize structure, Wannier functions, and Polaron wavefunctions, install mayavi')
    print('Mayavi can be installed with EPWpy using\npip install EPWpy-basic[visualization]')

@decorated_info
def error_dash():
    print('Dash-bio and plotly not found')
    print('To Visualize molecules, install dash-bio')
    print('Dash-bio is optional for EPWpy')


@decorated_info
def error_mp():
    print('Materials project API (mp-api) not found')
    print('To directly use the mp-api ID for structure download, install mp-api')
    print('To build EPWpy with mp-api\npip install EPWpy-basic[materials_project]')




