import numpy as np
import os
""" For bandstructure related properties """

def extract_band_eig(fname):
    """
    Extract the bandstructure from  .eig file
    Input
        fname (str): filename of .eig file
    Output
        Band (array): Bandstructre with first index k and second band (Band(k,n))
    """
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

def extract_band_scf(fname):
    """
    Extract the bandstructure from  scf.out file 
    Input
        fname (str): filename of .out file
    Output
        Band (array): Bandstructre with first index k and second band (Band(k,n))
    """
    Band=[]
    t=0
    Band_tmp=[]
    dec=1000
    with open(fname,'r') as f:
        AA=[]
        KK=[]
        for line in f:
            L=line.split()
            if ('occupation numbers' in line):
                dec = 1500
            if (len(line.split())>1) & (dec == 1500):
                if (line.split()[0] == 'k'):
                    dec = 0
            if(len(L)>2):          
                if(((L[0]=='Writing')&(L[2]=='to')) | ('highest occupied' in line)):
                    dec=1000
            if((len(line.split())>1) & (dec == 0)):    
                if (line.split()[0] != 'k'):
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
                if (('End of band' in line) | ('End of self-consistent' in line)):
                    dec=0

    if(len(AA)>0):
        Band.append(AA)
    Band=np.array(Band)
    return(Band)

def extract_band_dat(fname):
    """
    Extract the bandstructure from  .dat file (usually Wannier90)
    Input
        fname (str): filename of .dat file
    Output
        Band (array): Bandstructre with first index band and second k (Band(n,k))
    """
    Band=[]
    t=0
    Band_tmp=[]

    with open(fname,'r') as f:

        for line in f:
            AA=[]
            K=[]
            for i in range(len(line.split())):
                AA.append(float(line.split()[i]))
                #A.append(float(line.split()[0]))
            if(len(AA)!=0):

        
                Band_tmp.append(AA[1])
                if(t==0):
                    K.append(AA[0])
            else:
                Band.append(Band_tmp)
                Band_tmp=[]
                if(t==0): 
                    t=1
                  
    Band=np.array(Band)
    return(Band)

if __name__=='__main__':
    cwd=str(os.getcwd())
    B=extract_band_scf(cwd+'/si/nscf/nscf.out') 
    print(B)
