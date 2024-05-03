import shutil

fin = open("../data/pilots/tifantina/public_html/tifantina/manifests.csv", "r")
lines = fin.readlines()
for line in lines:
    if line[:-1].endswith(".json"):
        new_name = line.split("/")
        new_name = new_name[1]
        new_name = new_name.replace(" ", "_")
        new_name = new_name.lower()
        shutil.copy("../data/pilots/tifantina/public_html/tifantina"+line[1:-1],new_name+".json")
        print("../data/pilots/tifantina/public_html/tifantina"+line[1:-1], new_name+".json" )
