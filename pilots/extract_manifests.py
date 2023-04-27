import json
import shutil
pilot_dirs = ["/home/salvatore/public_html/norba"]

for pilot_dir in pilot_dirs:
    fp = open(pilot_dir+"/manifests.csv")
    lines = fp.readlines()
    for line in lines:
        if line.count("/") > 1:
            temp = line[2:-12]
            temp = temp.replace("/","_")
            print("data/pilots/norba/manifests/"+temp+".json")
            if line[-1]=='\n':
                line=line[:-1]
            shutil.copy(pilot_dir+line[1:], "data/pilots/norba/manifests/"+temp+".json")


