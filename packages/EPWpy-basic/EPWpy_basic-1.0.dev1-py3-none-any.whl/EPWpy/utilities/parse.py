import numpy as np

def parse_data(filename):
    atomic_labels = []
    atomic_positions = []
    cell_param = []
    add_param = {}
    reading_positions = False
    reading_cell_parameters = False

    with open(filename, "r") as file:
        for line in file:
            if "ATOMIC_POSITIONS " in line:
                reading_positions = True
            elif "CELL_PARAMETERS " in line:
                reading_cell_parameters = True
            elif reading_positions:
                line = line.strip()
                if line:
                    words = line.split()
                    atomic_label = words[0]
                    positions = np.array([float(w) for w in words[1:]])
                    atomic_labels.append(atomic_label)
                    atomic_positions.append(positions)
            elif reading_cell_parameters:
                line = line.strip()
                if line:
                    words = line.split()
                    cell_param.append([float(w) for w in words])
            else:
                if "nat" in line:
                    nat_value = line.split("=")[1].strip()
                    nat = int(nat_value)
                elif "ntyp" in line:
                    ntyp_value = line.split("=")[1].strip()
                    ntyp = int(ntyp_value)
                elif "ecutwfc" in line:
                    ecutwfc_value = line.split("=")[1].strip()
                    ecutwfc = float(ecutwfc_value)

    add_param["nat"] = nat
    add_param["ntyp"] = ntyp
    add_param["ecutwfc"] = ecutwfc

    return(atomic_labels, np.array(atomic_positions), np.array(cell_param), add_param)
if __name__=='__main__':

    atomic_labels,atomic_positions,cell_param, add_param = parse_data('data.txt')
    print(atomic_positions)
