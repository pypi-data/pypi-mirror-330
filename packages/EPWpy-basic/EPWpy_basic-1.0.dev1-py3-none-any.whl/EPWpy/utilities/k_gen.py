import numpy as np
import math
import os

def k_mesh(h,k,l,kx,ky,kz):
     kk=[]
#     print(len(h),len(k),len(l))
     leng=len(h)*len(k)*len(l)
     for i in range(len(h)):
       for j in range(len(k)):
         for m in range(len(l)):

            #kk.append(np.dot(h[i],kx)+np.dot(k[j],ky)+np.dot(l[m],kz))
            kk.append([h[i],k[j],l[m],round(1.0/(leng),6)])
            #print 'here'

     return(kk)
def k_path(K, leng, kx, ky, kz):
    KK=np.zeros((sum(leng)-2,3),dtype=float)
    kk=[]
    t=0
    for i in range(len(leng)):
       k1=np.linspace(K[i][0],K[i+1][0],leng[i],endpoint=True)
       k2=np.linspace(K[i][1],K[i+1][1],leng[i],endpoint=True)
       k3=np.linspace(K[i][2],K[i+1][2],leng[i],endpoint=True)
       for j in range(leng[i]-1):
           KK[t,0]=k1[j]
           KK[t,1]=k2[j]
           KK[t,2]=k3[j]
           #kk.append(np.dot(KK[t,0],kx)+np.dot(KK[t,1],ky)+np.dot(KK[t,2],kz))
           kk.append([round(KK[t,0],3),round(KK[t,1],3),round(KK[t,2],3),round(1.0/sum(leng),3)])
           t=t+1
#    print kk
    return(kk)

if __name__ =='__main__':

#       K=[[0,0.0,0],[0,0.5,0],[0.66,0.33,0.00],[0,0,0]]
        K=[[0.5,0.0,0.5],[0,0,0],[0.5,0.25,0.75],[0,0,0]]
        leng=[101,101,101]
        K=k_path(K,leng, kx, ky, kz)
        np.savetxt('k_path.txt',K,fmt='%1.3f')
        mesh=6
        h=np.linspace(0.0,1,mesh,endpoint=False)
        k=np.linspace(0.0,1,mesh,endpoint=False)
        l=np.linspace(0.0,1,1)

        k=k_mesh(h,k,l,kx,ky,kz)

        np.savetxt('k_mesh.txt',k,fmt='%1.3f')

