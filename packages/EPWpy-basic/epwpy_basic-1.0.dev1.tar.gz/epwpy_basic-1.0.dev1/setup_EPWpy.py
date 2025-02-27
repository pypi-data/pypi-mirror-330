import argparse
import os
from setuptools import setup

#with open("README.md", 'r') as f:
 #   long_description = f.read()

setup(
    name='EPWpy-basic',
    version='1.0.dev1',
    description='A Python wrapper for EPW',
    license="BSD",
#    long_description=open('README.md').read(),
#    long_description_content_type='text/x-rst',
    author='Sabyasachi Tiwari',
    author_email='sabyasachi.tiwari@austin.utexas.edu',
    package_dir = {'EPWpy' : 'EPWpy',
                  'EPWpy.QE' : 'EPWpy/QE',
                  'EPWpy.BGW' : 'EPWpy/BGW',
                  'EPWpy.utilities' : 'EPWpy/utilities',
                  'EPWpy.default' : 'EPWpy/default',
                  'EPWpy.structure' : 'EPWpy/structure',
                  'EPWpy.error_handling' : 'EPWpy/error_handling',
                  'EPWpy.flow':'EPWpy/flow',
                  'EPWpy.plotting':'EPWpy/plotting',
                  'EPWpy.Abinit':'EPWpy/Abinit'},
    url="https://epwpy.org",
    packages=['EPWpy','EPWpy/QE','EPWpy/BGW','EPWpy/utilities','EPWpy/default','EPWpy/structure',
             'EPWpy/error_handling','EPWpy/flow','EPWpy/plotting','EPWpy/Abinit'],  #same as name
    install_requires=['wheel', 
                      'alive-progress'],
    extras_require ={'materials_project':['mp-api'],
                     'visualization':['mayavi'],
                     'automatic_pseudo':['requests']} #external packages as dependencies
    )


