import numpy as np
import os
import sys


def extract_total_energy(folder):
    tot_energy=0.0
    with open(folder,'r') as f:
        for line in f:
            read=line.strip().split()
            if(len(read)>2):
                if((read[0]=='total') & (read[1]=='energy')):
                    tot_energy=float(read[-2])
    f.close()
    return(tot_energy)
def extract_HUMO(folder):
    HUMO=0.0
    with open(folder,'r') as f:
        for line in f:
            read=line.strip().split()
            if(len(read)>2):
                if((read[0]=='highest') & (read[1]=='occupied')):
                    HUMO=float(read[-1])
    f.close()
    return(HUMO)
def extract_dielectric(folder):
    eps=0.1
    t=0
    with open(folder,'r+') as f:
        for line in f:
            read=line.strip()
            print(read)
            read=line.strip().split()
            if(len(read)>2):
                if(read[0]=='Dielectric'):
                    t=1 
            if(t>0):
                t +=1
            if(t==4):
                eps=float(line.strip().split()[1])
    f.close()
    return(eps)
def extract_epsilon(folder):
    eps=np.loadtxt(str(folder))
    return(eps)

def match_benchmark(benchmark,tot_energy,thr=1E-4):
    if(abs(benchmark-tot_energy) < thr):
        return(True)
    else:
        return(False)

if __name__=='__main__':
    eps=extract_epsilon('epsilon2_indabs_300.0K.dat')
  #  print(np.shape(eps))    
    print(np.sum(eps[:,1]))
