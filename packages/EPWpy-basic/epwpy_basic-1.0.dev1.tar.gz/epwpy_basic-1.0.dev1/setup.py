import argparse
import os
from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

parser = argparse.ArgumentParser()
parser.add_argument('--configs', type=str,nargs='*', required = False,default= ' ')
parser.add_argument('--cores', type=str, default= '1', required = False)
parser.add_argument('--withQE', type=bool,default = False, required = False)
parser.add_argument('install', type=None)
parser.add_argument('--installed', type=bool,default = False, required = False)
parser.add_argument('--Release', type=bool, default = False, required = False)
args = parser.parse_args()
print(args.configs)
cmd = None
if (args.withQE):
    print('Building with QE')
    os.system('mkdir build')
    os.chdir('build')
    if (args.installed == False):
        os.system('wget https://gitlab.com/epw/q-e/-/archive/EPW-5.9s/q-e-EPW-5.9s.tar.gz && tar xfz q-e-EPW-5.9s.tar.gz')
    os.chdir('q-e-EPW-5.9s')
    configs = ' '
    for i in range(len(args.configs)):
        configs += f'--{args.configs[i]} '
    if (args.installed == False):
        os.system(f'./configure {configs}')
        os.system(f'make epw -j {args.cores}')
    cmd = os.getcwd()
    os.chdir('../../')
with open('EPWpy/default/code_loc.py','w') as f:
    if (cmd == None):
        f.write(f'code_set = {cmd}')
    else:
        f.write(f'code_set = \'{cmd}/bin\'')

if (args.Release):
    os.system('python setup_EPWpy.py sdist bdist_wheel')
else:
    os.system('python setup_EPWpy.py install')


