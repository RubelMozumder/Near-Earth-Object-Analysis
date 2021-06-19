"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
import numpy as np

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    search_header_name= ['name', 'pdes', 'diameter', 'pha'] 
    with open(PROJECT_ROOT/'neos.csv','r') as neocsv: 
        reader= csv.reader(neocsv) 
        header= np.array(next(reader)) 
        #header_name_index contains the corresponding index for name to search 
        header_name_index= [np.where(header==header_name)[0][0] for header_name in search_
    header_name] 
        # neo_infos is the list of arguments to used in the NearEarthObject class 
        neo_infos=[] 
        ii= 0 
        for data_line in iter(reader): 
            ii += 1 
            neo_info= dict() 
            for index in header_name_index: 
                if data_line[index] == None or data_line[index] == '': 
                    continue 
                neo_info[header[index]]=data_line[index]  
            neo_infos.append(neo_info) 

    # TODO: Load NEO data from the given CSV file.
    return ()


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    return ()
