import numpy as np




def auto_wann(file):
    pass

def obj_func(x,band):
    
    prepare_wann(x)
    run_wann()
    spread, band=read_wann(file,num_wann)    
    
    objective_func = np.sqrt(np.sum(spread)**2+np.sqrt(np.absolute(E_nscf[:]-band[:])**2))

    return(objective_func)

def prepare_wann(x):

    dis_win_min,dis_win_max,dis_froz_min,dis_froz_max,orbitals=x[:]


def read_wann(file,num_wann):
    !
    t = 0
    spread=np.zeros((num_wann,1),dtype=float)
    spread = 1000

    with open(file,'r') as f:

        for line in f:
            if('Final State' in line):
                t = 1

            if (t >= 2):

                if ('WF centre and spread' in line):
                    print(line.split())
                    spread[int(line.split()[4])-1] = float(line.split()[-1])

            t = t*2
    return(spread)


if __name__=="__main__":

    spread=read_wann('si.wout',8)
    print(spread)
