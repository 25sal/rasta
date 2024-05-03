import json
from xml.etree import ElementTree as ET
import xmlformatter
with open("../data/manifest/index.json") as f:
    data = json.load(f)

root = ET.Element("ead")
eadheader = ET.SubElement(root,"eadheader")
eadid = ET.SubElement(eadheader,"eadid")
filedesc = ET.SubElement(eadheader,"filedesc")
titlestmt = ET.SubElement(eadheader,"titlestmt")
titleproper = ET.SubElement(titlestmt,"titleproper")

#ricercare titolo address 
archdesc = ET.SubElement(root, "archdesc")
archdesc.set("level", "collection")
archdesc.set("relatedencoding", "ISAD(G)v2")
dsc = ET.SubElement(archdesc, "dsc", type="combined")

max_url=5
i=0
def get_label_value(data):
    label = {
        "title" : ""
    }
    for item in data.get("metadata", []):
        if item.get("label") == "Title":
            #titles.append(item.get("value"))
            label["title"]=item.get("value")

    
            titleproper.text = label["title"]
           #devuu fare in modo che su dsc type =combined

# call the function to extract title values and update the EAD tree
def Search_dublincore(json_data):
    dc = {
        "Title": "",
        "Type": "",
        "Location": "",
        "Description": "",
        "Date": "",
        "Format": ""
    }
    a=0
    for item in json_data.get("metadata", []):
        if item.get("label") == "Title" and a==0:
            dc["Title"] = item.get("value")
            a+=1
        elif item.get("label")=="Title" and a>0:
            dc["title" + str(a)] = item.get("value")
            a+=1

        elif item.get("label") == "Type":
            dc["Type"] = item.get("value")
        elif item.get("label") == "Location":
            dc["Location"] = item.get("value")
        elif item.get("label") == "Description":
            dc["Description"] = item.get("value")
        elif item.get("label") == "Date":
            dc["Date"] = item.get("value")
           # print(dc["Date"])
        elif item.get("label") == "Format":
            dc["Format"] = item.get("value")
    
    return dc
label =Search_dublincore(data)
print(label["Title"])
print(label)
#print(test)

a=0
for seq in data.get("sequences", []):
    can = seq.get("canvases", [])
    for canvas in can:
        for image in canvas['images']:
            if i>=max_url:
                break
            
            image_url = image['resource']['@id']
            item = ET.SubElement(dsc, "c", level="item")
            did = ET.SubElement(item, "did")
            unititle = ET.SubElement(did,"unittitle")
            if a==0:

              unititle.text = label["Title"]
              a+=1
            else: 
                unititle.text = label["title" + str(a)]
                a+=1
            dao = ET.SubElement(did, "dao")
            dao.set("linktype", "simple")
            dao.set("href", image_url)
            dao.set("role", "master")
            dao.set("actuate", "onrequest")
            dao.set("show", "embed")
            i+=1
             
            
get_label_value(data)
tree = ET.ElementTree(root)
tree.write("../data/manifest/index.xml", )

formatter = xmlformatter.Formatter()
formatter.format_file("../data/manifest/index.xml")

