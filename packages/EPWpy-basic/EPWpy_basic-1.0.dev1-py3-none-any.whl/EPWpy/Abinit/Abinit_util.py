# Author: Samuel Ponc\'e
# Date: 02/07/2024
# Converter of quadrupole tensor from Abinit to EPW format (Quadrupole.fmt). 

import numpy as np

class Abinit_utilities:
    """ 
    This is the utility class for abinit interface 
    """

    def __init__(self, folder = 'abinit',file = 'input'):
        """ 
        Utility class for Abinit
        """
        self.fold = folder
        self.file = file

    def quadrupole(self):
        """
        writes the quadrupole.fmt file
        """
        abinit2epw(f'./{self.fold}/{self.file}')

def abinit2epw(filename):
    quad = np.zeros((4,3,3,3)) # atoms, direction, efield, qgrad

    # Read the input file
    user_input = filename
    AB_file = user_input#.strip()

    with open(f'{AB_file}.abo','r') as N:
        for lines in N:
            tmp = lines.split()
            if (len(tmp) < 1):
                continue
            if (tmp[0] == 'natom' and len(tmp) == 2):
                natom = int(tmp[1])
                break
    N.close()
    quad = np.zeros((natom,3,3,3)) # atoms, direction, efield, qgrad

    Found = 0
    with open(f'{AB_file}.abo','r') as N:
        for lines in N:
            tmp = lines.split()
            if (len(tmp) < 1):
                continue
            if (tmp[0] == 'Quadrupole'):
                Found = 1
                continue
            if (tmp[0] == 'efidir' and Found == 1):
                Found = 2 
                continue
            if (Found == 2 and tmp[0] == 'Electronic'):
                Found = 0
                continue
            if (Found == 2):
              at = int(tmp[1]) - 1
              dirc = int(tmp[2]) - 1 
              efield = int(tmp[0]) - 1
              qgrad = int(tmp[3]) - 1
              val  = float(tmp[4])
              if np.absolute(val) < 1E-6:
                  val = 0.0
              quad[at,dirc,efield,qgrad] = val
    N.close()
    print('  atom   dir       Qxx             Qyy         Qzz          Qyz            Qxz         Qxy')

    for ii in np.arange(natom):
        at = ii
        dirc = 0
        print('  %3i   %3i    %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f'%(at+1, dirc+1, quad[at,dirc,0,0], quad[at,dirc,1,1], quad[at,dirc,2,2], quad[at,dirc,1,2], quad[at,dirc,0,2], quad[at,dirc,0,1],))

        at = ii
        dirc = 1
        print('  %3i   %3i    %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f'%(at+1, dirc+1, quad[at,dirc,0,0], quad[at,dirc,1,1], quad[at,dirc,2,2], quad[at,dirc,1,2], quad[at,dirc,0,2], quad[at,dirc,0,1],))

        at = ii
        dirc = 2
        print('  %3i   %3i    %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f'%(at+1, dirc+1, quad[at,dirc,0,0], quad[at,dirc,1,1], quad[at,dirc,2,2], quad[at,dirc,1,2], quad[at,dirc,0,2], quad[at,dirc,0,1],))

    with open('quadrupole.fmt','w') as f:
        f.write('  atom   dir       Qxx             Qyy         Qzz          Qyz            Qxz         Qxy\n')

        for ii in np.arange(natom):
            at = ii
            dirc = 0
            f.write('  %3i   %3i    %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f'%(at+1, dirc+1, quad[at,dirc,0,0], quad[at,dirc,1,1], quad[at,dirc,2,2], quad[at,dirc,1,2], quad[at,dirc,0,2], quad[at,dirc,0,1],))
            f.write('\n')
            at = ii
            dirc = 1
            f.write('  %3i   %3i    %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f'%(at+1, dirc+1, quad[at,dirc,0,0], quad[at,dirc,1,1], quad[at,dirc,2,2], quad[at,dirc,1,2], quad[at,dirc,0,2], quad[at,dirc,0,1],))
            f.write('\n')
            at = ii
            dirc = 2
            f.write('  %3i   %3i    %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f'%(at+1, dirc+1, quad[at,dirc,0,0], quad[at,dirc,1,1], quad[at,dirc,2,2], quad[at,dirc,1,2], quad[at,dirc,0,2], quad[at,dirc,0,1],))
            f.write('\n')


