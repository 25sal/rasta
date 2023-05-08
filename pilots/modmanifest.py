import glob
import json
import os
import logging


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)

pilot = "tifantina"
manifest_dir ="data/pilots/"+pilot+"/manifests"
manifests = glob.glob(manifest_dir+"/*.json")


def replace_items(manifest, jManifest, item_indexes):
    print(manifest)

    fid = open("data/pilots2/"+pilot+"/manifests/"+os.path.basename(manifest), "r")
    filedata = fid.read()
    new_data = filedata.replace("@none", "italian")
    fid.close()
    jbiif = json.loads(new_data)
    for i in item_indexes:

        print("------------------------------------------------------------")
        print(jManifest['items'][i]['items'][0]['items'])
        print("------------------------------------------------------------")
        print(jbiif['items'][i]['items'][0]['items'])
        print("------------------------------------------------------------")
        if len(jbiif['items'][i]['items'][0]['items']) > 0:
            jManifest['items'][i]['items'][0]['items'].append(jbiif['items'][i]['items'][0]['items'][0])
            jManifest['items'][i]['width'] = jbiif['items'][i]['items'][0]['items'][0]['body']['width']
            jManifest['items'][i]['height'] = jbiif['items'][i]['items'][0]['items'][0]['body']['height']
        else:
            logger.debug(manifest + " " + str(i))



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
    replace_items(manifest, jManifest, toberemoved)

    '''
    for index in toberemoved:
        # print(jManifest['items'][index-removed]['label']['italian'])
        # jManifest['items'].pop(index-removed)
        print("replaced_items:")
        print(jManifest['items'][index]['items'][0]['items'])
        removed +=1
    '''



    fout = open(manifest_dir+"/new/"+os.path.basename(manifest), "w")
    json.dump(jManifest,fout,indent=4)
    fout.close()

