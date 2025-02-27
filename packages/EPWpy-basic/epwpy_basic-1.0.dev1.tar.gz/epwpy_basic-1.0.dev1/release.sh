#!/bin/bash 
# Author: Sabyasachi Tiwari (sabyasachi.tiwari@austin.utexas.edu)

# Notes: 
#   Only launch this bash script when creating a new release for EPWpy    
#   Before this bash script is launched, change the version of EPWpy inside setup_EPW.py
#   The upload will require the API key which is not public

python setup.py install --withQE True --installed True --Release True

#twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose
twine upload dist/* --verbose





