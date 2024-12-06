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
    json_data = json.loads(labelled_json_obj)
    entities = list()
    for json_obj in json_data:
        doc_id = json_obj.get('id','')
        text = json_obj.get('text', '')
        entities = json_obj.get('entities', list())
            
        if not entities:
            logger.warning(f"No entities found for text: {text}")
            continue
        unique_entities = list()
        seen_entities = set()
        for entity in entities:
                entity_key = (entity.get('start_offset'), entity.get('end_offset'), entity.get('label'))
                if entity_key not in seen_entities:
                    unique_entities.append(entity)
                    seen_entities.add(entity_key)
        
        if unique_entities:
            labelled_data.append(
                (text,{
                    "entities":unique_entities,
                    "id":doc_id
                })
            )
        
    return labelled_data


def cleaned_data(data:list)->list:
    '''
    Return the cleaned data which will remove entities with leading spaces 
    and trailing blank along with empty entities
    '''
    cleaned_data = list()
    for text,annotations in data:
        entities = annotations.get('entities', list())
        doc_id = annotations.get('id','')
        if entities:
            cleaned_entry = {
                'entities': entities
            }
            cleaned_data.append((text,cleaned_entry))
            # valid_entites = validate_span_token(text,cleaned_entry)
        else:
            logger.warning(f"No valid entities found in text: {text}")
    return cleaned_data
            
            
def validate_span_token(text:str,entities:list)->list:
    '''
    removes leading spaces and validate the spacy span tokens
    '''
    valid_entities = list()
    for entity in entities['entities']:
        try:
            start = entity.get('start_offset', 0)
            end = entity.get('end_offset', len(text))
            label = entity.get('label', '')
            
            if start < 0 or end > len(text) or start >= end:
                logger.warning(f"Invalid span: {start}-{end} for text length {len(text)}")
                continue
            
            while end > start and text[end-1].isspace():
                end -= 1
            
            if start < end:
                entity_text = text[start:end].strip()
                
                if entity_text:
                    valid_entities.append([start, end, label])
                else:
                    logger.warning(f"Empty entity span: {start}-{end}")
        
        except Exception as e:
            logger.error(f"Error validating entity: {e}")
    
    return valid_entities


            
        

    