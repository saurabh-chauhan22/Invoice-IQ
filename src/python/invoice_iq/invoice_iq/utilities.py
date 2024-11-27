import logging
import re

import json

logger = logging.getLogger(__name__)

def convert_data_to_spacy_format(labelled_json_obj)->list:
    '''
    Convert the data to spacy recommonded format
    Returns a list of data
    '''
    labelled_data = list()
    for json_obj in json.loads(labelled_json_obj):
        entities = list()
        for entity in json_obj['entities']:
            entities.append(entity)
            #adding training example for (text, annotations) tuple
            labelled_data.append((json_obj['text'],{"entities":entities}))
    return labelled_data


def cleaned_data(data:list)->list:
    '''
    Return the cleaned data which will remove entities with leading spaces 
    and trailing blank along with empty entities
    '''
    cleaned_data= list()
    for text,annotations in data:
        entities = annotations['entities']
        if len(entities)>0:
            # valid_entites = list()
            # valid_entites = validate_span_token(text=text,entities=entities)
            cleaned_data.append([text,{'entities':entities}])
        else:
            logger.error("Entities not valid less entries")
    return cleaned_data
            
            
def validate_span_token(text:str,entities:list)->list:
    '''
    removes leading spaces and validate the spacy span tokens
    '''
    invalid_span_tokens = re.compile(r'\s')
    valid_entities = list()
    for entity in entities:
        start = entity.get('start_offset')
        end = entity.get('end_offset')
        label = entity.get('label')
        valid_start = start
        valid_end = end
        while valid_start <len(text) and invalid_span_tokens.match(text[valid_end-1]):
            valid_end -=1
        valid_entities.append([valid_start,valid_end,label])
    return valid_entities


            
        

    