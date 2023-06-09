import json
import shutil
import glob
import os
import subprocess
pilot_dirs = {"norba": "data/pilots2/norba", "tifantina":"data/pilots2/tifantina"}
base_dir="/home/salvatore/development/PycharmProjects/rasta/"
for key in pilot_dirs.keys():
    m_dirs = glob.glob(pilot_dirs[key]+"/*")
    for m_dir in m_dirs:
        if os.path.isdir(m_dir):
            print("node scripts/prova.js "+base_dir+m_dir)

            subprocess.run(["node", "scripts/prova.js", base_dir+m_dir], cwd="/data/persone/alba/biiif")
            # exit(0)
            manifest_file = m_dir+"/index.json"
            path_ele = manifest_file.split("/")
            new_file = path_ele[-2].replace("-","_")
            new_file = new_file.replace(" ","_")
            new_file = new_file.lower()
            print(manifest_file, new_file)
            if not os.path.isdir("data/pilots2/"+key+"/manifests/"):
                os.makedirs("data/pilots2/"+key+"/manifests")
            shutil.copy(manifest_file, "data/pilots2/"+key+"/manifests/"+new_file+".json")


