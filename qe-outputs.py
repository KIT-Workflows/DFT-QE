import sys, yaml, os

# os.system("awk '/^!.*total/{print vol, $5}' QEIN.out > temp_file")

# with open('temp_file') as f:
#     xml = f.read()

# decimal_points = 6
# xml = round(float(xml),decimal_points)

with open('rendered_wano.yml') as file:
    wano_file = yaml.full_load(file)

wano_file["energy"] = 0.004#xml

with open("QEOUT.yml",'w') as out:
            yaml.dump(wano_file, out,default_flow_style=False)

if os.path.exists("temp_file"):
    os.remove("temp_file")
