import numpy as np
#import matplotlib.pyplot as plt
import argparse
import math
import cmath
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

def shuffle_ar(atom_pos,natoms,ntot):
    import random 
    N=int(natoms[-1])
    aa=[]

    for i in range(N):
        aa.append(i+int(ntot)-N)
  
        aa=np.array(aa)
        aa=random.sample(aa,len(aa))
        atom_pos2=np.zeros((len(aa),3),dtype=float)
    for i in range(len(aa)):
        l=i+ntot-N

        atom_pos2[i,:]=atom_pos[aa[i],:]
    atom_pos[ntot-N:ntot,:]=atom_pos2[:,:]
    return(atom_pos)

def unit2prim(lattice_vec):

    a = np.sqrt(lattice_vec[0,0]**2 + lattice_vec[0,1]**2 + lattice_vec[0,2]**2)

    return(a,lattice_vec[:,:]/a)


def add_atoms(atom_pos,pos_new):
    pos_new=pos_new.astype('int')
    N=len(atom_pos[:,0])
    atom_pos2=np.zeros((N,3),dtype=float)
    for i in range(N):
      atom_pos2[i,:]=atom_pos[i,:]
    for i in range(len(pos_new)):
        T=atom_pos[N-i-1,:]
        B=atom_pos[pos_new[i]-1,:]
        atom_pos2[pos_new[i]-1,:]=T
        atom_pos2[N-i-1,:]=B
    return atom_pos2

def gen_POSCAR(lattice_vec,atom_pos,natoms,material):

    with open('POSCAR_new','w') as f:
      f.write(' system\n')
      f.write(' 1\n')   
      f.write('   '+str(lattice_vec[0,0])+'   '+str(lattice_vec[0,1])+'   '+str(lattice_vec[0,2])+'\n')
      f.write('   '+str(lattice_vec[1,0])+'   '+str(lattice_vec[1,1])+'   '+str(lattice_vec[1,2])+'\n')
      f.write('   '+str(lattice_vec[2,0])+'   '+str(lattice_vec[2,1])+'   '+str(lattice_vec[2,2])+'\n')
      f.write('   '+material+'\n')
      f.write('   '+str(natoms)+'\n')
      f.write('   Direct\n')
      for i in range(len(atom_pos[:,0])):    
          f.write('    '+str(atom_pos[i,0])+'    '+str(atom_pos[i,1])+'    '+str(atom_pos[i,2])+'\n')

def gen_xyz(atom_pos,natoms,mat):

    with open('xyz','w') as f:
      f.write(str(sum(natoms))+'\n')
      f.write('Molecule (in Angstrom)\n')
      for i in range(len(atom_pos[:,0])):    
          f.write(str(mat[i])+'    '+str(atom_pos[i,0])+'    '+str(atom_pos[i,1])+'    '+str(atom_pos[i,2])+'\n')



def dist(A,B):
    d=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2+(A[2]-B[2])**2)
    return d

def anglecalc(Bx,By,x_pos,y_pos):

    X=(Bx-x_pos)
    Y=(By-y_pos)          
    if ((Y>=0)&(X<0)):
      angle=-math.atan((-Y/X))+math.radians(180)
    elif((Y<=0)&(X<0)):
      angle=math.atan(((-Y)/(-X)))+math.radians(180)
    elif((Y<=0)&(X>0)):
      angle=-math.atan(-Y/X)+math.radians(360)
    else:
      try:
          angle=math.atan(Y/X)
      except RuntimeWarning:
          angle=0
    if(np.isnan(angle)==True): 
        angle=math.radians(90)
    return(angle)

def angle(A,B):
    D=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
    if((A[0]**2+A[1]**2)>(B[0]**2+B[1]**2)):
        phi_xz=anglecalc(0,B[2],D,A[2])
    else: 
        phi_xz=anglecalc(D,B[2],0,A[2])
    phi_xy=anglecalc(B[0],B[1],A[0],A[1])
    phi_yz=anglecalc(B[1],B[2],A[1],A[2])
    return([phi_xy,phi_xz,phi_yz])

def mat_calc(atom_pos,natoms,materials):

    near_neigh=[]
    mat=[]
    l=0
    prev=0
    for i in range(len(atom_pos[:,0])):
      B=[]
      if(i>=natoms[l]+prev):
        prev=prev+natoms[l]
        l=l+1
      if(i<(natoms[l]+prev)):
        mat.append(materials[l])

    return(mat)

def N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond,min_bond2,control):
    #from .globvar import Repeat_vec as L
    L=np.array([[0,0,0],[0,1,0],[1,0,0],[-1,0,0],[0,-1,0],[1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]
              ,[0,0,1],[0,1,1],[1,0,1],[-1,0,1],[0,-1,1],[1,1,1],[1,-1,1],[-1,1,1],[-1,-1,1]
              ,[0,0,-1],[0,1,-1],[1,0,-1],[-1,0,-1],[0,-1,-1],[1,1,-1],[1,-1,-1],[-1,1,-1],[-1,-1,-1]])

    N_near_neigh=[]
    N_bond=[]
    N_angle=[]
    N_occ=[]
    l=0
    prev=0  
    for i in range(len(atom_pos2[:,0])):
      B=[]
      Bd=[]
      angle2=[]
      occ=[]
      van_der=[]
      for j in range(len(atom_pos2[:,0])):
          t=0 
          for m in range(len(L[:,0])):

            blength=dist(atom_pos2[i,:],atom_pos2[j,:]+L[m,0]*lattice_vec[0,:]*a+L[m,1]*lattice_vec[1,:]*a+L[m,2]*lattice_vec[2,:]*a)
            angle3=angle(atom_pos2[i,:],atom_pos2[j,:]+L[m,0]*lattice_vec[0,:]*a+L[m,1]*lattice_vec[1,:]*a+L[m,2]*lattice_vec[2,:]*a)

            if((blength<min_bond2)&(blength>min_bond)): #&(j!=i)): last_change
              t=t+1
              if j not in B:        
               
                B.append(j)
                Bd.append(blength)     
                angle2.append(angle3)       
                  
          occ.append(t)               

      N_near_neigh.append(B)
      N_bond.append(Bd)
      N_angle.append(angle2)
      N_occ.append(occ)
    if control==1:

      return(N_near_neigh)     
    elif control==2:
      return(N_bond)   
    elif control==3:
      return(N_angle)     
    elif control==4:
      return(N_occ)
    elif control==5:
      return(N_near_neigh,N_bond,N_angle,N_occ)

def main_extract(min_bond,file_POSCAR,T=1,direc_1=0,direc_2=1):
    natoms2=0
    lattice_vec=np.zeros((3,3),dtype=float)
    with open(file_POSCAR) as f:
      j=0
      for line in f:
     
        if(j==1):
          a=float(line.split()[0])
        elif((j>1)&(j<5)):
          lattice_vec[j-2,0]=float(line.split()[0])
          lattice_vec[j-2,1]=float(line.split()[1])
          lattice_vec[j-2,2]=float(line.split()[2])
        elif(j==5):
          materials=np.array(line.split())
        elif(j==6):
          natoms=np.array(line.split()).astype('int')
          for i in range(len(natoms)):
            natoms2=natoms[i]+natoms2
          atom_pos=np.zeros((natoms2,3),dtype=float)
        elif((j>7)&(j<8+natoms2)):
          atom_pos[j-8,0]=float(line.split()[0])
          atom_pos[j-8,1]=float(line.split()[1])
          atom_pos[j-8,2]=float(line.split()[2])
      
        j=j+1
    mat_typ=int(len(materials))
    atom_pos2=np.zeros((len(atom_pos[:,0]),len(atom_pos[0,:])),dtype=float)

    for j in range(len(atom_pos[:,0])):
      atom_pos2[j,:]=atom_pos[j,0]*lattice_vec[0,:]*a+atom_pos[j,1]*lattice_vec[1,:]*a+atom_pos[j,2]*lattice_vec[2,:]*a
  
    mat=mat_calc(atom_pos,natoms,materials)  

    near_neigh=[]
    near_bond=[]
    near_angle=[]
    near_occ=[]
    for i in range(len(min_bond)-1):
      # Here we obtain all near-neighbor mappings ##########
      N1,N2,N3,N4=N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],5)
      near_neigh.append(N1)
      near_bond.append(N2)
      near_angle.append(N3)
      near_occ.append(N4)
    near_neigh=np.array(near_neigh)
    near_bond=np.array(near_bond)
    near_angle=np.array(near_angle)
    near_occ=np.array(near_occ)
    if(T==5):
      print(materials)
      N_plot_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[0],min_bond[1],1,materials,mat,direc_1,direc_2)
    if(T==2):
      return(atom_pos2,mat,near_neigh,near_bond,near_angle,materials,natoms,near_occ,lattice_vec,a)
    elif(T==3):
      return(near_occ)
    elif(T==1):
      return(atom_pos,atom_pos2,lattice_vec,mat,materials,natoms,a)

def main_extract_co_opt(structure,min_bond,T=1):
    natoms2=0
    lattice_vec=np.zeros((3,3),dtype=float)

    with open(str(structure)+'/POSCAR') as f:
      j=0
      for line in f:

        if(j==1):
            a=float(line.split()[0])

        elif((j>1)&(j<5)):
            lattice_vec[j-2,0]=float(line.split()[0])
            lattice_vec[j-2,1]=float(line.split()[1])
            lattice_vec[j-2,2]=float(line.split()[2])
        elif(j==5):
            materials=np.array(line.split())
        elif(j==6):
            natoms=np.array(line.split()).astype('int')

            for i in range(len(natoms)):
                natoms2=natoms[i]+natoms2
            atom_pos=np.zeros((natoms2,3),dtype=float)
        elif((j>7)&(j<8+natoms2)):
            atom_pos[j-8,0]=float(line.split()[0])
            atom_pos[j-8,1]=float(line.split()[1])
            atom_pos[j-8,2]=float(line.split()[2])

        j=j+1
    mat_typ=int(len(materials))
    atom_pos2=np.zeros((len(atom_pos[:,0]),len(atom_pos[0,:])),dtype=float)

    for j in range(len(atom_pos[:,0])):
      atom_pos2[j,:]=atom_pos[j,0]*lattice_vec[0,:]*a+atom_pos[j,1]*lattice_vec[1,:]*a+atom_pos[j,2]*lattice_vec[2,:]*a

    mat=mat_calc(atom_pos,natoms,materials)
    near_neigh=[]
    near_bond=[]
    near_angle=[]
    near_occ=[]
    # Nearest neighbour calculation
    for i in range(len(min_bond)-1):

        near_neigh.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],1))

        near_bond.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],2))

        near_angle.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],3))
        near_occ.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],4))
    near_neigh=np.array(near_neigh)
    near_bond=np.array(near_bond)
    near_angle=np.array(near_angle)
    near_occ=np.array(near_occ)

    if(T==5):
      print(materials)
      N_plot_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[0],min_bond[1],1,materials,mat,direc_1,direc_2)
    if(T==2):
      return(atom_pos2,mat,near_neigh,near_bond,near_angle,materials,natoms,near_occ,lattice_vec,a)
    elif(T==3):
      return(near_occ)
    elif(T==1):
      return(atom_pos2,mat,near_neigh,near_bond,near_angle,materials,natoms)

