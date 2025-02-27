import subprocess as sp



def set_links(cwd):

        sp.Popen('ln -s '+cwd+'/GW/wfn/wfn.cplx    '+cwd+'/GW/epsilon/WFN',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfnq/wfn.cplx  '+cwd+'/GW/epsilon/WFNq',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfn/vxc.dat     '+cwd+'/GW/sigma/vxc.dat',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfn/rho.cplx    '+cwd+'/GW/sigma/RHO',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfn/wfn.cplx    '+cwd+'/GW/sigma/WFN_inner',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/eps0mat '+cwd+'/GW/sigma',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/epsmat  '+cwd+'/GW/sigma',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/eps0mat.h5 '+cwd+'/GW/sigma',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/epsmat.h5 '+cwd+'/GW/sigma',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfn/wfn.cplx '+cwd+'/GW/kernel/WFN_co',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/eps0mat '+cwd+'/GW/kernel',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/epsmat '+cwd+'/GW/kernel',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/eps0mat.h5 '+cwd+'/GW/kernel',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/epsmat.h5 '+cwd+'/GW/kernel',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfn/wfn.cplx '+cwd+'/GW/absorption/WFN_co',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfnfi/wfn.cplx '+cwd+'/GW/absorption/WFN_fi',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/wfnqfi/wfn.cplx '+cwd+'/GW/absorption/WFNq_fi',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/eps0mat '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/epsmat '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/kernel/bsedmat '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/kernel/bsexmat '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/eps0mat.h5 '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/epsilon/epsmat.h5 '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/kernel/bsemat.h5 '+cwd+'/GW/absorption',shell=True)
        sp.Popen('ln -s '+cwd+'/GW/sigma/sigma_hp.log '+cwd+'/GW/sig2wan',shell=True)
 
