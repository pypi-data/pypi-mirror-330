import json
from read_rkf.parserkf import KFFile

def rkf_to_json(rkffile):
    '''
    Creating a jsonize extension of the rkf file
    '''
    data = KFFile(rkffile)
    json_data = {}
    all_sections = data.sections()
    for sections in all_sections:
        json_data[sections] =  data.read_section(sections)
    json_object = json.dumps(json_data, indent=4)
    return json_object

def rkf_to_dict(rkffile):
    '''
    return a python dictionary of an rkf file
    '''
    data = KFFile(rkffile)
    json_data = {}
    all_sections = data.sections()
    for sections in all_sections:
        json_data[sections] =  data.read_section(sections)
    return json_data
