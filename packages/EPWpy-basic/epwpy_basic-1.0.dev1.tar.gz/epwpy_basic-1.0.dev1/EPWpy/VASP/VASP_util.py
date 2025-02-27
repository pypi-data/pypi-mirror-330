# Author: Sabyasachi Tiwari
# Date: 02/17/2025

import numpy as np
import xml.etree.ElementTree as ET

class VASP_utilities:
    """ 
    This is the utility class for abinit interface 
    """

    def __init__(self, folder = 'vasp',file = 'input'):
        """ 
        Utility class for Abinit
        """
        self.fold = folder
        self.file = file

    def bands(self):
        """
        reads EIGENVAL file of VASP
        """
        return(read_EIGENVAL(f'{self.fold}'))

    def efermi(self):
        """
        reads fermi level from vasprun.xml
        """
        return(read_Fermi(f'{self.fold}'))

def read_EIGENVAL(filename):
    t = 0
    with open(f'{filename}/EIGENVAL', 'r') as f:
        band = []
        for line in f:
            if (t == 5):
                print(line.split())    
                nband = int(line.split()[-1])
                nkpt = int(line.split()[-2])
            
            if (t > 6):
                if ((len(line.split()) == 4) | (len(line.split()) == 0)):
                    pass
                else:
                    band.append(float(line.split()[-2]))
                                
            t +=1
    f.close()
    band = np.array(band).reshape(nkpt,nband)
    return(band)    

def read_Fermi(filename):
    """Reads and parses an XML file, then prints the tag and text of each element.

    Args:
        file_path (str): The path to the XML file.
    """

    with open(filename, "r", encoding="utf-8") as file:
        xml_content = file.read()

        try:
            root = ET.fromstring(xml_content)
            efermi = root.find(".//i[@name='efermi']")
            if efermi is not None:
                print("Efermi value:", efermi.text.strip())
            else:
                print("Efermi not found")
        except ET.ParseError as e:
            print("XML Parsing Error:", e)

    return(float(efermi.text.strip()))
