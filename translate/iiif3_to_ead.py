import json
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

publisher_text = "Dipartimento di lettere e beni culturali, Università della Campania Luigi Vanvitelli"

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












if __name__ == "__main__":
    manifest = "norba_acropoli"
    collection_id = "ITDILBEC01"
    sample_date = "2023-02-27"
    creator = 'Dipartimento di Beni Culturali, Università della Campania "Luigi Vanvitelli"'

    with open("../data/manifest/"+manifest+".json") as f:
        data = json.load(f)

        root = ET.Element("ead")
        eadheader = ET.SubElement(root, "eadheader")
        eadid = ET.SubElement(eadheader, "eadid")

        filedesc = ET.SubElement(eadheader, "filedesc")

        titlestmt = ET.SubElement(filedesc, "titlestmt")
        titleproper = ET.SubElement(titlestmt, "titleproper")

        # editionstmt = ET.SubElement(filedesc, "editionstmt")
        # edition = ET.SubElement(editionstmt, "edition")

        publicationstmt = ET.SubElement(filedesc, "publicationstmt")
        publisher = ET.SubElement(publicationstmt, "publisher")
        publisher.text = "Dipartimento di Lettere e Beni Culturali, Università della Campania Luigi Vanvitelli"

        creation_date = ET.SubElement(publicationstmt, "date")
        creation_date.set("normal", sample_date)
        creation_date.set("encodinganalog", sample_date)
        creation_date.text = sample_date

        address = ET.SubElement(publicationstmt, "address")
        addressline = ET.SubElement(address, "addressline")
        addressline.text = ""

        seriesstmt = ET.SubElement(filedesc, "seriesstmt")
        ser_titleproper = ET.SubElement(seriesstmt, "titleproper")

        # notestmt = ET.SubElement(filedesc,"notestmt")
        # note = ET.SubElement(notestmt,"note")

        profiledesc = ET.SubElement(eadheader, "profiledesc")
        # revisiondesc = ET.SubElement(eadheader,"revisiondesc")


        label =Search_dublincore(data)
        label["Title"] = data['label']['@none'][0]
        logger.debug("title:" + label["Title"])
        titleproper.text=label["Title"]
        titleproper.set("encodinganalog", 'title')

        # set id
        eadid.set("identifier", manifest)
        # eadid.set("mainagencycode", "")
        eadid.set("url", data['id'])
        eadid.text = collection_id



        '''
        Collection description
        '''
        archdesc = ET.SubElement(root, "archdesc")
        archdesc.set("level", "collection")
        archdesc.set("relatedencoding", "ISAD(G)v2")
        collection_did = ET.SubElement(archdesc, "did")



        # head = ET.SubElement(collection_did, "head")
        # abstract = ET.SubElement(collection_did, "abstract")

        unittitle = ET.SubElement(collection_did, "unittitle")
        unittitle.set("encodinganalog", "3.1.2")
        unittitle.text=manifest
        unitid = ET.SubElement(collection_did, "unitid")
        unitid.set("encodinganalog", "3.1.2")
        unitid.text = collection_id
        unitdate = ET.SubElement(collection_did, "unitdate")
        unitdate.set("encodinganalog", "3.1.2")
        unitdate.set("normal", sample_date+"/"+sample_date)
        unitdate.text = sample_date
        origination = ET.SubElement(collection_did, "origination")
        origination.set("encodinganalog", "3.1.2")
        origination_name = ET.SubElement(origination, "name")
        origination_name.set("encodinganalog", "3.1.2")
        origination_name.text = creator





        '''
        Collection content
        '''
        dsc = ET.SubElement(archdesc, "dsc")
        dsc.set("type", "combined")



        '''
        scan canvases
        '''
        n_images=0
        for item in data.get("items", []):
            if item['type'] == "Canvas":
                images = item['items'][0]['items']
                for canvas_image in images:
                    # logger.debug(canvas_image)
                    if canvas_image['motivation'] == "painting":
                        if canvas_image['body']['type'] == "Image":
                            image_url = canvas_image['body']['service'][0]['@id']+"/full/,120/0/default.jpg"
                            logger.debug(image_url)



                            item = ET.SubElement(dsc, "c", level="item")
                            did = ET.SubElement(item, "did")
                            unitid =  ET.SubElement(did, "unitid")
                            unitid.text = canvas_image['body']['id']

                            unititle = ET.SubElement(did,"unittitle")
                            unititle.text = canvas_image['body']['label']['@none'][0]

                            physdesc = ET.SubElement(did, "physdesc")
                            physdesc.set("encodinganalog", "3.1.5")
                            physdesc.text = "IIIF Images"

                            unitdate =  ET.SubElement(did,"unitdate")
                            unitdate.set("encodinganalog","3.1.3")
                            unitdate.text = sample_date

                            dao = ET.SubElement(did, "dao")
                            dao.set("linktype", "simple")
                            dao.set("href", image_url)
                            dao.set("role", "master")
                            dao.set("actuate", "onrequest")
                            dao.set("show", "embed")
                            n_images+=1

        # extent and media
        physdesc = ET.SubElement(collection_did, "physdesc")
        physdesc.set("encodinganalog","3.1.5")
        physdesc.text = str(n_images)+" IIIF Images"

        get_label_value(data)
        tree = ET.ElementTree(root)


        ET.indent(tree, space="\t", level=0)
        dtd = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE ead PUBLIC "+//ISBN 1-931666-00-8//DTD ead.dtd (Encoded Archival Description (EAD) Version 2002)//EN"' \
              ' "http://lcweb2.loc.gov/xmlcommon/dtds/ead2002/ead.dtd">'

        with open('../data/manifest/'+manifest+'_ead.xml', 'wb') as f:
            f.write(dtd.encode('utf8'))
            tree.write(f, 'utf-8')



