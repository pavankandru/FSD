from xml.etree import ElementTree as ET
from tqdm import tqdm
import pandas as pd
import re
from utils import *
import json

root = './'

mims_data = pd.read_excel(root+'data/mims attribute data.xlsx')

count = 0
lvl_count = 0
f = open(root+'data/processed_data.jsonl', 'w', encoding='utf-8')

for event, element in tqdm(ET.iterparse(root+"data/full database.xml", events=("end", "start"))):
    if event == "start":
        lvl_count += 1

    elif element.tag == "{http://www.drugbank.ca}drug":
        lvl_count -= 1
        if lvl_count == 1:
            dat = parse_drug(element)
            for key in ['Administration', 'Contraindications', 'Special Precautions', 'Storage',
                        'Adverse Reactions', 'Overdosage', 'Pregnancy Category (US FDA)']:
                dat[key] = get_from_excel(dat['name'], key, mims_data)
            dat['Pregnancy Category (US FDA)'] = dat['Pregnancy Category (US FDA)'] if \
                len(dat['Pregnancy Category (US FDA)']) == 1 else ''

            dat['type'] = element.attrib['type']
            f.write(json.dumps(dat))
            f.write('\n')
#             druglist.append(dat)
            count += 1
            if count % 200 == 199:
                print('Processed ', count, ' drugs')
        element.clear()
    else:
        lvl_count -= 1

f.close()
