import json
from xml.etree import ElementTree as ET


def get_label_value(data):
    label = {
        "title": ""
    }
    for item in data.get("metadata", []):
        if item.get("label") == "Title":
            # titles.append(item.get("value"))
            label["title"] = item.get("value")

            titleproper.text = label["title"]

        # devuu fare in modo che su dsc type =combined


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




root = ET.Element("ead")
eadheader = ET.SubElement(root, "eadheader")
eadid = ET.SubElement(eadheader, "eadid")
filedesc = ET.SubElement(eadheader, "filedesc")

titlestmt = ET.SubElement(filedesc, "titlestmt")
titleproper = ET.SubElement(titlestmt, "titleproper")

editionstmt = ET.SubElement(filedesc, "editionstmt")
edition = ET.SubElement(editionstmt, "edition")

publicationstmt = ET.SubElement(filedesc, "publicationstmt")
publisher = ET.SubElement(publicationstmt, "publisher")
publisher.text = ""
address = ET.SubElement(publicationstmt, "address")
addressline = ET.SubElement(address, "addressline")
addressline.text = ""

seriesstmt = ET.SubElement(filedesc, "seriesstmt")
titleproper = ET.SubElement(seriesstmt, "titleproper")

# notestmt = ET.SubElement(filedesc,"notestmt")
# note = ET.SubElement(notestmt,"note")

profiledesc = ET.SubElement(eadheader, "profiledesc")
# revisiondesc = ET.SubElement(eadheader,"revisiondesc")


# ricercare titolo address
archdesc = ET.SubElement(root, "archdesc")
archdesc.set("level", "collection")
archdesc.set("relatedencoding", "ISAD(G)v2")
did = ET.SubElement(archdesc, "did")
head = ET.SubElement(did, "head")
abstract = ET.SubElement(did, "abstract")
dsc = ET.SubElement(archdesc, "dsc")
dsc.set("type", "combined")

max_url = 5
i = 0



manifest = "norba_acropoli"

with open("../data/manifest/"+manifest+".json") as f:
    data = json.load(f)



label =Search_dublincore(data)
label["Title"] = data['label']
print(label["Title"])
print(label)
#print(test)

a=0
for seq in data.get("sequences", []):
    can = seq.get("canvases", [])
    for canvas in can:
        for image in canvas['images']:

            
            image_url = image['resource']['@id']
            item = ET.SubElement(dsc, "c", level="item")
            did = ET.SubElement(item, "did")
            unititle = ET.SubElement(did,"unittitle")
            if a==0:

              unititle.text = label["Title"]
              a+=1
            else: 
              unititle.text = label["Title"]
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


ET.indent(tree, space="\t", level=0)
dtd = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE ead PUBLIC "+//ISBN 1-931666-00-8//DTD ead.dtd (Encoded Archival Description (EAD) Version 2002)//EN"' \
      ' "http://lcweb2.loc.gov/xmlcommon/dtds/ead2002/ead.dtd">'

with open('../data/manifest/'+manifest+'_ead.xml', 'wb') as f:
    f.write(dtd.encode('utf8'))
    tree.write(f, 'utf-8')



