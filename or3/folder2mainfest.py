import glob
import shutil
import os
import json
import sys
from natsort import natsorted

def rename_files(file_path):
    filenames = glob.glob(file_path+"*.JPG")
    for filename in filenames:
        if "(" in filename:
            abs_name=filename[filename.index("(")+1:filename.index(")")];
            shutil.move(filename, file_path+abs_name+".jpg")
        




def create_sequence(base_url, collection, image_file, order):
    canvas = {}
    canvas["@id"] = base_url+"/"+collection+"/canvases/" +os.path.basename(image_file)
    canvas["@type"] = "sc:Canvas"
    canvas["height"] = 2736
    canvas["width"] =  3648
    canvas["label"] = os.path.basename(image_file)
    canvas["metadata"] = []
    canvas["images"] = []
    
    img = {}
    img["@id"] = base_url+"/"+collection + "/canvas/"+os.path.basename(image_file)+"/annotation_page/"+os.path.basename(image_file)
    img["@type"] = "oa:Annotation"
    img["motivation"] = "sc:painting"
    img["on"] = img["@id"]
    img["resource"] = {}
    img["resource"]["@id"] =  base_url+"/iiif/"+collection+"/"+os.path.basename(image_file)+"/full/max/0/default.jpg"
    img["resource"]["@type"] = "dctypes:Image"
    img["resource"]["format"] = "image/jpeg"
    img["resource"]["height"] = canvas["height"]
    img["resource"]["width"] = canvas["width"]
    img["resource"]["service"]  = {}
    img["resource"]["service"]["@context"] = "http://iiif.io/api/image/2/context.json"
    img["resource"]["service"]["profile"] = "http://iiif.io/api/image/2/level1.json"
    img["resource"]["service"]["@id"] = base_url+"/iiif/"+collection+"/"+os.path.basename(image_file)
    canvas["images"].append(img)
    return canvas
      
def convert_images(subdir):
    jpgs = glob.glob(subdir + '/*.JPG')
    # loop through all jpg files in the current subdir
    # esegui comando da shell
    for jpg in jpgs:
        os.system("vips im_vips2tiff "+jpg+" "+jpg[:-4]+".tif:deflate,tile:256x256,pyramid")


'''
rename file does not need if filename are ok
1) change platea in order to comply with the file_path where the images are
2) convert_images assumes images are *.JPG (capital letters)
3) Replace "10 Durazzano" with any lable describes the collections
4) base_url and collection match the current web server address
5) adapt width and height of images in create_sequence
'''

if __name__=="__main__":
    platea = "106_durazzano"
    file_path = "data/or3/manifests/platee/"+platea
    base_url = "https://cosme.unicampania.it"
    collection = "rasta/or3/platee/"+platea
    #rename_files(file_path)
    #convert_images(file_path)
    

    manifest_v2 = {}
    manifest_v2["@context"] = "http://iiif.io/api/presentation/2/context.json"
    manifest_v2["@id"] = base_url+"/"+collection+".json"
    manifest_v2["@type"] = "sc:Manifest"
    manifest_v2["label"] = "Platea 106 Durazzano"
    manifest_v2["description"] = "Platea 106 Durazzano"
    manifest_v2["metadata"] = []
    manifest_v2["metadata"].append({})
    manifest_v2["metadata"][0]["label"] ="any_label"
    manifest_v2["metadata"][0]["value"] ="any_value"
    manifest_v2["sequences"] = []
    sequence = {}
    sequence["@id"] = base_url+"/"+collection+"/sequence_0"
    sequence["@type"] =  "sc:Sequence"
    sequence["canvases"] = []
    manifest_v2["sequences"].append(sequence)

    

    filenames = glob.glob(file_path+"*.tif")
    filenames = natsorted(filenames)
    for i in range(len(filenames)):
        canvas = create_sequence(base_url,collection, filenames[i],i)
        manifest_v2["sequences"][0]["canvases"].append(canvas)
    with open("data/or3/manifests/platee/106_durazzano.json","w") as fout:
        json.dump(manifest_v2, fout, indent=4)
