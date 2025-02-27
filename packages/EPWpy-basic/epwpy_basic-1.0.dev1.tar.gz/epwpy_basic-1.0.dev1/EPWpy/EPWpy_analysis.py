import numpy as np
#import scipy
import os
from EPWpy.utilities.set_files import *
from EPWpy.utilities.constants import *
from EPWpy.utilities.kramers_kronig import *

class py_analysis:
    """
    Analysis class for EPW_py
    """
    def __init__(self,epw_fold='epw',
                      ph_fold = 'ph', 
                      scf_fold = 'scf',
                      nscf_fold = 'nscf',  
                      data=None): 
   
        self.data = data
        self.epw_fold = epw_fold
        self.scf_fold = scf_fold
        self.ph_fold = ph_fold
        self.nscf_fold = nscf_fold     

    @property
    def alpha(self):

        self.set_work()

        try:
            T=self.temp#default_epw_input['temps']
        except ValueError:

            print('key not found')

        if('lindabs' in self.epw_params.keys()):

            eps = np.loadtxt(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K.dat')
            #eps_dir = np.loadtxt(f'{self.epw_fold}/epsilon2_dirabs_'+str(T)+'K.dat')
 
        if('loptabs' in self.epw_params.keys()):

            eps = np.loadtxt(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K_'+self.epw_params['meshnum']+'.dat')

        alpha=eps[:,0]*eps[:,1]/(hbar*c*self.nr)

        self.set_home()

        return(alpha)
        
    @property
    def eps1(self):
        self.set_work()    
        T=self.temp

        if('lindabs' in self.epw_params.keys()):
            _,eps_real,_,_=calc_epr_real(f'{self.epw_file}/epsilon2_indabs_'+str(T)+'K.dat',self.eps0,100)

        if('loptabs' in self.epw_params.keys()): 
            _,eps_real,_,_=calc_epr_real(f'{self.epw_file}/epsilon2_indabs_'+str(T)+'K_'+self.epw_params['meshnum']+'.dat',self.eps0,100)
        self.set_home()

        return(eps_real)

    @property
    def nr(self,type_run='indabs'):

        self.set_work()

        T=self.temp#default_epw_input['temps']
        if('lindabs' in self.epw_params.keys()):
            nr,eps_real,_,_=calc_epr_real(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K.dat',self.eps0,100)
        if('loptabs' in self.epw_params.keys()):
            nr,eps_real,_,_=calc_epr_real(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K_'+self.default_epw_input['meshnum']+'.dat',self.eps0,100)
        self.set_home()

        return(nr)

    @property
    def eps2(self,type_run='indabs'):

        self.set_work()

        T=self.temp#default_epw_input['temps']
        if('lindabs' in self.epw_params.keys()):
            _,_,eps2,_=calc_epr_real(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K.dat',self.eps0,100)
        if('loptabs' in self.epw_params.keys()):
            _,_,eps2,_=calc_epr_real(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K_'+self.default_epw_input['meshnum']+'.dat',self.eps0,100)
        self.set_home()

        return(eps2)

    @property
    def omega(self,type_run='indabs'):

        self.set_work()
        T=self.temp#default_epw_input['temps']
        if('lindabs' in self.epw_params.keys()):
            _,_,_,omega=calc_epr_real(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K.dat',self.eps0,100)
        if('loptabs' in self.epw_params.keys()):
            _,_,_,omega=calc_epr_real(f'{self.epw_fold}/epsilon2_indabs_'+str(T)+'K_'+self.default_epw_input['meshnum']+'.dat',self.eps0,100)
        self.set_home()

        return(omega)

    @property
    def inv_tau(self):
        self.set_work()
        T=self.temp

        inv_tau=np.loadtxt(f'{self.epw_fold}/inv_tau.fmt')
        inv_tau[:,3]=inv_tau[:,3]*13.6
        inv_tau[:,4]=inv_tau[:,4]*20670.6944033

        self.set_home()

        return(inv_tau)

    @property
    def inv_taucb(self):
        self.set_work()
        T=self.temp

        inv_tau=np.loadtxt(f'{self.epw_fold}/inv_taucb.fmt')
        inv_tau[:,3]=inv_tau[:,3]*13.6
        inv_tau[:,4]=inv_tau[:,4]*20670.6944033

        self.set_home()

        return(inv_tau)

    @property
    def inv_tauvb(self):
        self.set_work()
        T=self.temp

        inv_tau=np.loadtxt(f'{self.epw_fold}/inv_tauvb.fmt')
        inv_tau[:,3]=inv_tau[:,3]*13.6
        inv_tau[:,4]=inv_tau[:,4]*20670.6944033

        self.set_home()

        return(inv_tau)

    @property
    def inv_taucb_freq(self):
        self.set_work()
        self.set_home()

    @property
    def abs_calc(self):
        system=self.system
        prefix=self.prefix

        fileimag =str(os.getcwd())+'/'+f"{system}/eps/epsi_{prefix}.dat"
        filereal =str(os.getcwd())+'/'+f"{system}/eps/epsr_{prefix}.dat"
        Ei, xi, yi, zi = np.loadtxt(fileimag, usecols=[0, 1, 2, 3], unpack=True,skiprows=2)
        Er, xr, yr, zr = np.loadtxt(filereal, usecols=[0, 1, 2, 3], unpack=True,skiprows=2)
        Im = (xi+yi+zi)/3
        Re = (xr+yr+zr)/3
        def abs(Er,Im,Re):
            h_cut = 6.58211915561E-16 # eV*s
            c = 299792458 # m/s
            delta = (np.sqrt(Re**2 + Im**2) - Re)#/2
            abs = (np.sqrt(2)/(h_cut*c))*Er*np.sqrt(delta)
            return abs
        output = open(str(os.getcwd())+'/'+f"{system}/eps/abs.dat", 'w')
        for i in range(0,len(Er),1):
            coef = abs(Er[i],Im[i],Re[i])
            print(Er[i],coef,file = output)
        output.close()

    @property
    def Eform(self):
        self.set_work()
        Ef = read_plrn(f'{self.epw_fold}/{self.epw_file}.out')
        self.set_home()
        return(Ef)    
       
    @property
    def ibte_mobility_e(self):
        self.set_work()
        _,ibte_mob = read_mobility(f'{self.epw_fold}/{self.epw_file}',float(self.epw_params['temps']))
        self.set_home()
        return(ibte_mob)              

    @property
    def serta_mobility_e(self):
        self.set_work()
        serta_mob,_ = read_mobility(f'{self.epw_fold}/{self.epw_file}',float(self.epw_params['temps']))        
        return(serta_mob)

    @property
    def ibte_mobility_h(self):
        self.set_work()
        _,ibte_mob = read_mobility(f'{self.epw_fold}/{self.epw_file}',float(self.epw_params['temps']),typ='Hole')
        self.set_home()
        return(ibte_mob)              

    @property
    def serta_mobility_h(self):
        self.set_work()
        serta_mob,_ = read_mobility(f'{self.epw_fold}/{self.epw_file}',float(self.epw_params['temps']),typ = 'Hole')        
        return(serta_mob)


    def set_home(self):
        os.chdir(self.home)

    def set_work(self):
        os.chdir(self.home+'/'+self.system)

def read_plrn(file1):

    with open(file1, 'r') as f: 
        for line in f:
            if( len(line.split())>0 ):
                if( line.split()[0] =='Formation'):    
                    Eform=float(line.split()[3])
    return(Eform)


def read_mobility(file1, T, typ='Elec'):

    read_mob_serta = False
    read_mob_ibte = False
    read_serta = False
    read_ibte = False
    serta_mob=np.zeros((3,3),dtype=float)
    ibte_mob=np.zeros((3,3),dtype=float)
    temp_found = False
    t = 0
    with open(f'{file1}.out', 'r') as f:

        for line in f:

            if ((len(line.split()) != 0) & (read_mob_serta == True)):
                try:
                    if((float(line.split()[0]) == T) & (t == 0)):
                        temp_found = True
                    if(temp_found == True):
                        serta_mob[t,:] = np.array(line.split()).astype(float)[-3:]
                        t +=1
                        if(t == 3):
                            read_mob_serta = False
                            read_serta = False
                            t = 0
                            temp_found = False 

                except ValueError:
                    pass
            if ((len(line.split()) != 0) & (read_mob_ibte == True)):            
                try:
                    if((float(line.split()[0]) == T) & (t == 0)):
                        temp_found = True
                    if(temp_found == True): 
                        ibte_mob[t,:] = np.array(line.split()).astype(float)[-3:]
                        t +=1
                        if(t == 3):
                            read_mob_ibte = False                    
                            t = 0
                            temp_found = False
                except ValueError:
                    pass                
            if ('SERTA' in line):
                read_serta = True 
            if ('Iteration number' in line):
                read_ibte = True
 
            if (f'Drift {typ} mobility' in line):
                if(read_serta == True) :
                    read_mob_serta = True
                elif(read_ibte == True):
                    read_mob_ibte = True


    f.close()    
    return(serta_mob, ibte_mob)
