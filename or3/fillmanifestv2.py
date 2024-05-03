import json
import copy

max_canvas = 55

infile = open("data/or3/manifests/platee/carditello_calvi_v2.json", "r")
jsonObj = json.load(infile)
infile.close()
canvas = jsonObj["sequences"][0]["canvases"][0]

for i in range(1, max_canvas):
    temp =  copy.deepcopy(jsonObj["sequences"][0]["canvases"][0])
    jsonObj["sequences"][0]["canvases"].append(temp)
    temp_id = jsonObj["sequences"][0]["canvases"][i]["images"][0]['resource']['@id']
    jsonObj["sequences"][0]["canvases"][i]["images"][0]['resource']['@id'] = temp_id.replace("1.tif", str(i+1)+".tif")
    temp_id = jsonObj["sequences"][0]["canvases"][i]["images"][0]['resource']['service']['@id']
    jsonObj["sequences"][0]["canvases"][i]["images"][0]['resource']['service']['@id'] = temp_id.replace("1.tif", str(i+1)+".tif")
    jsonObj["sequences"][0]["canvases"][i]['@id']= \
        jsonObj["sequences"][0]["canvases"][i]['@id'].replace("efe07759-6070-45c0-ba41-5447e0ebbb32", str(i+1))
    jsonObj["sequences"][0]["canvases"][i]["images"][0]['@id'] = \
        jsonObj["sequences"][0]["canvases"][i]["images"][0]['@id'].replace("efe07759-6070-45c0-ba41-5447e0ebbb32",
                                                                                str(i + 1))

    jsonObj["sequences"][0]["canvases"][i]["images"][0]['on'] = \
        jsonObj["sequences"][0]["canvases"][i]["images"][0]['on'].replace("efe07759-6070-45c0-ba41-5447e0ebbb32",
                                                                                str(i + 1))

i = 0
jsonObj["sequences"][0]["canvases"][i]['@id']= \
        jsonObj["sequences"][0]["canvases"][i]['@id'].replace("efe07759-6070-45c0-ba41-5447e0ebbb32", str(i+1))
jsonObj["sequences"][0]["canvases"][i]["images"][0]['@id'] = \
        jsonObj["sequences"][0]["canvases"][i]["images"][0]['@id'].replace("efe07759-6070-45c0-ba41-5447e0ebbb32", str(i+1))


outf = open("data/or3/manifests/platee/carditello_calvi_f_v2.json", "w")
json.dump(jsonObj, outf, indent=3)
outf.close()
infile = open("data/or3/manifests/platee/carditello_calvi_f_v2.json", "r")
text_file = infile.read()
text_file = text_file.replace("/config/manifest-templates/blank.json", "https://cosme.unicampania.it/iiif/cosme/carditello_calvi")
infile.close()
outf = open("data/or3/manifests/platee/carditello_calvi_f_v2.json", "w")
outf.write(text_file)

