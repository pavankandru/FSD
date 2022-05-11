from re import template
from tokenize import Name
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from sklearn.utils import resample
from genXML import tewiki, writePage
import re
import json

def getImage(url):
    return url.rsplit('/', 1)[-1]


def getData(datarow, resIdentifier, fi_str, c1_str, d1_str, r1_str, l1_str, adv_str, specP_str, class1, ind1_str):
    data = {

# {'Administration': '',
#   'Adverse Reactions': 'मतली,उल्टी करना,अपच,सरदर्द,चक्कर आना,शक्तिहीनता,एलर्जी,स्वप्रतिपिंडों का विकास,बुखार,हल्के से मध्यम इंजेक्शन साइट प्रतिक्रियाएं,जैसे,पर्विल,खुजली,दर्द,सूजन,.संभावित रूप से घातक,गंभीर संक्रमण,पूति,जैसे,भी,आक्रामक फंगल संक्रमण,,कैंसर,जैसे,स्तन,फेफड़ा,त्वचा कैंसर,लिंफोमा,,कभी-कभार,पैन्टीटोपेनिया,अप्लास्टिक एनीमिया,केंद्रीय,परिधीय demyelinating घटनाएं,एक प्रकार का वृक्ष,ल्यूपस से संबंधित स्थितियां,वाहिकाशोथ,तीव्रग्राहिता.',
#   'Contraindications': 'पूति या पूति का खतरा,पुराने या स्थानीय संक्रमण सहित सक्रिय संक्रमण।',
#   'Overdosage': '',
#   'Special Precautions': 'रोगी w / आवर्ती या पुराने संक्रमण का इतिहास या w / अंतर्निहित स्थितियां जो रोगी को संक्रमण के लिए प्रेरित कर सकती हैं,जैसे,उन्नत या खराब नियंत्रित डीएम,,पिछला हेपेटाइटिस बी वायरस संक्रमण,हेपेटाइटिस सी का इतिहास,रक्त डिस्क्रेसियस,पूर्व-मौजूदा या हाल ही में डिमाइलेटिंग रोग की शुरुआत,सीएफ़एफ़,मध्यम से गंभीर मादक हेपेटाइटिस,चाइल्डनो,गर्भावस्था,दुद्ध निकालना,मॉनिटरिंग पैरामीटर सीबीसी के साथ / अंतर की निगरानी करें,संक्रमण के लक्षण/लक्षण,निम्न से पहले,दौरान,चिकित्सा के बाद,,दिल की धड़कन रुकना,अतिसंवेदनशीलता प्रतिक्रियाएं,ल्यूपस जैसा सिंड्रोम,द्रोह,गुप्त टीबी के लिए स्क्रीनिंग करें,निम्न से पहले,चिकित्सा के दौरान,,हेपेटाइटिस बी वायरस,एचबीवी,,एचबीवी वाहक।',
#   'Storage': 'चमड़े के नीचे का,2-8°C . के बीच स्टोर करें,रौशनी से सुरक्षा,स्थिर नहीं रहो।',
#   'absorption': 'आरए के साथ वयस्कों में जनसंख्या फार्माकोकाइनेटिक मॉडलिंग,जैसा,या जो स्वस्थ थे उन्होंने 0.0223/एच के केए के साथ 56.9% की एक उपचर्म जैवउपलब्धता दिखाई। [ए 215352] बाल चिकित्सा जेआईए रोगियों में एक अन्य मॉडल ने 215% की उच्च औसत अंतर-व्यक्तिगत परिवर्तनशीलता के साथ 0.05 / एच की बढ़ी हुई केए को दिखाया। [ए 215357] सीमैक्स। एनब्रेल की एक 25 मिलीग्राम उपचर्म खुराक के बाद 69 एच के टीएमएक्स के साथ 1.1 एमसीजी/एल के रूप में रिपोर्ट किया गया है।,बाल चिकित्सा जेआईए रोगियों में 2.1 एमसीजी साप्ताहिक दो बार 0.4 मिलीग्राम / किग्रा की खुराक के साथ।',
#   'food_interactions': '',
#   'halflife': 'Etanercept का RA रोगियों में 102 घंटे के उन्मूलन का औसत आधा जीवन है। [L14862] जनसंख्या मॉडल ने स्वस्थ वयस्कों में 68 घंटे का औसत आधा जीवन दिखाया है।,बाल चिकित्सा JIA रोगियों में 70.7-94.8 घंटे। [A215657, A215357]',
#   'indication': 'Etanercept वयस्कों में मध्यम से गंभीर रूप से सक्रिय संधिशोथ के उपचार के लिए संकेत दिया गया है,4 वर्ष की आयु के रोगियों में पुरानी मध्यम से गंभीर पट्टिका सोरायसिस में,पुराना। [L14862] इसका उपयोग संकेतों को प्रबंधित करने के लिए भी किया जाता है,2 वर्ष की आयु के लोगों में पॉलीआर्टिकुलर इडियोपैथिक गठिया के लक्षण,बड़े,Etanercept का उपयोग सोरियाटिक गठिया के लक्षणों के प्रबंधन के लिए भी किया जाता है,रीढ़ के जोड़ों में गतिविधि-रोधक सूजन,',
#   'metabolism': 'चूंकि etanercept एक संलयन प्रोटीन एंटीबॉडी है,यह अंतर्जात प्रोटीन के समान प्रोटीन के माध्यम से चयापचय किया जाता है।',
#   'name': 'एटानेरसेप्ट',
#   'pharmacodynamics': 'Etanercept विशेष रूप से ट्यूमर नेक्रोसिस कारक को बांधता है,टीएनएफ,,इस प्रकार टीएनएफ द्वारा प्रेरित या विनियमित जैविक प्रक्रियाओं को नियंत्रित करता है। [एल 14862, ए 216522] प्रभावित ऐसी प्रक्रियाओं या अणुओं में व्यक्त आसंजन अणुओं का स्तर शामिल है।,साथ ही साइटोकिन्स के सीरम स्तर,मैट्रिक्स मेटालोप्रोटीनिस।',
#   'proteinbinding': 'कोई महत्वपूर्ण प्रोटीन बंधन की पहचान नहीं की गई है।'},
        'info_Administration': datarow['Administration'],
        'protein_bound': datarow['proteinbinding'],
        'Storage': datarow['Storage'],
        'Pharmacodynamics': datarow["pharmacodynamics"],
        'elimination_half_life': datarow['halflife'],
        'Indication': ind1_str,

        'imageURL' : datarow['image'],
        'Classification' : class1,
        'info_state': datarow['state'],
        'Metabolism': datarow['metabolism'],
        'Name': datarow['name'],
        # 'imageURL': getImage(datarow[23]),
        'Absorption': datarow['absorption'],
        'Food_interactions': fi_str,
        'Categories': c1_str,
        'Drug_interactions': d1_str,
        'Adverse_Reactions': adv_str,
        'Contraindications': datarow['Contraindications'],
        'Overdosage': datarow['Overdosage'],
        'Special_Precautions': specP_str,
        'Description' : datarow['description'],
        'patents' : datarow['patents'],
        'Effects' : datarow['effects'],
        'Introduction' : datarow['introduction'],
        'Salts' : datarow['salts'],
        'Vod' : datarow['vod'],
        'Direct-parent' : datarow['direct-parent'],
        'Moa' : datarow['moa'],
        'Toxicity' : datarow['toxicity'],
        'Ao' : datarow['ao'],
        'Excretion' : datarow['roe'],
        'References' : r1_str,
        'External_links': l1_str,
        'Synthesis_ref' : datarow['synthesis_ref'],

        'CAS_number' : resIdentifier['CAS_number'],
        'CAS_supplemental' : resIdentifier['CAS_supplemental'],
        'PubChem' : resIdentifier['PubChem'], 
        'PubChemSubstance' : resIdentifier['PubChemSubstance'], 
        'IUPHAR_ligand': resIdentifier['IUPHAR_ligand'], 
        'DrugBank_Ref': resIdentifier['DrugBank_Ref'], 
        'DrugBank': resIdentifier['DrugBank'], 
        'ChemSpiderID_Ref': resIdentifier['ChemSpiderID_Ref'], 
        'ChemSpiderID' : resIdentifier['ChemSpiderID'], 
        'UNII_Ref': resIdentifier['UNII_Ref'], 
        'UNII': resIdentifier['UNII'], 
        'KEGG_Ref': resIdentifier['KEGG_Ref'], 
        'KEGG': resIdentifier['KEGG'],  
        'KEGG2': resIdentifier['KEGG2'],
        'ChEBI_Ref': resIdentifier['ChEBI_Ref'], 
        'ChEBI': resIdentifier['ChEBI'], 
        'ChEMBL': resIdentifier['ChEMBL'], 
        'NIAID_ChemDB': resIdentifier['NIAID_ChemDB'],
        'PDB_ligand': resIdentifier['PDB_ligand'], 
        'ATC_prefix' : resIdentifier['ATC_prefix'],
        'ATC_suffix' : resIdentifier['ATC_suffix'],
        'ATC_supplemental' : resIdentifier['ATC_supplemental'],
        'pregnancy_category' : resIdentifier['PregnancyFDA'],
        'melting_point' : resIdentifier['melting_point'],
        'boiling_point' : resIdentifier['boiling_point'],
        'solubility': resIdentifier['solubility'],
        'boiling_notes': resIdentifier['boiling_notes'],
        'melting_notes': resIdentifier['melting_notes'],
        'synonyms': resIdentifier['synonyms'],
        'amass': resIdentifier['amass'],
        'mmass': resIdentifier['mmass']
    }
    return data


def main():
    fileLoader = FileSystemLoader('./')
    env = Environment(loader=fileLoader)
    template = env.get_template('Template/drugsHindi.j2')

    # df = pd.read_csv(open('m2_json_out', 'r'))
    in_file = open('m1_sample_json_out','r')
    data= json.load(in_file)
    in_file.close()
    print("length of data", len(data))
    # df = df.fillna('NaN')

    xmlDump = open('drugs.xml', 'w')
    xmlDump.write(tewiki+'\n')

    # file = open('test.txt', 'w')
    initial_page_id = 900000

# | CAS_number         = 103-90-2
# | CAS_supplemental   = 
# | PubChem            = 1983
# | PubChemSubstance   = 46506142
# | IUPHAR_ligand      = 5239
# | DrugBank_Ref       = {{drugbankcite|correct|drugbank}}
# | DrugBank           = DB00316
# | ChemSpiderID_Ref   = {{chemspidercite|correct|chemspider}}
# | ChemSpiderID       = 1906
# | UNII_Ref           = {{fdacite|correct|FDA}}
# | UNII               = 362O9ITL9D
# | KEGG_Ref           = {{keggcite|correct|kegg}}
# | KEGG               = D00217
# | KEGG2              = C06804
# | ChEBI_Ref          = {{ebicite|correct|EBI}}
# | ChEBI              = 46195
# | ChEMBL_Ref         = {{ebicite|correct|EBI}}
# | ChEMBL             = 112
# | NIAID_ChemDB       = 
# | PDB_ligand         = TYL
# | synonyms           = N-acetyl-para-aminophenol (APAP)
#  [{'resource': 'Drugs Product Database (DPD)', 'identifier': '13175'},  {'resource': 'GenBank', 'identifier': 'J00228'}, {'resource': 'PharmGKB', 'identifier': 'PA10040'}, {'resource': 'Therapeutic Targets Database', 'identifier': 'DNC000788'}, {'resource': 'Wikipedia', 'identifier': 'Cetuximab'}, {'resource': 'ChEMBL', 'identifier': 'CHEMBL1201577'}, {'resource': 'RxCUI', 'identifier': '318341'}]    
    resList = ['CAS_number', 'CAS_supplemental', 'PubChem', 'melting_point', 'boiling_notes','boiling_point', 'melting_notes','solubility','amass', 'mmass','ATC_prefix', 'ATC_suffix', 'ATC_supplemental' 'PubChemSubstance', 'IUPHAR_ligand', 'DrugBank_Ref', 'DrugBank', 'ChemSpiderID_Ref', 'ChemSpiderID', 'UNII_Ref', 'UNII', 'KEGG_Ref', 'KEGG',  'KEGG2','ChEBI_Ref', 'ChEBI',  'ChEMBL', 'NIAID_ChemDB','PDB_ligand', 'synonyms' ]

    for i in range(len(data)):
    # for i in range(10):
        extIdfrs = dict()
        for kr in resList:
            extIdfrs[kr] = None
        row = data[i]

        extIdfrs['UNII'] = row['unii']

# "atc": {"C10AA03": [["C10AA", "HMG CoA reductase inhibitors"], ["C10A", "LIPID MODIFYING AGENTS, PLAIN"], 
# ["C10", "LIPID MODIFYING AGENTS"], ["C", "CARDIOVASCULAR SYSTEM"]], "C10BA03": 
# [["C10BA", "HMG CoA reductase inhibitors in combination with other lipid modifying agents"], 
# ["C10B", "LIPID MODIFYING AGENTS, COMBINATIONS"], ["C10", "LIPID MODIFYING AGENTS"], ["C", "CARDIOVASCULAR SYSTEM"]], 
# "C10BX02": [["C10BX", "HMG CoA reductase inhibitors, other combinations"], 
# ["C10B", "LIPID MODIFYING AGENTS, COMBINATIONS"], ["C10", "LIPID MODIFYING AGENTS"], 
# ["C", "CARDIOVASCULAR SYSTEM"]]},
# | ATC_prefix         = N02
# | ATC_suffix         = BE01
# | ATC_supplemental   = {{ATC|N02|BE51}} {{ATC|N02|BE71}}
        atc1 = row['atc']
        atc1_str = ''
        firstATC = True
        if atc1 != None:
            for atcat1 in atc1.keys():
                if firstATC:
                    extIdfrs['ATC_prefix'] = atcat1[0:3]
                    extIdfrs['ATC_suffix'] = atcat1[3:]
                    firstATC = False
                else:
                    atc1_str = atc1_str+ '{{ATC|' + atcat1[0:3] + '|' + atcat1[3:]+'}} '
        extIdfrs['ATC_supplemental'] = atc1_str

        extIdfrs['PregnancyFDA'] = row['pregnancy category (us fda)']
        extIdfrs['amass'] = row['amass']    
        extIdfrs['mmass'] = row['mmass']    
        # 'melting_point', 'boiling_point', 'solubility'
        if 'ep' in row.keys():
            chemEP = row['ep']
            print(chemEP)    
            for chem1 in chemEP:
                if 'Boiling Point' == chem1['kind']:
                    extIdfrs['boiling_point'] = chem1['value']
                    extIdfrs['boiling_notes'] = chem1['source']
                if 'Melting Point' == chem1['kind']:
                    extIdfrs['melting_point'] = chem1['value']
                    extIdfrs['melting_notes'] = chem1['source']
                if 'Water Solubility' == chem1['kind']:
                    extIdfrs['solubility'] = chem1['value']

        extIdfrs['synonyms'] = row['synonyms']        
        extIdfrs['CAS_number'] = row['cas']
        extIdfrs['DrugBank'] = row['primary-id']

        idfrs = row['external_identifiers']
        for kr in idfrs: 
            extIdfrs[kr['resource']] = kr['identifier']
            if kr['resource'] == 'KEGG Drug':
                extIdfrs['KEGG'] = kr['identifier']
            if kr['resource'] == 'ChemSpider':
                extIdfrs['ChemSpiderID'] = kr['identifier']
            if kr['resource'] == 'ChEBI':
                extIdfrs['ChEBI'] = kr['identifier']
            if kr['resource'] == 'PubChem Substance':
                extIdfrs['PubChemSubstance'] = kr['identifier']

        # print(extIdfrs)
        f1_str = ''
        f1 = row['food_interactions']
        if f1 != '' and f1 != None:
            f1_str = re.sub('\[', '', f1)
            f1_str = re.sub('\]', '', f1_str)

        print(f1_str)

        # "Indicatio" convert to bullet points
        ind1_str = ''
        ind1 = row['indication']
        if ind1 != '' and ind1 != None:
            ind1_str = re.sub('\', \[\'', '<ul><li>', ind1)
            ind1_str = re.sub('\', \'', '</li>\n<li>', ind1_str)
            ind1_str = re.sub('\'\]', '</li>\n</ul>', ind1_str)
            ind1_str = re.sub('\[', '', ind1_str)
            ind1_str = re.sub('\]', '', ind1_str)
            ind1_str = re.sub('\'', '', ind1_str)
        # print(ind1_str)
        # print("\n")

        c1 = row['categories']
        c1_str = ''
        if c1 != None:
            for cat1 in c1:
                categoryName = cat1['category']
                c1_str = c1_str+ '[[Category: '+ categoryName + "]]\n"
        
        d1 = row['Drug Interactions']
        d1_str = d1
        # engName = row['engName']
        # n1 = row['name']
        # d1_str = ''
        # if d1 != None:
        #     d1_str = '<table border="1" class="dataframe"><tr><th>दवाई</th><th>पारस्परिक प्रभाव</th></tr>'
        #     for dr1 in d1:
        #         if 'description' in dr1.keys() and 'name' in dr1.keys():
        #             des = dr1['description']
        #             des1 = des.replace(engName, n1)
        #             des = re.sub('प्रतिकूल प्रभावों के जोखिम या गंभीरता को तब बढ़ाया जा सकता है', 'प्रतिकूल प्रभावों के जोखिम बढ़ जाते हैं', des1)
        #             des = re.sub('को तब बढ़ाया जा सकता है', 'तब बढ़ सकता है', des)
        #             d1_str = d1_str+ '<tr><td>'+dr1['name']+'</td><td>'+des+'</td></tr>'
        #     d1_str = d1_str+ '</table>'


        class1= ''
        class1 = '<table border="1" class="dataframe">'
        class1 = class1+ '<tr><td>'+ 'साम्राज्य' +'</td><td>'+ row['kingdom']+'</td></tr>'
        class1 = class1+ '<tr><td>'+ 'सुपर वर्ग' +'</td><td>'+ row['superclass']+'</td></tr>'
        class1 = class1+ '<tr><td>'+ 'वर्ग' +'</td><td>'+ row['class']+'</td></tr>'
        class1 = class1+ '<tr><td>'+ 'उप वर्ग' +'</td><td>'+ row['subclass']+'</td></tr>'   
        class1 = class1+ '</table>'    

        # r1 = row['references']
        engName = row['engName']
        name = row['name']
        r1_str = ''
        # if r1 != None:
        #     for rr1 in r1:
        #         if 'citation' in rr1.keys():
        #             r1_str = r1_str+ '<ref>' + rr1['citation'] + '</ref>'
        #         else:
        #             if 'title' in rr1.keys():
        #                 r1_str = r1_str+ '<ref>' + rr1['title'] + '</ref>'
                        
        l1 = row['external_links']
        engName = row['engName']
        name = row['name']
        l1_str = ''
        # if l1 != None:
        #     for ll1 in r1:
        #         if 'resource' in ll1.keys():
        #             l1_str = l1_str+ ll1['resource'] 
        #         if 'url' in ll1.keys():
        #             l1_str = l1_str+ ' at ' + ll1['url'] + "\n"
        #         else:
        #             l1_str = l1_str+ "\n"

        adv= row['Adverse Reactions']
        adv_str = ''
        adv_str2 = ''
        if 'संभावित रूप से घातक' in adv:
            advList = re.split('\',{\'संभावित रूप से घातक\',', adv)
            for advl1 in advList:
                if adv_str == '':
                    advl1 = re.sub('\[\'', '', advl1)
                    adv_str = adv_str + advl1
                else:
                    advList2 = re.split(',\' दुर्लभ\',', advl1)
                    for advl2 in advList2:
                        if adv_str2 == '':
                            adv_str2 = adv_str2 + '\n <B> संभावित रूप से घातक: </B>'  + advl2
                        else:
                            adv_str2 = adv_str2 + '\n <B> दुर्लभ: </B>' + advl2
                    adv_str2 = re.sub('\'\}\]', '', adv_str2)
                    adv_str = adv_str + adv_str2   

        # print(adv_str)

        specP= row['Special Precautions']
        print(specP)
        specP_str = ''
        if "मॉनिटरिंग पैरामीटर्स" in specP:
            spList = re.split("मॉनिटरिंग पैरामीटर्स", specP)
            for sp1 in spList:
                if specP_str == '':
                    specP_str = specP_str + sp1
                else:
                    specP_str = specP_str + '\n <B> मॉनिटरिंग पैरामीटर्स: </B>' + sp1
        else:
            specP_str = specP

        text = template.render(getData(row,extIdfrs, f1_str, c1_str, d1_str, r1_str, l1_str, adv_str, specP_str, class1, ind1_str))
        title = row['name']
        # print(title)
        writePage(initial_page_id, title, text, xmlDump)
        initial_page_id += 1
        # file.write(text)

    xmlDump.write('</mediawiki>')
    xmlDump.close()

if __name__ == '__main__':
    main()
