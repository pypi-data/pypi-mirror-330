import numpy as np
#from scipy.interpolate import interp1d

def calc_epr(file_inp):
    A=np.loadtxt(file_inp)
    omega= A[:,0]
    eps2 = A[:,1]
    eps1=np.zeros((len(A[:,1]),1),dtype=float)
    omega_calc=omega
    nr=[]
    dw=omega[2]-omega[1]   
    for i in range(len(omega_calc)):
        for j in range(len(omega)):
            if(omega[j]!=omega_calc[i]):
                eps1[i]=eps1[i]+((2.0*dw/np.pi)*omega[j]*eps2[j]/(omega[j]**2-omega_calc[i]**2))
        eps1[i] = eps1[i]+1.0

        nr.append(np.sqrt(np.sqrt(eps1[i]**2+eps2[i]**2)+eps2[i])/np.sqrt(2))
    return(nr,eps1,eps2)

def calc_epr_real(file_inp,T,N,f='ind'):
    A=np.loadtxt(file_inp)
    omega= A[:,0]
    eps2 = A[:,1]
    omega_inp=np.linspace(min(omega),max(omega),N)
	#eps2_n=interp1d(omega,eps2)
    eps2_inp= np.interp(omega_inp,omega,eps2)      #eps2_n(omega_inp)
    nr=[]
    dw=omega_inp[2]-omega_inp[1]
    eps1=np.zeros((len(omega_inp),1),dtype=float)
#    print(omega_inp,eps2_inp)
    for i in range(len(omega_inp)):
        for j in range(len(omega_inp)):
            if(omega_inp[j]!=omega_inp[i]):
                eps1[i]=eps1[i]+((2.0*dw/np.pi)*omega_inp[j]*eps2_inp[j]/(omega_inp[j]**2-omega_inp[i]**2))
        eps1[i] = eps1[i]+T
        nr.append(np.sqrt(np.sqrt(eps1[i]**2+eps2_inp[i]**2)+eps2_inp[i])/np.sqrt(2))
    return(nr,eps1,eps2_inp,omega_inp)
