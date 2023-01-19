from ase.io import read
import yaml, re, datetime
from ase.cell import Cell
import numpy as np

class Util_tricks:

    def find_last_line(self, filename, string):

        with open(filename, 'r') as file:
            lines = file.readlines()
            last_line = None
            for line in lines:
                if string in line:
                    last_line = line
            return last_line
    
    def metadata(self, dict_properties):

        self.dict_properties = dict_properties

        results_dict['user'] = 'Your user name'

        current_datetime = datetime.datetime.now()
        self.dict_properties['datetime'] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        return dict_properties
    
    def find_line_number(self, file_name, string_to_search):
        with open(file_name, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if string_to_search in line:
                return i + 1
        return -1

    def remove_substrings(self, file_name, name, start_line):
        with open(file_name, 'r') as file:
            lines = file.readlines()

        with open(file_name, 'w') as file:
            for i, line in enumerate(lines):
                if i < start_line-1 or name not in line:
                    file.write(line)
                else:
                    if line.strip() != '':  # check if current line is not blank
                        line = line.replace(name, '')
                        file.write(line)
                    else:
                        break

class QE_properties:
    
    def __init__(self, properties_bool, dict_properties):
        self.properties_bool = properties_bool
        self.dict_properties = dict_properties 

    def check_conv_qe(self):
        
        '''
        Check if the convergency criteria was reached in the last iteration        
        '''

        with open('QEIN.out', 'r') as f:
            qe_lines = f.readlines()

        # Find the last iteration of the electronic minimization loop
        for i, line in enumerate(reversed(qe_lines)):
            if "convergence has been achieved" in line:
                break

        # Check if the convergency criteria was reached in the last iteration

        if "convergence has been achieved" in qe_lines[-i-1]:
            
            print("QE calculations successfully finished")
            
            self.dict_properties["convergence"] = "Yes"
            return self.dict_properties
        
        else:
            
            print("QE calculations not successfully finished")
            self.dict_properties["convergence"] = "No"
            return self.dict_properties

    def get_bandgap(self, location = "DOSCAR",tol = 1e-3):
        doscar = open(location)
        for i in range(6):
            l=doscar.readline()
        efermi = float(l.split()[3])
        step1 = doscar.readline().split()[0]
        step2 = doscar.readline().split()[0]
        step_size = float(step2)-float(step1)
        not_found = True
        while not_found:
            l = doscar.readline().split()
            e = float(l.pop(0))
            dens = 0
            for i in range(int(len(l)/2)):
                dens += float(l[i])
            if e < efermi and dens > tol:
                bot = e
            elif e > efermi and dens > tol:
                top = e
                not_found = False
        if top - bot < step_size*2:

            self.dict_properties["band_gap"] = 0.0
            self.dict_properties["vbm"] = 0.0
            self.dict_properties["cbm"] = 0.0

            return self.dict_properties
        else:
            self.dict_properties["band_gap"] = top - bot
            self.dict_properties["vbm"] = bot-efermi
            self.dict_properties["cbm"] = top-efermi
            
            return self.dict_properties

    def get_pressures(self):

        ''' This function will return the external pressure and Pullay stress in kB '''

        ut = Util_tricks() 
        press = ut.find_last_line('QEIN.out', 'pressure')
        press =press.split("kB")
        self.dict_properties["external_pressure"] = float(re.findall(r'[+-]?\d+.\d+', press[0])[0])
        self.dict_properties["pullay_stress"] = float(re.findall(r'[+-]?\d+.\d+', press[1])[0])

        return self.dict_properties

    def get_qe_properties(self):

        ''' Pressure and band gap aren't supported in ASE '''

        ut = Util_tricks()
        self.check_conv_qe()

        try:

            atoms = read('QEIN.out', format = "espresso-out")                        

        except ValueError:

            file_name = "QEIN.out"
            string_to_search = "Magnetic moment per site"
            strings_to_remove = "atom   "

            start_line = ut.find_line_number(file_name, string_to_search)
            ut.remove_substrings(file_name, strings_to_remove, start_line)
            atoms = read('QEIN.out', format = "espresso-out")

        a = "atoms.get_"
        c = "()"

        for var_prop in self.properties_bool:

            if isinstance(eval("".join( [a, var_prop, c] )), np.ndarray) or isinstance(eval("".join( [a, var_prop, c] )), Cell):
                self.dict_properties[var_prop] = eval("".join( [a, var_prop, c] )).tolist()
            elif isinstance(eval("".join( [a, var_prop, c] )), np.float64):
                self.dict_properties[var_prop] = eval("".join( [a, var_prop, c] ))
                self.dict_properties[var_prop] = float(self.dict_properties[var_prop])
            else:
                self.dict_properties[var_prop] = eval("".join( [a, var_prop, c] ))
                    
        return self.dict_properties


if __name__ == '__main__':

    ''' Supported properties in ASE '''

    properties_bool = ['total_energy', 'potential_energy', 'initial_magnetic_moments', 
            'magnetic_moments' ,'kinetic_energy','cell', 'cell_lengths_and_angles', 'positions', 'forces', 
            'chemical_formula', 'chemical_symbols', 'center_of_mass', 'volume', 'temperature', 'all_distances', 
            'masses', 'atomic_numbers', 'global_number_of_atoms', 'initial_charges']

    # sanitize properties

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    nspin = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["Spin"]
    calculation = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["calculation"]
    
    if nspin == 1:
        properties_bool.remove('magnetic_moments')
    
    if calculation == 'scf':
        properties_bool.remove('forces')


    
    results_dict = {}

    ''' current_datetime '''

    ut = Util_tricks()
    ut.metadata(results_dict)
    

    properties_qe = QE_properties(properties_bool, results_dict)
    
    results_dict = properties_qe.get_qe_properties()

    # with open("qe_results.yml","w") as out:
    #     yaml.dump(results_dict, out, default_flow_style=False)

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    # with open('qe_results.yml') as file:
    #     vasp_file = yaml.full_load(file)

    wano_file = {**wano_file, **results_dict}

    with open("qe_results.yml", "w") as out:
        yaml.dump(wano_file, out, default_flow_style=False)
    
    # with open("db_vasp_results.yml", "w") as out:
    #     yaml.dump(wano_file, out, default_flow_style=False)
    
