import numpy as np
import os
#from os import *

class write_BGW_files:
   
    def __init__(self,write):

        self.write=write
    

    def write_epsilon(self,epsilonin={}):
        with open('epsilon.inp', 'w') as f:
            for key in self.BGW_epsilon.keys():
                if(key not in epsilonin):
                    f.write(str(key)+' '+str(self.BGW_epsilon[key])+'\n')
            for key in epsilonin.keys():
                    f.write(str(key)+' '+str(epsilonin[key])+'\n')
            f.write('begin qpoints\n')
            for j in range(len(self.GW_ks[:,0])):
                for l in range(3):
                    f.write(' '+str(self.GW_ks[j,l])+'  ')
                if(j==0):
                    f.write('1.0'+' '+'1.0\n')
                else:
                    f.write('1.0'+' '+'0.0\n')
            f.write('end\n')
            
        f.close()

    def write_sigma(self,sigmain={}):
        with open('sigma.inp', 'w') as f:
            for key in self.BGW_sigma.keys():
                if(key not in sigmain):
                    f.write(str(key)+' '+str(self.BGW_sigma[key])+'\n')
            for key in sigmain.keys():
                    f.write(str(key)+' '+str(sigmain[key])+'\n')
            f.write('begin kpoints\n')
            for j in range(len(self.GW_k[:,0])):
                for l in range(3):
                    f.write(' '+str(self.GW_k[j,l])+'  ')
                f.write('1.0'+'\n')
            f.write('end\n')
        f.close()

    def write_kernel(self,kernelin={}):
        with open('kernel.inp', 'w') as f:
            for key in self.BGW_kernel.keys():
                if(key not in kernelin):
                    f.write(str(key)+' '+str(self.BGW_kernel[key])+'\n')
            for key in kernelin.keys():
                    f.write(str(key)+' '+str(kernelin[key])+'\n')
        f.close()

    def write_absorption(self,absorptionin={}):
        with open('absorption.inp', 'w') as f:
            for key in self.BGW_absorption.keys():
                if(key not in absorptionin):
                    f.write(str(key)+' '+str(self.BGW_absorption[key])+'\n')
            for key in absorptionin.keys():
                    f.write(str(key)+' '+str(absorptionin[key])+'\n')
        f.close()

    def write_pw2bgw(self,pw2bgw={}):
        prefix=self.prefix.replace('\'','')
        with open(str(prefix)+'.pw2bgw','w') as f:
            f.write('&input_pw2bgw\n')
            f.write('prefix = '+str(self.prefix))
            f.write('\n') 
            for key in self.BGW_pw2bgw:
                f.write(str(key)+' = '+str(self.BGW_pw2bgw[key]))
                f.write('\n')
            f.write('/')
        f.close()
    def write_sig2wan(self,sig2wan={}):
        prefix=self.prefix.replace('\'','')
        with open('sig2wan.inp','w') as f:
            f.write('sigma_hp.log\n') 
            for key in self.BGW_sig2wan:
                f.write(str(self.BGW_sig2wan[key]))
                f.write('\n')
            f.write(str(self.prefix)+'.nnkp\n')
            f.write(str(self.prefix)+'.eig\n')
 
        f.close()

