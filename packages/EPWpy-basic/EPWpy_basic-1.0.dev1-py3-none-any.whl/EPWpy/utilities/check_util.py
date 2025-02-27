import numpy as np


def datatyp(A):

    if (type(A) == type(int(1))):
        return('int')

    elif (type(A) == type(float(1))):
        return('float')

    elif (type(A) == type([1])):
        return('list')

    elif (type(A) == type(np.array([1]))):
        return('array')

    elif (type(A) == type('a')):
        return('str')
 
    elif (type(A) == type(1.0+1j)):
        return('cmplx')

    elif (type(A) == type(np.array([int(1)])[0])):
        return('np_int')

    elif (type(A) == type(np.array([1.0])[0])):
        return('np_float')
 
    else:
        return(None)

    
if __name__=="__main__":

    A=None
    if (datatyp(A)) == None:
        print('found none')
    print(type(np.array([1.0])[0]))
    print(datatyp(np.array([1.0])[0]))
