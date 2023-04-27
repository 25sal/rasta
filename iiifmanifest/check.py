import json
import glob
import os

host_name = "https://cosme.unicampania.it"
home_path = host_name+"/rasta/tifantina"
m_dirs = glob.glob("/home/salvatore/Downloads/dianatifatina/test/*")
for m_dir in m_dirs:
    if os.path.isdir(m_dir):
        manifests = glob.glob(m_dir+"/*.json")
        for manifest_file in manifests:
            filein = open(manifest_file, "r")
            manifest = json.load(filein)
            items_l1 = manifest['items']
            for item_l1  in items_l1:
                if item_l1['type'] =='Canvas':
                    items_l2 = item_l1['items'][0]['items']
                    for item_l2 in items_l2:
                        if item_l2['body']['type']== 'Image':

                            image_uri = item_l2['body']['service'][0]['@id']
                            print(image_uri)
                            id = item_l2['body']['id'][:-4]+".tif"

                            id = host_name + "/iiif"+id[len(host_name):]
                            print(id)
                            item_l2['body']['service'][0]['@id'] =  id
                            item_l2['body']['id'] = id
                    if 'thumbnail' in item_l1.keys():
                        thumb = item_l1['thumbnail'][0]['id']
                        print(thumb)
                        parts = thumb.split("/")
                        print(home_path + "/" +parts[-2] +"/" +parts[-3]+"/"+parts[-1])
                        item_l1['thumbnail'][0]['id'] = home_path + "/" +parts[-2] +"/" +parts[-3]+"/"+parts[-1]

            filein.close()
            file_out = open(manifest_file,"w")
            json.dump(manifest, file_out, indent=4)

