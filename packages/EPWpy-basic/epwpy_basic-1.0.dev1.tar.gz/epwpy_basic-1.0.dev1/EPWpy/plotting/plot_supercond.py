import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import re
import fnmatch
import os

from EPWpy.utilities.constants import CM2MEV

def get_fermi(prefix):
    pattern = "Fermi | highest"
    with open(f"./{prefix}/scf/scf.out") as text_file:
        for line in text_file:
            if re.search(pattern, line):
                print(line)
                ef = None
                for i in range(12, 15):  # Try slices 12, 13, and 14
                    try:
                        ef = float(line.split(' ')[i])
                        break  # Exit the loop if successful
                    except IndexError:
                        pass  # Continue to the next slice if IndexError occurs
                    except ValueError:
                        ef = None  # Handle the case where the value cannot be converted to float
                if ef is not None:
                    return ef  # Return the value if successfully extracted

def get_sym_points(prefix):
    points=[]
    with open(f"./{prefix}/bs/bands.out") as text_file:
        for line in text_file:
            if re.search("coordinate", line):
                #get last entry and remove trailing \n at end
                #print(line.split(' ')[-1].strip())
                points.append(float(line.split(' ')[-1].strip()))
    return(points)

def band_plot(prefix, xticks, ylim=(-15, 15), type_run='nscf_tetra'):
    fig, (bnd, dos) = plt.subplots(1, 2, sharey=True, \
            gridspec_kw={'width_ratios':[4, 1]})
    #fig.subplots_adjust(wspace=0)
    fig.subplots_adjust(wspace=0.06, hspace=0.06)

    # Load data from bands.dat.gnu
    bandData = np.loadtxt(f'./{prefix.lower()}/bs/bands.dat.gnu')
    k = np.unique(bandData[:, 0])
    bands = np.reshape(bandData[:, 1], (-1, len(k)))
    if type_run=='nscf':
        dosData = np.loadtxt(f'./{prefix.lower()}/nscf/{prefix.lower()}.dos')
    else:
        dosData = np.loadtxt(f'./{prefix.lower()}/nscf_tetra/{prefix.lower()}.dos')
    energy = dosData[:, 0]
    density = dosData[:, 1]

    ef = get_fermi(prefix)

    # Plot band structure
    for band in range(len(bands)):
        bnd.plot(k, bands[band, :]-ef, c='b')

    # Plot dotted line at Fermi energy
    bnd.axhline(0, c='red', ls=':')   

    # Add the x and y-axis labels
    bnd.set_ylabel('Energy$-$E$_F$ (eV)')

    # Label high-symmetry points
    bnd.set_xticks(get_sym_points(prefix), xticks)
    bnd.grid(visible=True, axis='x')
    bnd.set_xlim(0, k[-1])
    bnd.set_ylim(ylim)
    bnd.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

    # Plot DOS
    dos.plot(density, energy - ef, c='b')

    # Set axis limits
    windowFactor = 1.05
    dos.set_xlim(0, np.max(density) * windowFactor)
    dos.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

    # Plot dotted line at Fermi energy
    dos.axhline(0, c='red', ls=':')   

    #dos.set_xticks([])
    dos.set_xlabel('DOS (States/eV)')

    # Save figure to PDF
    plt.savefig(f"./{prefix}_band_dos.pdf")

    # Show figure
    plt.show()
    plt.close()

def phonon_plot(prefix, xticks):
    fig, (phonon, dos) = plt.subplots(1, 2, sharey=True, \
            gridspec_kw={'width_ratios':[4, 1]})
    fig.subplots_adjust(wspace=0.08)

    # Load data from file
    ## Note:  Band energies have unit cm^-1 in these files
    phononData = np.loadtxt(f'./{prefix.lower()}/ph/{prefix.lower()}.freq.gp')
    qPoints = phononData[:, 0]
    bands = phononData[:, 1:] * CM2MEV

    dosData = np.loadtxt(f'./{prefix.lower()}/ph/{prefix.lower()}.dos')
    frequency = dosData[:, 0] * CM2MEV
    density = dosData[:, 1]

    # Plot phonon dispersion
    for band in range(len(bands[0])):
        phonon.plot(qPoints, bands[:, band], c='b')

    # Set the axis limits
    windowFactor = 1.05
    phonon.set_xlim(0, qPoints[-1])
    phonon.set_ylim(np.min(bands) * windowFactor, np.max(bands) * windowFactor)
    phonon.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

    # Add the y-axis label
    phonon.set_ylabel('$\omega$ (meV)')

    # Label high-symmetry points
    phonon.set_xticks(get_sym_points(prefix), xticks)
    phonon.grid(visible=True, axis='x')
    if phonon.get_ylim()[0] != 0 :
        phonon.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
        dos.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)

    # Plot DOS
    dos.plot(density, frequency, c='b')

    # Set axis limits
    dos.set_xlim(0, np.max(density) * windowFactor)
    dos.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

    #dos.set_xticks([])
    dos.set_xlabel(r'PhDOS(meV$^{-1}$)')


    # Save figure to PDF
    plt.savefig(f"./{prefix}_phonons.pdf")

    # Show figure
    plt.show()
    plt.close()
    
##### get the q-path for phonon selfenergy and nesting function plot
def get_qpath(prefix, input_file=None, output_file=None, pattern=None):
    """
    Processes the input file to find lines matching the pattern,
    writes them to the output file, appends 1/number_of_lines to each line.

    Parameters:
    - prefix (str): The prefix for the default file names.
    - input_file (str, optional): The path to the input file. Defaults to None.
    - output_file (str, optional): The path to the output file. Defaults to None.
    - pattern (str, optional): The regex pattern to search for. Defaults to None.

    Returns:
    None
    """
    # Set default file paths if not provided
    if input_file is None:
        input_file = f"{prefix}/ph/{prefix}.freq"
    if output_file is None:
        output_file = f"{prefix}/ph/{prefix}_band.kpt"
        
    if pattern is None:
        pattern = r'\s{10}'  # The pattern to grep for (exactly 10 whitespace characters)
    
    # Step 1: Read lines from input_file that contain the pattern
    with open(input_file, 'r') as infile:
        lines = [line for line in infile if re.search(pattern, line)]
    
    # Step 2: Calculate 1/number_of_lines 
    number_of_lines = len(lines)
    if number_of_lines > 0:
        value_to_append = round(1 / number_of_lines, 8)
    else:
        value_to_append = 0  # To handle the case where no lines match the pattern

    # Step 3: Write the header line and the modified lines to the output file
    with open(output_file, 'w') as outfile:
        outfile.write(f"{number_of_lines} Cartesian\n")  # Write the header line
        for line in lines:
            outfile.write(f"{line.strip()} {value_to_append:.8f}\n")  # Write modified lines

    # Step 4: Check if the file was created and modified successfully
    if os.path.exists(output_file):
        print(f"File {output_file} has been created successfully.")
    else:
        print(f"Error: File {output_file} was not created.")

### extract the nesting function from std.out file
def extract_nesting(prefix, input_file=None, output_file=None, pattern=None):
    """
    Generates the prefix.nesting_fn file by extracting lines from epw4.out that
    match the pattern 'Nesting function (q)= ', extracting the 4th field,
    numbering the lines, and writing to pb.nesting_fn.
    """
    # Set default file paths if not provided
    if input_file is None:
        input_file = f"{prefix}/nesting/nesting.out"
    if output_file is None:
        output_file = f"{prefix}/nesting/{prefix}.nesting_fn"
    if pattern is None:
        pattern = re.compile(r'Nesting function \(q\)= ')  
        
    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Write the header
        outfile.write("#iq Nesting function (q)\n")
        
        # Open the input file and process lines
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
        
        # Filter and process matching lines
        filtered_lines = []
        for line in lines:
            if pattern.search(line):
                # Extract the 4th field
                fields = line.split()
                if len(fields) >= 4:
                    filtered_lines.append(fields[3])
        
        # Write the filtered lines with numbering
        for idx, value in enumerate(filtered_lines, start=1):
            outfile.write(f"{idx} {value}\n")
            
### plot nesting function ####
def nesting_plot(prefix, xticks, phononData=None, nestData=None):
    
    fig = plt.figure(figsize=(4.5, 3.0))
    ax1 = fig.add_subplot(111)
    # Load data from file
    ## get the x-coordinates from phonon freq data
    if phononData is None:
        phononData = np.loadtxt(f'./{prefix.lower()}/ph/{prefix.lower()}.freq.gp')
    
    qPoints = phononData[:, 0]
    if nestData is None:
        nestData = np.loadtxt(f'./{prefix.lower()}/nesting/{prefix.lower()}.nesting_fn', skiprows=1)
    nest = nestData[:, 1] * 0.01

    ax1.plot(qPoints, nest, linestyle='-', marker='o', markersize = 2, c='b') # 0.001 is abribtrary

    # Set the axis limits
    windowFactor = 1.05
    ax1.set_xlim(0, qPoints[-1])
    ax1.set_ylim(0, np.max(nest) * windowFactor)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_ylabel(r'$f_{nest} \,(\mathbf{q})$ (arb. units)')

    # Label high-symmetry points
    ax1.set_xticks(get_sym_points(prefix), xticks)
    ax1.grid(visible=True, axis='x')
    if ax1.get_ylim()[0] != 0 :
        ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
     
    # Save figure to PDF
    plt.savefig(f"./{prefix}_nesting.pdf")

    # Show figure
    plt.show()
    plt.close()
    
### plot lambda function ####
def lambdaq_plot(prefix, xticks, phononData=None, temps=None):
    
    ## get the x-coordinates from phonon freq data
    if phononData is None:
        phononData = np.loadtxt(f'./{prefix.lower()}/ph/{prefix.lower()}.freq.gp')
    
    qPoints = phononData[:, 0]
    if temps is None:
        temps = 1
    lamq = np.loadtxt(f'./{prefix.lower()}/phselfen/lambda.phself.{temps}.000K', skiprows=4)
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4.0), sharey=True)
    fig.subplots_adjust(wspace=0.08)
    # Set the axis limits
    windowFactor = 1.05

    ax1.plot(qPoints, lamq[:, 1], linestyle='-', c='b') 
    ax1.set_xlim(0, qPoints[-1])
    #ax1.set_ylim(0, np.max(lamq[:, 1]) * windowFactor)
    ax1.set_ylim(0, 1.5)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_ylabel(r'$\lambda_{\mathbf{q}\nu}$')
    ax1.set_title(r'$\nu = 1$')
    # Label high-symmetry points
    ax1.set_xticks(get_sym_points(prefix), xticks)
    ax1.grid(visible=True, axis='x')
    if ax1.get_ylim()[0] != 0 :
        ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
        
    ax2.plot(qPoints, lamq[:, 2], linestyle='-', c='b') 
    ax2.set_xlim(0, qPoints[-1])
    ax2.set_title(r'$\nu = 2$')
    # Label high-symmetry points
    ax2.set_xticks(get_sym_points(prefix), xticks)
    ax2.grid(visible=True, axis='x')
    if ax2.get_ylim()[0] != 0 :
        ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
        
    ax3.plot(qPoints, lamq[:, 3], linestyle='-', c='b') 
    ax3.set_xlim(0, qPoints[-1])
    ax3.set_title(r'$\nu = 3$')
    # Label high-symmetry points
    ax3.set_xticks(get_sym_points(prefix), xticks)
    ax3.grid(visible=True, axis='x')
    if ax3.get_ylim()[0] != 0 :
        ax3.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
     
    # Save figure to PDF
    plt.savefig(f"./{prefix}_lambdaq.pdf")

    # Show figure
    plt.show()
    plt.close()
    
 ##combined plot nesting and lamda_q

def combined_plot(prefix, xticks, phononData=None, nestData=None, temps=None):
    """
    Generates a combined plot with 2x2 subplots.
    First subplot: Nesting function
    Second, Third, and Fourth subplots: Lambda function for different modes
    """
    if phononData is None:
        phononData = np.loadtxt(f'./{prefix.lower()}/ph/{prefix.lower()}.freq.gp')
    
    qPoints = phononData[:, 0]
    
    if nestData is None:
        nestData = np.loadtxt(f'./{prefix.lower()}/nesting/{prefix.lower()}.nesting_fn', skiprows=1)
    nest = nestData[:, 1] * 0.01

    if temps is None:
        temps = 1
    lamq = np.loadtxt(f'./{prefix.lower()}/phselfen/lambda.phself.{temps}.000K', skiprows=4)
    
    # Create a 2x2 subplot layout
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # Plot the nesting function
    ax1.plot(qPoints, nest, linestyle='-', marker='o', markersize=2, c='b')
    ax1.set_xlim(0, qPoints[-1])
    ax1.set_ylim(0, np.max(nest) * 1.05)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_ylabel(r'$f_{nest} \,(\mathbf{q})$ (arb. units)')
    ax1.set_xticks(get_sym_points(prefix))
    ax1.set_xticklabels(xticks)
    ax1.grid(visible=True, axis='x')
    if ax1.get_ylim()[0] != 0:
        ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax1.set_title('Nesting Function')

    # Plot the lambda function for mode 1
    ax2.plot(qPoints, lamq[:, 1], linestyle='-', marker='o', markersize=2, c='b')
    ax2.set_xlim(0, qPoints[-1])
    ax2.set_ylim(0, 1.5)
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax2.set_ylabel(r'$\lambda_{\mathbf{q}\nu}$')
    ax2.set_xticks(get_sym_points(prefix))
    ax2.set_xticklabels(xticks)
    ax2.grid(visible=True, axis='x')
    if ax2.get_ylim()[0] != 0:
        ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.set_title(r'$\nu = 1$')

    # Plot the lambda function for mode 2
    ax3.plot(qPoints, lamq[:, 2], linestyle='-', marker='o', markersize=2, c='b')
    ax3.set_xlim(0, qPoints[-1])
    ax3.set_ylim(0, 1.5)
    ax3.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax3.set_ylabel(r'$\lambda_{\mathbf{q}\nu}$')
    ax3.set_xticks(get_sym_points(prefix))
    ax3.set_xticklabels(xticks)
    ax3.grid(visible=True, axis='x')
    if ax3.get_ylim()[0] != 0:
        ax3.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax3.set_title(r'$\nu = 2$')

    # Plot the lambda function for mode 3
    ax4.plot(qPoints, lamq[:, 3], linestyle='-', marker='o', markersize=2, c='b')
    ax4.set_xlim(0, qPoints[-1])
    ax4.set_ylim(0, 1.5)
    ax4.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax4.set_ylabel(r'$\lambda_{\mathbf{q}\nu}$')
    ax4.set_xticks(get_sym_points(prefix))
    ax4.set_xticklabels(xticks)
    ax4.grid(visible=True, axis='x')
    if ax4.get_ylim()[0] != 0:
        ax4.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax4.set_title(r'$\nu = 3$')

    # Set the title for the entire figure
    #fig.suptitle('Nesting Function and Lambda Function Subplots', fontsize=16)
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    
    # Save figure to PDF
    plt.savefig(f"./{prefix}_combined_plot.pdf")

    # Show figure
    plt.show()
    plt.close()
    
#### Isotropic gap (real and imaginary)
def gap_iso_real_imag(prefix, home, temp=0.3, font=12):
    os.chdir(home)
    os.chdir(f'./{prefix}/epw')
    ##load data
    imag_iso=np.loadtxt(f'{prefix}.imag_iso_00{temp}0', skiprows=1)*1000
    imag_pade=np.loadtxt(f'{prefix}.pade_iso_00{temp}0', skiprows=1)*1000
    #imag_acon=np.loadtxt(f'./{prefix}/epw/{prefix}.acon_iso_000.30', skiprows=1)*1000

    fig = plt.figure(figsize=(14.5, 5.0))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    #plot gap along imaginary axis
    #plt.plot(imag_iso[:,0],imag_iso[:,1])
    ax1.plot(imag_iso[:,0],imag_iso[:,2],color='k')
    ax1.set_title(f'Gap conv. along Im. axis at T = {temp} K',fontsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_ylabel('$\Delta$ [meV]',fontsize=font)
    ax1.set_xlabel('$\omega$ [meV]',fontsize=font)

    ax2.plot(imag_pade[:,0],imag_pade[:,3],color='k')
    ax2.plot(imag_pade[:,0],imag_pade[:,4],color='r')

    #ax2.plot(imag_acon[:,0],imag_acon[:,3],color='crimson',linestyle='--')
    #ax2.plot(imag_acon[:,0],imag_acon[:,4],color='royalblue',linestyle='--')

    ax2.legend(['Re($\Delta$): Pade approx.','Im($\Delta$): Pade approx.',
                'Re($\Delta$): Analytic cont.','Im($\Delta$): Analytic cont.'],fontsize=font-2.0)
    ax2.set_ylabel('$\Delta$ [meV]',fontsize=font)
    ax2.set_xlabel('$\omega$ [meV]',fontsize=font)
    ax2.tick_params(axis="y", labelsize=font)
    ax2.tick_params(axis="x", labelsize=font)
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax2.set_title(f'Gap conv. using Pade approx. at T = {temp} K',fontsize=font)
    
    ax2.set_xlabel('$\omega$ [meV]',fontsize=font)
    plt.tight_layout()
    plt.savefig(f"./{prefix}_iso_gap_real_imag.pdf")
    plt.show()
    
#### Isotropic gap (Imaginary)
def gap_iso_imag(prefix, home, temp=0.3, font=12):
    ##load data
    os.chdir(home)
    os.chdir(f'./{prefix}/epw')
    imag_iso=np.loadtxt(f'{prefix}.imag_iso_00{temp}0', skiprows=1)*1000
    
    fig = plt.figure(figsize=(5.5, 4.0))
    ax1 = fig.add_subplot(1,1,1)

    #plot gap along imaginary axis
    #plt.plot(imag_iso[:,0],imag_iso[:,1])
    ax1.plot(imag_iso[:,0],imag_iso[:,2])
    ax1.tick_params(axis="x", labelsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

    ax1.set_ylabel('$\Delta$ [meV]',fontsize=font)
    ax1.set_xlabel('$\omega$ [meV]',fontsize=font)
    plt.tight_layout()
    plt.savefig(f"./{prefix}_iso_gap_imag.pdf")
    plt.show()
    
#### Isotropic gap (Imaginary, real and ) vs. temeprature

def gap_iso_real_imag_temp(prefix, home, tempmax, font=12):
    #dirctory
    #dir_list = os.listdir(f'./{prefix}/epw/')
    os.chdir(home)
    os.chdir(f'./{prefix}/epw')
    dir_list = os.listdir(os.getcwd())
    #dir_list = os.listdir(filepath)
    #print(dir_list)
    gap0_imag = []
    gap0_pade = []
    #gap0_acon = []
    for i in range(len(dir_list)):
        if fnmatch.fnmatch(dir_list[i], "*.imag_iso*"):
            gap0_imag.append(dir_list[i])
            #print(gap0_imag)
            gap0_imag = sorted(gap0_imag)
        if fnmatch.fnmatch(dir_list[i], "*.pade_iso*"):
            gap0_pade.append(dir_list[i])
            gap0_pade = sorted(gap0_pade)

    imag_delta = np.zeros(len(gap0_imag))
    pade_delta = np.zeros(len(gap0_pade))
    #acon_delta = np.zeros(len(gap0_acon))
    
    for i in range(len(gap0_imag)):
        dummy, dummy, imag_delta[i] = np.loadtxt(gap0_imag[i],unpack=True, skiprows=1, max_rows=1)
        imag_delta[i] = imag_delta[i]*1000 #Convert to meV
        #
    for i in range(len(gap0_pade)):
        dummy, dummy, dummy, pade_delta[i], dummy = np.loadtxt(gap0_pade[i],unpack=True, skiprows=1, max_rows=1)
        pade_delta[i] = pade_delta[i]*1000 #Convert to meV
        #
    imag_temp = []
    pade_temp = []
    #acon_temp = []
    
    for fname in gap0_imag:
        res =  re.findall("imag_iso_(\S+)",fname)
        if not res: continue
        imag_temp.append(float(res[0]))

    for fname in gap0_pade:
        res =  re.findall("pade_iso_(\S+)",fname)
        if not res: continue
        pade_temp.append(float(res[0]))
 
    ##Plot    
    fig = plt.figure(figsize=(4.5, 3.5))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title('Superconducting Gap vs. Temperature', fontsize=font)
    ax1.set_xlabel('Temeperature (K)', fontsize=font)
    ax1.set_xlim(0,tempmax)
    ax1.set_ylabel(r'$\Delta_0$ (meV)', fontsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.plot(imag_temp, imag_delta, linestyle = '-', marker='o', c='k', label='Im. axis')
    ax1.plot(pade_temp, pade_delta, linestyle = '--', marker='o', c='r', label='Pade approx.')
    ax1.legend()
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_iso_gap_real_imag_vs_Temp.pdf")
    plt.show()
    
#### Isotropic gap (Imaginary, real and ) vs. temeprature

def gap_iso_imag_temp(prefix, home, tempmax, font=12):
    #dirctory
    os.chdir(home)
    os.chdir(f'./{prefix}/epw')
    dir_list = os.listdir(os.getcwd())
    #dir_list = os.listdir(f'./{prefix}/epw')
    gap0_imag = []
    
    for i in range(len(dir_list)):
        if fnmatch.fnmatch(dir_list[i], "*.imag_iso*"):
            gap0_imag.append(dir_list[i])
            gap0_imag = sorted(gap0_imag)
        
    #print(gap0_imag)
    
    imag_delta = np.zeros(len(gap0_imag))
    
    for i in range(len(gap0_imag)):
        dummy, dummy, imag_delta[i] = np.loadtxt(gap0_imag[i],unpack=True, skiprows=1, max_rows=1)
        imag_delta[i] = imag_delta[i]*1000 #Convert to meV
        #
    # print(imag_delta)
   
    imag_temp = []
        
    for fname in gap0_imag:
        res =  re.findall("imag_iso_(\S+)",fname)
        if not res: continue
        imag_temp.append(float(res[0]))
    #print(imag_temp)
    
    ##Plot
    fig = plt.figure(figsize=(4.5, 3.5))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title('Superconducting Gap vs. Temperature', fontsize=font)
    ax1.set_xlabel('Temeperature (K)', fontsize=font)
    ax1.set_xlim(0,tempmax)
    ax1.set_ylabel(r'$\Delta_0$ (meV)', fontsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.plot(imag_temp, imag_delta, linestyle = '-', marker='o', c='k', label='Im. axis')
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    plt.tight_layout()
    plt.savefig(f"./{prefix}_iso_gap_imag_vs_Temp.pdf")
    plt.show()
    
 ### FBW gap
def gap_iso_imag_fbw(prefix, home, tempmax, font=12):
    #dirctory
    os.chdir(home)
    os.chdir(f'./{prefix}/fbw')
    dir_list = os.listdir(os.getcwd())
    #dir_list = os.listdir(f'./{prefix}/epw')
    gap0_imag = []
    
    for i in range(len(dir_list)):
        if fnmatch.fnmatch(dir_list[i], "*.imag_iso*"):
            gap0_imag.append(dir_list[i])
            gap0_imag = sorted(gap0_imag)
        
    #print(gap0_imag)
    
    imag_delta = np.zeros(len(gap0_imag))
    
    for i in range(len(gap0_imag)):
        dummy, dummy, imag_delta[i], dummy = np.loadtxt(gap0_imag[i],unpack=True, skiprows=1, max_rows=1)
        imag_delta[i] = imag_delta[i]*1000 #Convert to meV
        #
    # print(imag_delta)
   
    imag_temp = []
        
    for fname in gap0_imag:
        res =  re.findall("imag_iso_(\S+)",fname)
        if not res: continue
        imag_temp.append(float(res[0]))
    #print(imag_temp)
    
    ##Plot
    fig = plt.figure(figsize=(4.5, 3.5))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title('Superconducting Gap vs. Temperature', fontsize=font)
    ax1.set_xlabel('Temeperature (K)', fontsize=font)
    ax1.set_xlim(0,tempmax)
    ax1.set_ylabel(r'$\Delta_0$ (meV)', fontsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.plot(imag_temp, imag_delta, linestyle = '-', marker='o', c='k', label='Im. axis')
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    plt.tight_layout()
    plt.savefig(f"./{prefix}_iso_FBW_gap_imag_vs_Temp.pdf")
    plt.show()
   
 ### FBW-FSR gap comparison

def gap_iso_fsr_and_fbw(prefix, home, tempmax, font=12):
    # Change directory to the specified 'home' directory
    # Change directory to the specified 'home' directory
    os.chdir(home)
    
    # Get list of files in the directories
    dir_fsr = os.listdir(f'./{prefix}/epw')
    dir_fbw = os.listdir(f'./{prefix}/fbw')
    
    # Filter out files with pattern "*.imag_iso*" from FSR and FBW directories
    gap_files_imag_fsr = sorted([file for file in dir_fsr if fnmatch.fnmatch(file, "*.imag_iso*")])
    gap_files_imag_fbw = sorted([file for file in dir_fbw if fnmatch.fnmatch(file, "*.imag_iso*")])
    
    # Initialize arrays to store gap values
    gap_values_fsr = np.zeros(len(gap_files_imag_fsr))
    gap_values_fbw = np.zeros(len(gap_files_imag_fbw))
    
    # Extract gap values from files
    for i, file in enumerate(gap_files_imag_fsr):
        full_path = os.path.join(home, prefix, "epw", file)  # Construct full path
        try:
            _, _, gap_values_fsr[i] = np.loadtxt(full_path, unpack=True, skiprows=1, max_rows=1)
            gap_values_fsr[i] *= 1000  # Convert to meV
        except Exception as e:
            print(f"Error loading file {full_path}: {e}")
        
    for i, file in enumerate(gap_files_imag_fbw):
        full_path = os.path.join(home, prefix, "fbw", file)  # Construct full path
        try:
            _, _, gap_values_fbw[i], _ = np.loadtxt(full_path, unpack=True, skiprows=1, max_rows=1)
            gap_values_fbw[i] *= 1000  # Convert to meV
        except Exception as e:
            print(f"Error loading file {full_path}: {e}")
    
    # Extract temperatures from file names
    imag_temp_fsr = [float(re.findall("imag_iso_(\S+)", fname)[0]) for fname in gap_files_imag_fsr]
    imag_temp_fbw = [float(re.findall("imag_iso_(\S+)", fname)[0]) for fname in gap_files_imag_fbw]
    
    ## Plot
    fig, ax1 = plt.subplots(figsize=(4.5, 3.5))
    ax1.set_title('Superconducting Gap vs. Temperature', fontsize=font)
    ax1.set_xlabel('Temperature (K)', fontsize=font)
    ax1.set_xlim(0, tempmax)   
    
    ax1.set_ylabel(r'$\Delta_0$ (meV)', fontsize=font)
    ax1.tick_params(axis="both", labelsize=font)
    ax1.plot(imag_temp_fsr, gap_values_fsr, linestyle='-', marker='o', c='k', label='FSR')
    ax1.plot(imag_temp_fbw, gap_values_fbw, linestyle='-', marker='*', c='r', label='FBW')
    ax1.legend()
    windowFactor = 1.05
    ax1.set_ylim(0, np.max(gap_values_fsr) * windowFactor)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_iso_FSR_FBW_gap_vs_Temp.pdf")
    plt.show()

    
def max_eig_temp(prefix, home, filename, nstemp = 21, font=12):
    os.chdir(home)
    #os.chdir(f'./{prefix}/epw')

    with open(f'./{prefix}/epw/{filename}','r') as f: 
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "eigenvalue  " in line:
                temp_vs_eig_lines=lines[index+2:index+2+nstemp]
    temp_vs_maxeigen = np.zeros((len(temp_vs_eig_lines),2))
    for i in range(len(temp_vs_eig_lines)):
        temp_vs_maxeigen[i][0] = float(temp_vs_eig_lines[i][9:17])
        temp_vs_maxeigen[i][1] = float(temp_vs_eig_lines[i][21:32])
    #print(temp_vs_maxeigen)
    fig = plt.figure(figsize=(5.5, 4.0))
    ax1 = fig.add_subplot(1,1,1)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.set_xlabel('Temeperature (K)', fontsize=font)
    ax1.set_ylabel('Max. Eigenvalue', fontsize=font)
    ax1.set_ylim(0,max(temp_vs_maxeigen[:,0])+0.5)
    ax1.set_ylim(0,max(temp_vs_maxeigen[:,1])+0.5)
    ax1.axhline(1, c='k', ls=':')   
    ax1.plot(temp_vs_maxeigen[:,0], temp_vs_maxeigen[:,1],marker='o')
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_max_eig_value_vs_Temp.pdf")
    plt.show()
    
    
##anisotropic plots #####

def plot_lambda(prefix, home, font=12):
    os.chdir(home)
    lam, rho, rho_not = np.loadtxt(f"./{prefix}/epw/{prefix}.lambda_pairs", unpack=True, skiprows=2)
    lam_pair = np.column_stack((lam,rho))

    lam, rho, rho_not = np.loadtxt(f"./{prefix}/epw/{prefix}.lambda_k_pairs", unpack=True, skiprows=2)
    lam_k_pair = np.column_stack((lam,rho))

    fig = plt.figure(figsize=(10.5, 3.5))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    ax1.plot(lam_pair[:,0], lam_pair[:,1], c='k', label=r'$\rho(\lambda_{nk, mk+q})$')
    ax1.fill_between(lam_pair[:,0], lam_pair[:,1], 'gray', alpha=0.5)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.set_xlim(0,6)
    ax1.set_ylim(0,max(lam_pair[:,1]))
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.set_yticks(())
    #ax1.set_ylabel('$\Delta$ [meV]',fontsize=font)
    ax1.set_xlabel(r'$\lambda_{nk, mk+q}$',fontsize=font)

    ax2.plot(lam_k_pair[:,0], lam_k_pair[:,1], c='k', label=r'$\rho(\lambda_{nk})$')
    ax2.fill_between(lam_k_pair[:,0], lam_k_pair[:,1], 'gray', alpha=0.5)
    ax2.set_xlim(0,max(lam_k_pair[:,0]))
    ax2.set_ylim(0,max(lam_k_pair[:,1]))
    ax2.tick_params(axis="y", labelsize=font)
    ax2.tick_params(axis="x", labelsize=font)
    ax2.set_xlabel(r'$\lambda_{nk}$', fontsize=font)
    ax2.set_yticks(())
    plt.tight_layout()
    plt.savefig(f"./{prefix}_lambda_pairs.pdf")
    plt.show()
    
### a2f plot ###
def plot_a2f(prefix, home, nqsmear = 10, font=12):
    os.chdir(home)
    #dataset
    a2f = np.loadtxt(f"./{prefix}/epw/{prefix}.a2f", skiprows=1, max_rows=500)

    fig = plt.figure(figsize=(4.5, 3.5))
    ax1 = fig.add_subplot(1,1,1)

    ax1.set_xlabel(r'$\omega$ (meV)')
    ax1.set_xlim(0,max(a2f[:,0]))
    ax1.set_ylim(0,max(a2f[:,nqsmear+1])+0.25)
    ax1.plot(a2f[:,0], a2f[:,1], color='k', label=r'$\alpha^2F(\omega)$')
    ax1.plot(a2f[:,0], a2f[:,nqsmear+1], color='r', label=r'$\lambda$')
    ax1.legend()
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_a2f_plot.pdf")
    plt.show()
    

## combined lambda aniso and isotropic plots

def plot_lamda_aniso_iso(prefix, home, nqsmear=10, font=12):
    os.chdir(home)
    
    # Load lambda pair data
    lam, rho, rho_not = np.loadtxt(f"./{prefix}/epw/{prefix}.lambda_pairs", unpack=True, skiprows=2)
    lam_pair = np.column_stack((lam, rho))

    lam, rho, rho_not = np.loadtxt(f"./{prefix}/epw/{prefix}.lambda_k_pairs", unpack=True, skiprows=2)
    lam_k_pair = np.column_stack((lam, rho))
    
    # Load a2F data
    a2f = np.loadtxt(f"./{prefix}/epw/{prefix}.a2f", skiprows=1, max_rows=500)
    
    # Create a 1x3 subplot layout
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.0))

    # Plot lambda pairs
    ax1.plot(lam_pair[:, 0], lam_pair[:, 1], c='k', label=r'$\rho(\lambda_{nk, mk+q})$')
    ax1.fill_between(lam_pair[:, 0], lam_pair[:, 1], 'gray', alpha=0.5)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, max(lam_pair[:, 1]))
    ax1.set_yticks(())
    ax1.set_xlabel(r'$\lambda_{nk, mk+q}$', fontsize=font)
    ax1.set_title(r'$\rho(\lambda_{nk, mk+q})$')
    
    # Plot lambda_k pairs
    ax2.plot(lam_k_pair[:, 0], lam_k_pair[:, 1], c='k', label=r'$\rho(\lambda_{nk})$')
    ax2.fill_between(lam_k_pair[:, 0], lam_k_pair[:, 1], 'gray', alpha=0.5)
    ax2.set_xlim(0, max(lam_k_pair[:, 0]))
    ax2.set_ylim(0, max(lam_k_pair[:, 1]))
    ax2.tick_params(axis="y", labelsize=font)
    ax2.tick_params(axis="x", labelsize=font)
    ax2.set_xlabel(r'$\lambda_{nk}$', fontsize=font)
    ax2.set_yticks(())
    ax2.set_title(r'$\rho(\lambda_{nk})$')
    
    # Plot alpha2F
    ax3.plot(a2f[:, 0], a2f[:, 1], color='k', label=r'$\alpha^2F(\omega)$')
    ax3.plot(a2f[:, 0], a2f[:, nqsmear + 1], color='r', label=r'$\lambda$')
    ax3.set_xlabel(r'$\omega$ (meV)')
    ax3.set_xlim(0, max(a2f[:, 0]))
    ax3.set_ylim(0, max(a2f[:, nqsmear + 1]) + 0.25)
    ax3.legend()
    ax3.tick_params(axis="y", labelsize=font)
    ax3.tick_params(axis="x", labelsize=font)
    ax3.set_title(r'isotropic $\alpha^2F(\omega)$ and $\lambda$')

    plt.tight_layout()
    plt.savefig(f"./{prefix}_aniso_iso_e-ph_coupling.pdf")
    plt.show()
    plt.close()

    
##anisotropic gap
def gap_conv_aniso_real_imag(prefix, home, temp=10, font=12, calc_type='fsr'):
    os.chdir(home)
    fig = plt.figure(figsize=(10.5, 4.0))
    
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    
    if calc_type == 'fbw':
        imag_gap_aniso = np.loadtxt(f"./{prefix}/fbw/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))
    elif calc_type == 'fbw_mu':
        imag_gap_aniso = np.loadtxt(f"./{prefix}/fbw_mu/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))
    else:
        imag_gap_aniso = np.loadtxt(f"./{prefix}/epw/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))

    #imag_gap_aniso = np.loadtxt(f"./{prefix}/epw/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))
    imag_gap_aniso = imag_gap_aniso*1000

    real_gap_pade_aniso = np.loadtxt(f"./{prefix}/epw/{prefix}.pade_aniso_0{temp}.00", skiprows=1, usecols=(0,4))
    real_gap_pade_aniso = real_gap_pade_aniso*1000

    ax1.set_ylabel(r'$\Delta_{nk}$ (meV)',fontsize=font)
    ax1.set_xlabel(r'i$\omega$ [meV]',fontsize=font)
    ax1.set_xlim(0,max(imag_gap_aniso[:,0]))
    ax1.set_ylim(-2,max(imag_gap_aniso[:,1])+3)
    ax1.plot(imag_gap_aniso[:,0], imag_gap_aniso[:,1],',')
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_title(f"Gap convergence at T = {temp} K")

    ax2.tick_params(axis="y", labelsize=font)
    ax2.tick_params(axis="x", labelsize=font)
    ax2.set_ylabel(r'$\Delta_{nk}$ (meV)',fontsize=font)
    ax2.set_xlabel(r'$\omega$ [meV]',fontsize=font)
    ax2.set_xlim(0,max(real_gap_pade_aniso[:,0]))
    ax2.set_ylim(-100,100)
    ax2.plot(real_gap_pade_aniso[:,0], real_gap_pade_aniso[:,1], ',')
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

    ax2.set_title(f"Gap convergence at T = {temp} K")
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_gap_conv_re_im.pdf")
    plt.show()

##anisotropic gap
def gap_conv_aniso_imag(prefix, home, calc_type='fsr', temp=10, font=12):
    os.chdir(home)
    fig = plt.figure(figsize=(4.5, 2.8))
    
    ax1 = fig.add_subplot(1,2,1)  
    
    if calc_type == 'fbw':
        imag_gap_aniso = np.loadtxt(f"./{prefix}/fbw/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))
    elif calc_type == 'fbw_mu':
        imag_gap_aniso = np.loadtxt(f"./{prefix}/fbw_mu/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))
    else:
        imag_gap_aniso = np.loadtxt(f"./{prefix}/epw/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))

    #imag_gap_aniso = np.loadtxt(f"./{prefix}/epw/{prefix}.imag_aniso_0{temp}.00", skiprows=1, usecols=(0,3))
    imag_gap_aniso = imag_gap_aniso*1000
    ax1.set_ylabel(r'$\Delta_{nk}$ (meV)',fontsize=font)
    ax1.set_xlabel(r'i$\omega$ [meV]',fontsize=font)
    ax1.set_xlim(0,max(imag_gap_aniso[:,0]))
    ax1.set_ylim(-2,max(imag_gap_aniso[:,1])+3)
    ax1.plot(imag_gap_aniso[:,0], imag_gap_aniso[:,1],',')
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_title(f"Gap convergence at T = {temp} K")

    plt.tight_layout()
    plt.savefig(f"./{prefix}_aniso_Im_gap_conv.pdf")
    plt.show()
    
#### Gap vs. Temperature #####
def gap_aniso_temp(prefix, home, calc_type='fsr', tempmax=30, font=12):
    #directory path
    os.chdir(home)
    
    fig = plt.figure(figsize=(4.5, 2.8))
    ax1 = fig.add_subplot(111)
    
    if calc_type == 'fbw':
        os.chdir(f'./{prefix}/fbw')
        #ax1.set_title('./{prefix}/fbw')
    elif calc_type == 'fbw_mu':
        os.chdir(f'./{prefix}/fbw_mu')
    else:
        os.chdir(f'./{prefix}/epw')

    #os.chdir(f'./{prefix}/epw')
    dir_list = os.listdir(os.getcwd())

    gap0_aniso_files = sorted([
            filename for filename in dir_list 
            if fnmatch.fnmatch(filename, "*.imag_aniso_gap0*") 
            and not filename.endswith('.frmsf') 
            and not filename.endswith('.cube')
        ])
        
    dict_files={}
    for i in range(len(gap0_aniso_files)):
        dict_files[gap0_aniso_files[i]] = np.loadtxt(gap0_aniso_files[i], skiprows=1)
        
    # Determine the maximum y-limit value from the first file's data
    max_y_value = max(dict_files[gap0_aniso_files[0]][:, 1]) if gap0_aniso_files else 1
    
    for i in range(len(gap0_aniso_files)):
        ax1.plot(dict_files[gap0_aniso_files[i]][:,0], dict_files[gap0_aniso_files[i]][:,1], color='blue')

    ax1.set_xlabel('Temeperature (K)', fontsize=font)
    ax1.set_xlim(0,tempmax)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.set_ylabel(r'$\Delta_{nk}$ (meV)', fontsize=font)
    ax1.set_ylim(0,max_y_value * 1.05)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax1.set_title(f'Supercond. Im. gap using {calc_type} approx.')
    #ax1.annotate(r'$\pi$', (7.5, 3), fontsize=font)
    #ax1.annotate(r'$\sigma$', (7.5, 10), fontsize=font)

    #plt.title('Superconducting Gap vs. Temperature', fontsize=font)
    plt.tight_layout()
    plt.savefig(f"./{prefix}_gap_aniso_vs_temp.pdf")
    plt.show()
    
def gap_aniso_fsr_fbw(prefix, home, tempmax=30, font=12):
    fig = plt.figure(figsize=(4.5, 2.8))
    ax1 = fig.add_subplot(111)

    types = ['fsr', 'fbw']
    colors = ['blue', 'green']
    
    for i, calc_type in enumerate(types):
        os.chdir(home)
        if calc_type == 'fbw':
            os.chdir(f'./{prefix}/fbw')
        else:
            os.chdir(f'./{prefix}/epw')
            
        dir_list = os.listdir(os.getcwd())
        
        gap0_aniso_files = [file for file in dir_list if fnmatch.fnmatch(file, "*.imag_aniso_gap0*") and len(file) == 27]
        gap0_aniso_files = sorted(gap0_aniso_files)
        
        dict_files = {}
        for file in gap0_aniso_files:
            dict_files[file] = np.loadtxt(file, skiprows=1)
        
        for file in gap0_aniso_files:
            ax1.plot(dict_files[file][:, 0], dict_files[file][:, 1], color=colors[i])

    ax1.set_xlabel('Temperature (K)', fontsize=font)
    ax1.set_xlim(0, tempmax)
    ax1.tick_params(axis="both", labelsize=font)
    ax1.set_ylabel(r'$\Delta_{nk}$ (meV)', fontsize=font)
    ax1.set_ylim(0, 15)
    ax1.legend(['FSR', 'FBW'])
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_gap_aniso_fsr_fbw_vs_temp.pdf")
    plt.show()
    
def gap_aniso_outerwin(prefix, home, ylim=(0, 5), tempmax=30, muc=0.25, mu=0.429, font=12):
    fig = plt.figure(figsize=(5.0, 4.0))
    ax1 = fig.add_subplot(111)

    types = ['muc', 'outer']
    colors = ['blue', 'green']
    
    for i, calc_type in enumerate(types):
        os.chdir(home)
        if calc_type == 'outer':
            os.chdir(f'./{prefix}/epw_outerbands')
        else:
            os.chdir(f'./{prefix}/fbw_mu')
            
        dir_list = os.listdir(os.getcwd())
        
        gap0_aniso_files = [file for file in dir_list if fnmatch.fnmatch(file, "*.imag_aniso_gap0*")]
        gap0_aniso_files = sorted(gap0_aniso_files)
        
        dict_files = {}
        for file in gap0_aniso_files:
            dict_files[file] = np.loadtxt(file, skiprows=1)
        
        for file in gap0_aniso_files:
            ax1.plot(dict_files[file][:, 0], dict_files[file][:, 1], color=colors[i])

    ax1.set_xlabel('Temperature (K)', fontsize=font)
    ax1.set_xlim(0, tempmax)
    ax1.tick_params(axis="both", labelsize=font)
    ax1.set_ylabel(r'$\Delta_{nk}$ (meV)', fontsize=font)
    ax1.set_ylim(ylim)
    ax1.legend([r'$\mu_c^*$ = 0.25', r'With outer bads ($\mu$ = 0.429)'])
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_gap_aniso_wo_vs_with_coul.pdf")
    plt.show()
    
def gap_aniso_fsr_fbw_mu_temp(prefix, home, tempmax=30, font=12):
    fig = plt.figure(figsize=(4.5, 3.0))
    ax1 = fig.add_subplot(111)

    types = ['fsr', 'fbw', 'fbw_mu']
    colors = ['blue', 'green', 'red']
    
    for i, calc_type in enumerate(types):
        os.chdir(home)
        if calc_type == 'fbw':
            os.chdir(f'./{prefix}/fbw')
        elif calc_type == 'fbw_mu':
            os.chdir(f'./{prefix}/fbw_mu')
        else:
            os.chdir(f'./{prefix}/epw')
            
        dir_list = os.listdir(os.getcwd())
        
        gap0_aniso_files = [file for file in dir_list if fnmatch.fnmatch(file, "*.imag_aniso_gap0*") and len(file) == 27]
        gap0_aniso_files = sorted(gap0_aniso_files)
        
        dict_files = {}
        for file in gap0_aniso_files:
            dict_files[file] = np.loadtxt(file, skiprows=1)
        
        for file in gap0_aniso_files:
            ax1.plot(dict_files[file][:, 0], dict_files[file][:, 1], color=colors[i])

    ax1.set_xlabel('Temperature (K)', fontsize=font)
    ax1.set_xlim(0, tempmax)
    ax1.tick_params(axis="both", labelsize=font)
    ax1.set_ylabel(r'$\Delta_{nk}$ (meV)', fontsize=font)
    ax1.set_ylim(0, 15)

    ax1.legend(['FSR', 'FBW', r'FBW+$\mu$'])
    
    plt.tight_layout()
    plt.savefig(f"./{prefix}_gap_aniso_fsr_fbw_mu_vs_temp.pdf")
    plt.show()
    
## Quasiparticle DOS
def plot_qpdos(prefix, home, filename ='epw1.out', temp=10, font=12):
    #directory path
    os.chdir(home)
    ## data file 
    qdos = np.loadtxt(f"./{prefix}/epw/{prefix}.qdos_010.00", skiprows=1)

    with open(f'./{prefix}/epw/{filename}','r') as f:
        lines = f.readlines()
        itera = 0
        for index, line in enumerate(lines):
            if "DOS" in line and itera == 0:
                DOS_value=lines[index]
                itera = itera + 1

    DOS_value = float(DOS_value[-22:-5])

    fig = plt.figure(figsize=(4.5, 4.0))
    ax1 = fig.add_subplot(111)

    ax1.set_xlabel(r'$\omega$ (meV)', fontsize=font)
    #ax1.set_xlim(0,max(qdos[:,0])*1000*0.2)
    #ax1.set_xticks(fontsize=font)
    ax1.set_xlim(0,15)
    ax1.tick_params(axis="y", labelsize=font)
    ax1.tick_params(axis="x", labelsize=font)
    ax1.set_ylabel(r'$N_s(\omega)/N_F$', fontsize=font)
    ax1.plot(qdos[:,0]*1000, qdos[:,1]/DOS_value, color='k')

    plt.tight_layout()
    plt.savefig(f"./{prefix}_Qpdos_{temp}.pdf")
    plt.show()
