import numpy as np
import os


def read_scf_out(file,string):

    T=False
    with open(file,'r') as f:
        for line in f:
            if string in line.strip():
                T=True
            else:
                if (T):
                    continue
                
    f.close()
    return(T) 





if __name__=='__main__':
    cwd=str(os.getcwd())
    read_scf_out(cwd+'/si/nscf/nscf.out','job')        
