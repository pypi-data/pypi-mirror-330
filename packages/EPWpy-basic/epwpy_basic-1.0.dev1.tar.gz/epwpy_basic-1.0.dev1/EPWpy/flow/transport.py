import numpy as np

from EPWpy.EPWpy_prepare import py_prepare
from EPWpy.EPWpy_run import py_run
from EPWpy.QE.PW_util import find_fermi

class flow_manager(py_prepare, py_run):

    def __init__(self, data = None):

        self.data = data
    
    def scf_to_ph_flow(func):

        def inner(self):

            self.run_serial = True
            #print(self.flow_parallelization)
            self.prepare(1,type_run = 'scf')
            if ('scf' not  in self.dont_do):
                self.run(self.procs,type_run = 'scf',parallelization = self.flow_parallelization[0])
            self.prepare(1,type_run = 'nscf')
            if ('nscf' not  in self.dont_do):
                self.run(self.procs,type_run = 'nscf',parallelization = self.flow_parallelization[1])
            self.prepare(1,type_run = 'ph')
            if ('ph' not  in self.dont_do):
                self.run(self.procs,type_run = 'ph',parallelization = self.flow_parallelization[2])
            func(self)

        return inner

    @scf_to_ph_flow
    def transport_flow(self):
        self.EPWpy_info(message=f'Inside transport flow\nIn this mode EPWpy calculates transport coefficient in one shot\nCarefully check the final .json files inside \'{self.prefix}\' folder')
        epwin={}
        data = self._set_fine_transport()
        
        self.epw(name='epw1')
        self.prepare(1,type_run='epw1')

        if ('epw1' not  in self.dont_do):
            self.run(self.procs,'epw1')        
 
        epwin = self._set_epwin_transport(data)

        self.epw(epwin,name='epw2')
        self.prepare(1,type_run='epw2')
        self.run(self.procs,'epw2')

        return(None)

    @scf_to_ph_flow
    def optics_flow(self):
        self.EPWpy_info(message=f'Inside Optics flow\nIn this mode EPWpy calculates imaginary dielectric constant in one shot\nCarefully check the final .json files inside \'{self.prefix}\' folder')
        epwin={}
        data = self._set_fine_optics()
        
        self.epw(name='epw1')
        self.prepare(1,type_run='epw1')

        if ('epw1' not  in self.dont_do):
            self.run(self.procs,'epw1')        
 
        epwin = self._set_epwin_optics(data)

        self.epw(epwin,name='epw2')
        self.prepare(1,type_run='epw2')
        self.run(self.procs,'epw2')

        return(None)
    
    def _set_epwin_transport(self,data):

        nkf1 = data['nkf1']
        nkf2 = data['nkf2']
        nkf3 = data['nkf3']
        nqf1 = data['nqf1']
        nqf2 = data['nqf2']
        nqf3 = data['nqf3']
        
        if('etf_mem' not in data.keys()):
            if(nkf1*nkf2*nkf3 == nqf1*nqf2*nqf3):
                data['etf_mem'] = 3
                data['efermi_read'] = '.true.'
                data['fermi_energy'] =  find_fermi(f'{self.prefix}/{self.scf_fold}/{self.scf_file}.out')
            
            else:
                data['etf_mem'] = 1
   
        if ('ncarrier' in data.keys()):
            pass
        else:
            data['ncarrier'] = '1E13'
            print('setting a default carrier concentration of 1E13 for ncarrier')
         
        if ('hole_mobility' in self.epw_params.keys()): 
            data['ncarrier'] += '-'
 
        
        epwin={'scattering':'.true.',
               'int_mob':'.false.',
               'iterative_bte':'.true.',
               'carrier':'.true.',
               'mp_mesh_k':'.true.',
               'degaussw':0,
               'clean_transport': None,
               'nkf1':nkf1,
               'nkf2':nkf2,
               'nkf3':nkf3,
               'nqf1':nqf1,
               'nqf2':nqf2,
               'nqf3':nqf3}
        epwin.update(data) 
        self.EPWpy_info('Setting epw inputs as',data=epwin)
        return(epwin)

    def _set_epwin_optics(self,data):

        nkf1 = data['nkf1']
        nkf2 = data['nkf2']
        nkf3 = data['nkf3']
        nqf1 = data['nqf1']
        nqf2 = data['nqf2']
        nqf3 = data['nqf3']
            
        data['etf_mem'] = 1
        
        epwin={'loptabs':'.true.',
               'mp_mesh_k':'.true.',
               'degaussw':0,
               'clean_transport': None,
               'nkf1':nkf1,
               'nkf2':nkf2,
               'nkf3':nkf3,
               'nqf1':nqf1,
               'nqf2':nqf2,
               'nqf3':nqf3}
        epwin.update(data) 
        self.EPWpy_info('Setting epw inputs as',data=epwin)
        return(epwin)



    def _set_fine_transport(self):
        try:
            if (self.epw_params['nkf1'] == None):
                self.EPWpy_exit('no fine grid defined in EPW')              
        except KeyError:
            self.EPWpy_exit('no fine grid defined in EPW')
        data={}

        data['nkf1'] = self.epw_params['nkf1']
        data['nkf2'] = self.epw_params['nkf2']
        data['nkf3'] = self.epw_params['nkf3']
        data['nqf1'] = self.epw_params['nqf1']
        data['nqf2'] = self.epw_params['nqf2']
        data['nqf3'] = self.epw_params['nqf3']

        self.epw_params['nkf1']=None
        self.epw_params['nkf2']=None
        self.epw_params['nkf3']=None
        self.epw_params['nqf1']=None
        self.epw_params['nqf2']=None
        self.epw_params['nqf3']=None

        if ('ncarrier' in self.epw_params.keys()):
            data['ncarrier'] = self.epw_params['ncarrier']
            del self.epw_params['ncarrier']

        if ('efermi_read' in self.epw_params.keys()):
            data['efermi_read'] = self.epw_params['efermi_read']
        else:
            data['efermi_read'] = None

        if ('fermi_energy' in self.epw_params.keys()):
            data['fermi_energy'] = self.epw_params['fermi_energy']
        else:
            data['fermi_energy'] = find_fermi(f'{self.prefix}/{self.scf_fold}/{self.scf_file}.out')

        if ('fsthick' in self.epw_params.keys()):
            data['fsthick'] = self.epw_params['fsthick']
        else:
            data['fsthick'] = 0.5             
        if ('etf_mem' in self.epw_params.keys()):
            data['etf_mem'] = self.epw_params['etf_mem']
            self.epw_params['etf_mem'] = 0
        if ('mp_mesh_k' in self.epw_params.keys()):
            data['mp_mesh_k'] = self.epw_params['mp_mesh_k']
            del self.epw_params['mp_mesh_k']
        if ('temps' in self.epw_params.keys()):
            data['temps'] = self.epw_params['temps']
            del self.epw_params['temps']
 
        if ('nstemp' in self.epw_params.keys()):
            data['nstemp'] = self.epw_params['nstemp']
            del self.epw_params['nstemp']
 
        return(data)

    def _set_fine_optics(self):
        try:
            if (self.epw_params['nkf1'] == None):
                self.EPWpy_exit('no fine grid defined in EPW')              
        except KeyError:
            self.EPWpy_exit('no fine grid defined in EPW')
        data={}

        data['nkf1'] = self.epw_params['nkf1']
        data['nkf2'] = self.epw_params['nkf2']
        data['nkf3'] = self.epw_params['nkf3']
        data['nqf1'] = self.epw_params['nqf1']
        data['nqf2'] = self.epw_params['nqf2']
        data['nqf3'] = self.epw_params['nqf3']

        self.epw_params['nkf1']=None
        self.epw_params['nkf2']=None
        self.epw_params['nkf3']=None
        self.epw_params['nqf1']=None
        self.epw_params['nqf2']=None
        self.epw_params['nqf3']=None

        if ('omegamin' in self.epw_params.keys()):
            data['omegamin'] = self.epw_params['omegamin']
            del self.epw_params['omegamin']

        if ('omegamax' in self.epw_params.keys()):
            data['omegamax'] = self.epw_params['omegamax']
            del self.epw_params['omegamax']

        if ('omegastep' in self.epw_params.keys()):
            data['omegastep'] = self.epw_params['omegastep']
            del self.epw_params['omegastep']

        if ('efermi_read' in self.epw_params.keys()):
            data['efermi_read'] = self.epw_params['efermi_read']
        else:
            data['efermi_read'] = '.true.'

        if ('fermi_energy' in self.epw_params.keys()):
            data['fermi_energy'] = self.epw_params['fermi-energy']
        else:
            data['fermi_energy'] = find_fermi(f'{self.prefix}/{self.scf_fold}/{self.scf_file}.out')

        if ('fsthick' in self.epw_params.keys()):
            data['fsthick'] = self.epw_params['fsthick']
        else:
            data['fsthick'] = 4.5             

        return(data)
                

if __name__=="__main__":
    flowm=flow_manager()
    flowm.transport_flow 

