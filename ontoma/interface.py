# -*- coding: utf-8 -*-
__all__ = ["OnToma"]

from ontoma.downloaders import get_omim_to_efo_mappings
from ontoma.query import ols
from ontoma.ols import OlsClient

from ontoma import URLS

import requests
import csv
import json
from io import BytesIO, TextIOWrapper
import obonet
import python_jsonschema_objects as pjs 

import logging
logger = logging.getLogger(__name__)

# if you want to use across classes
# _cache = {"files":None}


class OnToma(object):
    '''Open Targets ontology mapping cascade

    if you have an id, find a xref to EFO
    elif search exact match to name in EFO (or synonyms)
    elif search fuzzy match to name in EFO
    elif search in OLS
    elif search in Zooma High confidence set

    Initialize the class (which will download EFO,OBO and others):
    >>> t=OnToma()

    We can now lookup "asthma" and get:
    >>> t.efo_lookup('asthma')
    'EFO:0000270'

    We can now lookup "Phenotypic abnormality" on HP: 
    >>> t.hp_lookup('Phenotypic abnormality')
    'HP:0000118'

    Lookup in OLS
    >>> t.ols_lookup('asthma')
    'EFO:0000270'

    OMIM code lookup
    TODO: should have a logic for what is the better hit here
    >>> t.omim_lookup('230650')
    ['http://www.orpha.net/ORDO/Orphanet_354','http://www.orpha.net/ORDO/Orphanet_79257']
    

    Searching the ICD9 code for 'other dermatoses' returns EFO's skin disease:
    >>> t.oxo_lookup('702')
    'EFO:0000701'
    '''

    def __init__(self, efourl = URLS.EFO, 
                        hpurl = URLS.HP):

        self.logger = logging.getLogger(__name__)

        '''Parse the ontology obo files for exact match lookup'''
        self._efo = obonet.read_obo(efourl)
        self.logger.info('EFO parsed. Size: {} nodes'.format(len(self._efo)))
        self._hp = obonet.read_obo(hpurl)
        self.logger.info('HP parsed. Size: {} nodes'.format(len(self._hp)))

        '''Create name mappings'''

        # id_to_name = {id_: data['name'] for id_, data in efo.nodes(data=True)}
        self.name_to_efo = {data['name']: id_ 
                            for id_, data in self._efo.nodes(data=True)}
        
        self.name_to_hp = {data['name']: id_ 
                           for id_, data in self._hp.nodes(data=True)}

        '''Initialize API clients'''

        self._ols = OlsClient(ontology=['efo'],field_list=['short_form'])
        # self.zooma = get_opentargets_zooma_to_efo_mappings()

        # self.icd9_to_efo = {}
        # payload={"ids":[],"inputSource":"ICD9CM","mappingTarget":["EFO"],"distance":"3"}
        # r = requests.post('https://www.ebi.ac.uk/spot/oxo/api/search?size=1000', data= payload)
        # oxomappings = r.json()['_embedded']['searchResults']
        #     while oxo.json().get('next') == True:
        # for row in oxomappings:
        #     self.icd9_to_efo[ row['curie'].split(':')[1] ] = row['mappingResponseList'][0]['curie']

        # self.zooma_to_efo_map = OrderedDict()
        self._omim_to_efo = get_omim_to_efo_mappings(URLS.OMIM_EFO_MAP)


    def omim_lookup(self, omimcode):
        return self._omim_to_efo[omimcode]
    
    def ols_lookup(self, name):
        return self._ols.besthit(name)

    def hp_lookup(self, name):
        return self.name_to_hp[name]
    
    def efo_lookup(self, name):
        return self.name_to_efo[name]

    def oxo_lookup(self, other_ontology_id):
        '''should return an EFO code for any given xref'''
        return None
