import glob
import json
import os

manifest_dir ="data/pilots/tifantina/manifests"
manifest_dir ="data/pilots/norba/manifests"
manifests = glob.glob(manifest_dir+"/*.json")
for manifest in manifests:
    if manifest.endswith("temp.json"):
        continue
    print(manifest)
    fin = open(manifest, "r")
    fout = open(manifest_dir+"/temp.json", "w")
    filedata = fin.read()
    fin.close()
    new_data=filedata.replace("@none", "italian")
    fout.write(new_data)
    fout.close()
    fin = open(manifest_dir+"/temp.json", "r")
    jManifest = json.load(fin)
    fin.close()
    jManifest["annotations"] = []
    toberemoved = []
    for i in range(len(jManifest['items'])):
        if 'annotations' in jManifest['items'][i].keys():
            annotation = jManifest['items'][i]['annotations']
            jManifest["annotations"].append(annotation)
            jManifest['items'][i].pop('annotations', None)

    # correggere tutte le canvas senza immagine (Es. JPG invece che jpg)
        if 'width' not in  jManifest['items'][i].keys():
            if "duration" not in  jManifest['items'][i].keys():
                toberemoved.append(i)
    print(toberemoved)
    removed = 0
    for index in toberemoved:
        print(jManifest['items'][index-removed]['label']['italian'])
        jManifest['items'].pop(index-removed)
        removed +=1


    fout = open(manifest_dir+"/new/"+os.path.basename(manifest), "w")
    json.dump(jManifest,fout,indent=4)
    fout.close()
