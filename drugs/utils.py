from xml.etree import ElementTree as ET
from tqdm import tqdm
import pandas as pd
import re

import re


def id_handler(element, dat):
    if 'primary' in element.attrib and element.attrib['primary'] == 'true':
        dat['primary-id'] = element.text
    else:
        dat['secondary-id'] = dat.get('secondary-id', [])+[element.text]
    return dat


def copy_text(element, dat, key):
    dat[key] = element.text if element.text else ''
    return dat


def parse_headings(element, dat, key):
    if element.text is None:
        dat[key] = ''
        return dat
    current_dict = {}
    sl = element.text.split('**')
    if len(sl) == 1:
        dat[key] = sl[0]
        return dat
    if sl[0] != '':
        for i, j in zip(sl[1::2], sl[2::2]):
            current_dict[i] = j
        dat[key] = [sl[0], current_dict]
    else:
        for i, j in zip(sl[1::2], sl[2::2]):
            current_dict[i] = j
        dat[key] = current_dict
    return dat


def parse_bullets(element, dat, key):

    if element.text is None:
        dat[key] = ''
        return dat
    if key in dat and not isinstance(dat[key], str):
        return dat

    sl = element.text.split('*')
    if len(sl) == 1:
        dat[key] = sl[0]
        return dat

    current_dict = []
    if sl[0] != '':
        for j in sl[1:]:
            current_dict.append(j)
        dat[key] = [sl[0], current_dict]
    else:
        for j in sl[1:]:
            current_dict.append(j)
        dat[key] = current_dict

    return dat


def pipeline1(element, dat, key):
    dat = parse_headings(element, dat, key)
    return parse_bullets(element, dat, key)


def pipeline2(element, dat, key):
    dat = parse_bullets(element, dat, key)

    if element.text is None:
        dat[key] = ''
        return dat

    if key in dat and isinstance(dat[key], str):
        return dat

    current_dict = {}
    no_keys = []

    for i in dat[key]:
        #         print('here')
        if isinstance(i, str) and i != '':
            k = re.findall('\[([^\]]*)\][\r]*[\n]*$', i)
            if len(k) == 0:
                no_keys.append(i)
                continue
            k = k[0]
            value = re.sub('\[([^\]]*)\][\r]*[\n]*$', '', i).strip()

            current_dict[k] = value

    current_dict = current_dict if len(
        no_keys) == 0 else no_keys+[current_dict] if len(current_dict) > 0 else no_keys
    dat[key] = current_dict
    return dat


def display_elem(element):
    print('**************************')
    print(element.tag)
    print(element.text)
    print(element.attrib)
    print(list(element))


def name_handler(element, dat): return copy_text(element, dat, 'name')


def description_handler(element, dat): return copy_text(
    element, dat, 'description')

# Handle bullet points


def indication_handler(element, dat): return pipeline1(
    element, dat, 'indication')


def pharmacodynamics_handler(element, dat): return copy_text(
    element, dat, 'pharmacodynamics')


def moa_handler(element, dat): return pipeline1(element, dat, 'moa')


def state_handler(element, dat): return copy_text(element, dat, 'state')


def unii_handler(element, dat): return copy_text(element, dat, 'unii')


def cas_handler(element, dat): return copy_text(element, dat, 'cas')

# Re-visit


def groups_handler(element, dat): return dat  # display_elem(element)

# Contains acronyms to be resolved eg: LD_50


def toxicity_handler(element, dat): return pipeline1(element, dat, 'toxicity')


def metabolism_handler(element, dat): return pipeline1(
    element, dat, 'metabolism')


def absorption_handler(element, dat): return pipeline1(
    element, dat, 'absorption')


def halflife_handler(element, dat): return pipeline1(element, dat, 'halflife')

# text saying "not available"


def proteinbinding_handler(element, dat): return copy_text(
    element, dat, 'proteinbinding')


def roe_handler(element, dat): return copy_text(element, dat, 'roe')


def vod_handler(element, dat): return pipeline2(element, dat, 'vod')


def clearance_handler(element, dat): return pipeline2(
    element, dat, 'clearance')


def classification_handler(element, dat):

    #     display_elem(element)
    single_valued_keys = {'description', 'direct-parent',
                          'kingdom', 'superclass', 'class', 'subclass'}
    if len(list(element)) == 0:
        return dat
    for i in element:
        if i.tag[24:] in single_valued_keys:
            dat[i.tag[24:] if i.tag[24:] !=
                'description' else 'introduction'] = i.text
        else:
            dat[i.tag[24:]] = dat.get(i.tag[24:], [])+[i.text]
    return dat


def salts_handler(element, dat):
    if len(list(element)) == 0:
        dat['salts'] = ''
        return dat
    salt_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        salt_list.append(props)
    dat['salts'] = salt_list
    return dat


def synonyms_handler(element, dat):
    #     display_elem(element)
    if len(list(element)) == 0:
        dat['synonyms'] = ''
        return dat
    synonym_list = []
    for i in element:

        props = {'name': i.text,
                 'language': i.attrib['language'],
                 'identifiedin': i.attrib['coder']}
        synonym_list.append(props)
    dat['synonyms'] = synonym_list
    return dat


def categories_handler(element, dat):
    if len(list(element)) == 0:
        dat['categories'] = ''
        return dat
    categories_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        categories_list.append(props)
    dat['categories'] = categories_list
    return dat


def ao_handler(element, dat):
    #     display_elem(element)
    if len(list(element)) == 0:
        dat['ao'] = ''
        return dat
    dat['ao'] = [i.text for i in element]
    return dat


def dosages_handler(element, dat):
    if len(list(element)) == 0:
        dat['dosages'] = ''
        return dat
    dosage_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        dosage_list.append(props)
    dat['dosages'] = dosage_list
    return dat


def fdalabel_handler(element, dat): return copy_text(element, dat, 'fdalabel')


def msds_handler(element, dat): return copy_text(element, dat, 'msds')


def patents_handler(element, dat):
    if len(list(element)) == 0:
        dat['patents'] = ''
        return dat
    patent_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        patent_list.append(props)
    dat['patents'] = patent_list
    return dat


def sequences_handler(element, dat):
    if len(list(element)) == 0:
        dat['sequences'] = ''
        return dat
    sequence = {}
    for i in element:
        sequence[i.text.split('\n')[0][1:]] = i.text.split('\n')[1]
    dat['sequences'] = sequence
    return dat


def ep_handler(element, dat):
    if len(list(element)) == 0:
        dat['ep'] = ''
        return dat
    ep_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        ep_list.append(props)
    dat['ep'] = ep_list
    return dat


def pathways_handler(element, dat):
    if len(list(element)) == 0:
        dat['pathway'] = ''
        return dat
    ep_list = []
    for pathway in element:
        props = {j.tag[24:]: j.text for j in pathway if j not in {
            'drugs', 'enzymes'}}
        ep_list.append(props)
    dat['pathway'] = ep_list
    return dat


def reactions_handler(element, dat):
    # display_elem(element)
    if len(list(element)) == 0:
        dat['reactions'] = ''
        return dat

    def fill_dict(di, l, r):
        di['left'] = di.get('left', [])+[l]
        di['right'] = di.get('right', [])+[r]
        return di
    reaction_list = {}
    for pathway in element:
        props = {j.tag[24:]: j for j in pathway}
        le_info = {i.tag[24:]: i.text for i in props['left-element']}
        re_info = {i.tag[24:]: i.text for i in props['right-element']}
        reaction_list[props['sequence'].text] = fill_dict(
            reaction_list.get(props['sequence'].text, dict()), le_info, re_info)

    dat['reactions'] = reaction_list
    return dat


def snpeffects_handler(element, dat):
    if len(list(element)) == 0:
        dat['effects'] = ''
        return dat
    effect_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        effect_list.append(props)
    dat['effects'] = effect_list
    return dat


def gr_handler(element, dat):
    if len(list(element)) == 0:
        dat['references'] = ''
        return dat
    ref_list = []
    for i in element:
        for j in i:
            props = {k.tag[24:]: k.text for k in j}
            ref_list.append(props)
    dat['references'] = ref_list
    return dat


def sr_handler(element, dat): return copy_text(element, dat, 'synthesis_ref')


def ei_handler(element, dat):
    if len(list(element)) == 0:
        dat['external_identifiers'] = ''
        return dat
    ei_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        ei_list.append(props)
    dat['external_identifiers'] = ei_list
    return dat


def el_handler(element, dat):
    if len(list(element)) == 0:
        dat['external_links'] = ''
        return dat
    ei_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        ei_list.append(props)
    dat['external_links'] = ei_list
    return dat


def fi_handler(element, dat):
    if len(list(element)) == 0:
        dat['food_interactions'] = ''
        return dat
    ei_list = []
#     display_elem(element)
    for i in element:
        ei_list.append(i.text)
    dat['food_interactions'] = ei_list
    return dat


def di_handler(element, dat):
    if len(list(element)) == 0:
        dat['drug_interactions'] = ''
        return dat
    ei_list = []
    for i in element:
        props = {j.tag[24:]: j.text for j in i}
        ei_list.append(props)
    dat['drug_interactions'] = ei_list
    return dat


fmap = {'drugbank-id': id_handler,
        'name': name_handler,
        'description': description_handler,
        'indication': indication_handler,
        'pharmacodynamics': pharmacodynamics_handler,
        'mechanism-of-action': moa_handler,
        'state': state_handler,
        'unii': unii_handler,  # unique ingredient identifier
        'cas-number': cas_handler,  # chemical abstract service
        'groups': groups_handler,
        'toxicity': toxicity_handler,
        'metabolism': metabolism_handler,
        'absorption': absorption_handler,
        'half-life': halflife_handler,
        'protein-binding': proteinbinding_handler,
        'route-of-elimination': roe_handler,
        'volume-of-distribution': vod_handler,
        'clearance': clearance_handler,
        'classification': classification_handler,
        'salts': salts_handler,
        'synonyms': synonyms_handler,
        'categories': categories_handler,
        'affected-organisms': ao_handler,
        'dosages': dosages_handler,
        'fda-label': fdalabel_handler,
        'msds': msds_handler,
        'patents': patents_handler,
        'sequences': sequences_handler,
        'experimental-properties': ep_handler,
        'pathways': pathways_handler,
        'reactions': reactions_handler,
        'snp-effects': snpeffects_handler,
        'general-references': gr_handler,
        'synthesis-reference': sr_handler,
        'external-identifiers': ei_handler,
        'external-links': el_handler,
        'food-interactions': fi_handler,
        'drug-interactions': di_handler
        }


def parse_drug(drug):
    dat = {}
    # print(drug[0].text)
    for child in drug:
        try:
            dat = fmap[child.tag[24:]](child, dat)
        except KeyError as e:
            pass
        except Exception as e:
            print(child.tag)
            print(dat)
            print(e)
            raise UndefinedError
    return dat


def get_from_excel(name, feature, df):
    try:
        val = df[df['Drug'] == name.lower()][feature].values[0]
        return val if isinstance(val, str) else ''
    except:
        return ''
