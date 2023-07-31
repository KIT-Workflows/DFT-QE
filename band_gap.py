import argparse
import re

def HELP():
    print("gappw.py [ -n -c -h ] FILENAME")
    print("Usage: Find band gap from PWscf output file\nFor semiconductor and insulator only\nrun as\n $./gappw.py pw.out")
    print("-n : noncollinear format")
    print("-c : collinear format")
    print("-h : show this message")
    print("N.B. spin-polarized not implement")
    exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("-n", action="store_true", help="noncollinear format")
parser.add_argument("-c", action="store_true", help="collinear format")
parser.add_argument("-h", action="store_true", help="show this message")
parser.add_argument("file_in", help="PWscf output file")
args = parser.parse_args()

if args.h:
    HELP()

if not args.n and not args.c:
    print("ERROR: Must specify either -n or -c")
    HELP()

if args.n:
    print("noncollinear")
    flag_noncol = 1
else:
    print("collinear")
    flag_noncol = 0

file_in = args.file_in

with open(file_in) as f:
    file_text = f.read()

NKPT = re.search("number of k points=(\d+)", file_text).group(1)
if not NKPT:
    print("No k-point found")
    exit(1)

NBD = re.search("number of Kohn-Sham states=(\d+)", file_text).group(1)
NTYP = re.search("number of atomic types    =(\d+)", file_text).group(1)

IZVAL = re.findall("atomic species   valence.*\n(\w+)\s+(\d+)", file_text)
ELEM = [x[0] for x in IZVAL]
IZVAL = [x[1] for x in IZVAL]

NAT = re.search("number of atoms/cell      =(\d+)", file_text).group(1)

print("number of k-piont  = ", NKPT)
print("number of band = ", NBD)
print("number of atomic type = ", NTYP)
print("number of valence electron = ", IZVAL)
print("number of atoms = ", NAT)
print("atomic species = ", ELEM)

flag_SOC_non_mag = "Non magnetic calculation with spin-orbit" in file_text
flag_SOC_mag = "Noncollinear calculation with spin-orbit" in file_text
flag_noncol_non_SOC = "Noncollinear calculation without spin-orbit" in file_text

if flag_SOC_non_mag:
    flag_noncol = 1
    print("calculation with spin-orbit, non-magnetic")

if flag_SOC_mag:
    flag_noncol = 1
    print("calculation with spin-orbit, magnetic")

if flag_noncol_non_SOC:
    flag_noncol = 0
    print("calculation without spin-orbit, non-magnetic")

if flag_noncol:
    print("noncollinear calculation")
else:
    print("collinear calculation")
