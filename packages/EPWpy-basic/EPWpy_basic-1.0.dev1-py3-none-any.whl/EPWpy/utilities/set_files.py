import numpy as np
import os

class set_dir:
    "class to set the directories"
    def __init__(self,data):
        self.data=data

    def set_home(self):
        os.chdir(self.home)

    def set_work(self):
        os.chdir(self.home+'/'+self.system)

    def makedir(self,filein):
        try:
            os.mkdir(filein)
        except OSError:
            pass 
    def changedir(self,directory):
        os.chdir(directory)

    def set_folds(self, name, type_run, ins):
        """ sets the folders for methods """

        
        if (type_run == 'scf'):
            self.scf_fold = name
            ins.scf_fold = self.scf_fold
            self.state.update({'scf_fold': self.scf_fold})

        if (type_run == 'bs'):
            self.bs_fold = name
            ins.scf_fold = self.scf_fold
            self.state.update({'bs_fold':self.bs_fold})

        if (type_run == 'nscf'):
            self.nscf_fold = name
            ins.scf_fold = self.scf_fold
            ins.nscf_fold = self.nscf_fold
            self.state.update({'nscf_fold':self.nscf_fold})

           
        if (type_run == 'ph'):
            self.ph_fold = name
            ins.scf_fold = self.scf_fold
            ins.ph_fold = self.ph_fold
            self.state.update({'ph_fold':self.ph_fold})

        if (type_run == 'epw1'):
            if (name == 'epw1'):
                name = 'epw'
            self.epw_fold = name
            ins.scf_fold = self.scf_fold
            ins.nscf_fold = self.nscf_fold
            ins.ph_fold = self.ph_fold
            ins.epw_fold = self.epw_fold
            self.state.update({'epw_fold':self.epw_fold})

        else:
            ins.scf_fold = self.scf_fold
            try:
                ins.nscf_fold = self.nscf_fold
            except AttributeError:
                pass

            try:
                ins.ph_fold = self.ph_fold
            except AttributeError:
                pass

            try:
                ins.epw_fold = self.epw_fold
            except AttributeError:
                pass

       
