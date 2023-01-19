#from ase.build import bulk
#from ase import Atoms
from ase.io import write, read
import yaml
from ast import literal_eval

def pseud_pot(elements):

    pseudopot={}

    SSSP = {"Ag":'Ag_ONCV_PBE-1.0.oncvpsp.upf', "C": 'C.pbe-n-kjpaw_psl.1.0.0.UPF', 
    "Ho":'Ho.GGA-PBE-paw-v1.0.UPF', "Nd":'Nd.GGA-PBE-paw-v1.0.UPF', "Rh":'Rh_ONCV_PBE-1.0.oncvpsp.upf',
    "Te":'Te_pbe_v1.uspp.F.UPF', "Al":'Al.pbe-n-kjpaw_psl.1.0.0.UPF', "Cr":'cr_pbe_v1.5.uspp.F.UPF',
    "H":'H_ONCV_PBE-1.0.oncvpsp.upf', "Ne":'Ne_ONCV_PBE-1.0.oncvpsp.upf', "Rn":'Rn.pbe-dn-kjpaw_psl.1.0.0.UPF',
    "Ti":'ti_pbe_v1.4.uspp.F.UPF',"Ar":'Ar_ONCV_PBE-1.1.oncvpsp.upf', "Cs":'Cs_pbe_v1.uspp.F.UPF',
    "In":'In.pbe-dn-rrkjus_psl.0.2.2.UPF', "Ni":'ni_pbe_v1.4.uspp.F.UPF', "Ru":'Ru_ONCV_PBE-1.0.oncvpsp.upf',
    "Tl":'Tl_pbe_v1.2.uspp.F.UPF', "As":'As.pbe-n-rrkjus_psl.0.2.UPF',"Cu":'Cu_ONCV_PBE-1.0.oncvpsp.upf', 
    "I":'I.pbe-n-kjpaw_psl.0.2.UPF',"N":'N.oncvpsp.upf', "Sb":'sb_pbe_v1.4.uspp.F.UPF', 
    "Tm":'Tm.GGA-PBE-paw-v1.0.UPF',"Au":'Au_ONCV_PBE-1.0.oncvpsp.upf',"Dy":'Dy.GGA-PBE-paw-v1.0.UPF',
    "Ir":'Ir_pbe_v1.2.uspp.F.UPF',"O":'O.pbe-n-kjpaw_psl.0.1.UPF', "Sc":'Sc.pbe-spn-kjpaw_psl.0.2.3.UPF', 
    "V":'v_pbe_v1.4.uspp.F.UPF',"Ba":'Ba.pbe-spn-kjpaw_psl.1.0.0.UPF',"Er":'Er.GGA-PBE-paw-v1.0.UPF',
    "K":'K.pbe-spn-kjpaw_psl.1.0.0.UPF',"Os":'Os_pbe_v1.2.uspp.F.UPF', "Se":'Se_pbe_v1.uspp.F.UPF', 
    "W":'W_pbe_v1.2.uspp.F.UPF', "Be":'Be_ONCV_PBE-1.0.oncvpsp.upf', "Eu":'Eu.GGA-PBE-paw-v1.0.UPF', 
    "Kr":'Kr_ONCV_PBE-1.0.oncvpsp.upf',"Pb":'Pb.pbe-dn-kjpaw_psl.0.2.2.UPF',
    "Si":'Si.pbe-n-rrkjus_psl.1.0.0.UPF', "Xe":'Xe_ONCV_PBE-1.1.oncvpsp.upf', "Bi":'Bi_pbe_v1.uspp.F.UPF',
    "Fe":'Fe.pbe-spn-kjpaw_psl.0.2.1.UPF', "La":'La.GGA-PBE-paw-v1.0.UPF', "Pd":'Pd_ONCV_PBE-1.0.oncvpsp.upf',
    "Sm":'Sm.GGA-PBE-paw-v1.0.UPF',"Yb":'Yb.GGA-PBE-paw-v1.0.UPF',"B":'B_pbe_v1.01.uspp.F.UPF', 
    "F":'F.oncvpsp.upf', "Li":'li_pbe_v1.4.uspp.F.UPF', "Pm":'Pm.GGA-PBE-paw-v1.0.UPF',
    "Sn":'Sn_pbe_v1.uspp.F.UPF', "Y":'Y_pbe_v1.uspp.F.UPF',"Br":'br_pbe_v1.4.uspp.F.UPF', 
    "Ga":'Ga.pbe-dn-kjpaw_psl.1.0.0.UPF',"Lu":'Lu.GGA-PBE-paw-v1.0.UPF', "Po":'Po.pbe-dn-rrkjus_psl.1.0.0.UPF',
    "S":'s_pbe_v1.4.uspp.F.UPF',"Zn":'Zn_pbe_v1.uspp.F.UPF', "Ca":'Ca_pbe_v1.uspp.F.UPF', 
    "Gd":'Gd.GGA-PBE-paw-v1.0.UPF', "Mg":'mg_pbe_v1.4.uspp.F.UPF', "P":'P.pbe-n-rrkjus_psl.1.0.0.UPF',
    "Sr":'Sr_pbe_v1.uspp.F.UPF', "Zr":'Zr_pbe_v1.uspp.F.UPF', "Cd":'Cd.pbe-dn-rrkjus_psl.0.3.1.UPF',
    "Ge":'ge_pbe_v1.4.uspp.F.UPF',"Mn":'mn_pbe_v1.5.uspp.F.UPF', "Pr":'Pr.GGA-PBE-paw-v1.0.UPF',
    "Ce":'Ce.GGA-PBE-paw-v1.0.UPF',"He":'He_ONCV_PBE-1.0.oncvpsp.upf', "Mo":'Mo_ONCV_PBE-1.0.oncvpsp.upf',
    "Pt":'Pt.pbe-spfn-rrkjus_psl.1.0.0.UPF',"Ta":'Ta_pbe_v1.uspp.F.UPF',"Cl":'Cl.pbe-n-rrkjus_psl.1.0.0.UPF',
    "Hf":'Hf-sp.oncvpsp.upf', "Na":'Na_ONCV_PBE-1.0.oncvpsp.upf', "Rb":'Rb_ONCV_PBE-1.0.oncvpsp.upf',
    "Tb":'Tb.GGA-PBE-paw-v1.0.UPF', "Co":'Co_pbe_v1.2.uspp.F.UPF', "Hg":'Hg_ONCV_PBE-1.0.oncvpsp.upf',
    "Nb":'Nb.pbe-spn-kjpaw_psl.0.3.0.UPF', "Re":'Re_pbe_v1.2.uspp.F.UPF',"Tc":'Tc_ONCV_PBE-1.0.oncvpsp.upf'}

    for element in elements:
        if element in SSSP:
            pseudopot[element] = SSSP[element]
        else:
            print('There is no pseudopotential for this element:' + element)
            print('Check your pseudopotential folder!!!')
            exit

    return pseudopot



def check_vdW(dict_input):
    dict_vdw = {"D2":'DFT-D',"D3":'DFT-D3',"MBD":'MBD', "TS":'TS', "XDM":'XDM'}
    var_value = dict_input.get('vdw_corr')
    
    if var_value in dict_vdw:
        dict_input['vdw_corr'] = dict_vdw[var_value]
    else:
        del dict_input['vdw_corr']
    
    return dict_input

def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)

if __name__ == '__main__':

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    # Define the ase-espresso keys we will use.
    keys = {
        'pseudo_dir' : '/home/ws/gt5111/Celso_QE/SSSP_precision/',
        'pseudopotentials':'H_ONCV_PBE-1.0.oncvpsp.upf',
        'ibrav' : 0,
        'nspin': 1,
        'prefix': 'h2',
        'calculation': 'relax',
        'ion_dynamics': 'bfgs',
        'ecutwfc': 30.0,
        'input_dft': 'RPBE',
        'vdw_corr': 'none',
        'conv_thr': 1e-6,
        'diagonalization': 'cg',
        'outdir': '.',
        'output': {'removesave': True},
        'pw': 200,
        'dw': 2000,
        'electron_maxstep': 400,
        'nstep': 200,
        'convergence': {'energy': 1e-5, 'mixing': 0.35}
        }

    keys["title"] = wano_file["TABS"]["SETUP"]["Initial structure"]["Title"]
    keys["prefix"] = wano_file["TABS"]["SETUP"]["Initial structure"]["Title"]

    # Read the initial geometry
    geometry_name = wano_file["TABS"]["SETUP"]["Initial structure"]["Structure file"]
    initial_struct = read(geometry_name)

    # Defining the pseudopotentials
    elements = initial_struct.get_chemical_symbols()
    elements = list(set(elements))
    pseudopot = pseud_pot(elements)

    # Adding vdw-correctios
    keys["vdw_corr"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["vdw-corr"]
    keys = check_vdW(keys)

    keys["calculation"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["calculation"]
    keys["nspin"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["Spin"]
    
    keys["ecutwfc"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["ecutwfc"]
    keys["input_dft"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["Functional"]
    keys["diagonalization"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["diagonalization"]
    keys["ion_dynamics"] = wano_file["TABS"]["SETUP"]["CONTROL SYSTEM ELECTRONS IONS"]["ion dynamics"] 
    
    
    mat_n = literal_eval(wano_file["TABS"]["SETUP"]["KPOINTS"]["Monkhorst"])
    n_mesh = [mat_n[0][0], mat_n[0][1], mat_n[0][2]]
    n_shift = [mat_n[1][0], mat_n[1][1], mat_n[1][2]]
    
    gamma_point = [1, 1, 1]
    n_mesh.sort()
    gamma_point.sort()

    if n_mesh == gamma_point:
        keys["kpts"] = None
        keys["koffset"] = None
    else:    
        keys["kpts"] = n_mesh
        keys["koffset"] = [int(item) for item in n_shift]
    
    if keys["nspin"] > 1:
#        keys["tot_magnetization"] = 1
        keys["occupations"] = 'smearing'
        keys["smearing"] = 'marzari-vanderbilt'
        keys["degauss"] = 0.01 


    write('input.pwi', initial_struct, kpts = keys["kpts"], koffset = keys["koffset"], input_data = keys, pseudopotentials = pseudopot)

    if keys["nspin"] > 1:
        for ii in range(len(elements)):
            temp_str = str(ii + 1)
            inplace_change('input.pwi', 'starting_magnetization('+ temp_str +') = 0.0', 'starting_magnetization('+ temp_str +') = 0.5')

    # a3 = bulk('Cu', 'fcc', a=3.6, cubic=True)
    # a3 = bulk('NaCl', crystalstructure='rocksalt', a=6.0)
    # a3.write('NaCl.cif',format='cif')
    # initial_struct = read('NaCl.cif')
    
    
    #atoms.info = keys
    #write_espresso_in('input.in',atoms, kpts=keys["kpts"])
    #write_espresso_in('name.in',atoms,input(keys))