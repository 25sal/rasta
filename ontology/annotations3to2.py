import json
import sys
import copy

ann_v2 = {
          '@type': "sc:AnnotationList",
          'resources' : [

            ],
        '@id': "http://localhost:8888/annotation/list/e98b708e1fb7d04c676f25e0eabfc7bb.json",
        '@context': "http://iiif.io/api/presentation/2/context.json"
        }
res_template = {
        '@id': "http://localhost:8888/annotation/1678220080557",
        '@type': "oa:Annotation",
        'dcterms:created': "2023-03-07T21:14:40",
        'dcterms:modified': "2023-03-07T21:14:40",
        'resource': [
            {
             '@type': "oa:Tag",
             'http://dev.llgc.org.uk/sas/full_text': "hallo",
              'chars': "hallo"
            },
            {
             '@type': "dctypes:Text",
             'http://dev.llgc.org.uk/sas/full_text': "",
             'format': "text/html",
             'chars': ""
            }
          ],
        'on': [
               {
                    '@type': "oa:SpecificResource",
                    'within': {
                    '@id': "https://dms-data.stanford.edu/data/manifests/BnF/jr903ng8662/manifest.json",
                    '@type': "sc:Manifest"
                              },
               'selector':
                    {
                     '@type': "oa:Choice",
                     'default':
                         {
                            '@type': "oa:FragmentSelector",
                            'value': "xywh=2158,511,580,310"
                        },
                    'item': {
                        '@type': "oa:SvgSelector",
                        'value': '<svg xmlns="http://www.w3.org/2000/svg"><path xmlns="http://www.w3.org/2000/svg" d='
                       }
                    },
               'full': "https://dms-data.stanford.edu/data/manifests/BnF/jr903ng8662/canvas/canvas-1"
                }
                ],
        'motivation': ["oa:commenting", "oa:tagging"],
        '@context': "http://iiif.io/api/presentation/2/context.json"
        }

# fin = open("../data/ontologies/annotationsv3.json", "r")

def a3to2(manifest_file):
    fin = open(manifest_file, "r")

    annotations = json.load(fin)
    manifest = annotations['id']
    annotations = annotations["annotations"]

    ann_v2['@id'] = 'https://cosme.unicampania.it/rasta/norba/annotation/list/123'

    svg_left = '<svg xmlns="http://www.w3.org/2000/svg"><path xmlns="http://www.w3.org/2000/svg" d='
    svg_right =  ' data-paper-data="{&quot;strokeWidth&quot;:1,&quot;rotation&quot;:0,&quot;deleteIcon&quot;:' \
                 'null,&quot;rotationIcon&quot;:null,&quot;group&quot;:null,&quot;editable&quot;:true,&quot;annotation&quot;:null}"' \
                 ' id="rectangle_4edd3b90-2281-4c5d-b856-dfa7d91a7067" fill-opacity="0" fill="#00bfff" fill-rule="nonzero"' \
                 ' stroke="#00bfff" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10"' \
                 ' stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none"' \
                 ' text-anchor="none" style="mix-blend-mode: normal"/></svg>'
    #template = "M2157.79168,511.38823h289.97078v0h289.97078v154.93771v154.93771h-289.97078h-289.97078v-154.93771z"
    i = 1
    for annotation_page in annotations:
        for annotation in annotation_page['items']:
            res_template['@id'] = "http://localhost:8888/annotation/111"+str(i)
            res_template['resource'][0]['http://dev.llgc.org.uk/sas/full_text'] = annotation['body']['value']
            res_template['resource'][0]['chars'] = annotation['body']['value']
            res_template['on'][0]['within']['@id'] = manifest
            target = annotation['target']
            value = target[target.index('#xywh=')+1:]
            res_template['on'][0]['selector']['default']['value'] = value

            dims = value[value.index("="):]
            dims = dims.split(",")
            svg_d = '"M'+dims[0]+","+dims[1]
            svg_d += 'h'+str(int(dims[2])/2)+"v0h"+str(int(dims[2])/2)+'v'+str(int(dims[3])/2)
            svg_d += 'v'+str(int(dims[3])/2)+"h-"+str(int(dims[2])/2)+"h-"+str(int(dims[2])/2)
            svg_d += 'v-'+str(int(dims[3])/2)+'z"'
            res_template['on'][0]['selector']['item']['value'] = svg_left+svg_d+svg_right
            res_template['on'][0]['full'] = target[:target.index('#xywh=')]
            ann_v2['resources'].append(copy.deepcopy(res_template))
            i +=1

    print(json.dumps(ann_v2, indent=2))



#a3to2("../data/manifest/norba_8.json")
a3to2("../data/pilots/norba/manifests/0-CISTERNE.json")