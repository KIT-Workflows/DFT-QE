from ase.io import read, write

# Load the structure from the CIF file using ASE
initial_struct = read('initial_structure.cif')

# Convert atomic positions to fractional coordinates
cell = initial_struct.get_cell()
positions = initial_struct.get_scaled_positions()

# Write the structure in "ATOMIC_POSITIONS {crystal}" format
with open('input.pwi', 'w') as f:
    f.write('ATOMIC_POSITIONS {crystal}\n')
    for symbol, pos in zip(initial_struct.get_chemical_symbols(), positions):
        f.write(f'  {symbol} {pos[0]} {pos[1]} {pos[2]}\n')
