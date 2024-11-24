from pathlib import Path

from invoice_iq.config import MODELS_DIR, PROCESSED_DATA_DIR

from spacy import load, blank

class SpacyModel:
    '''
    Model creation class for custom large language en model
    '''
    def __init__(self) -> None:
        '''
        '''
        pass
    
    def load_model(self, model):
        nlp = None
        if model =='en':
            nlp = blank(model)
        else:
            nlp = load(model)
        return nlp
    
    def save_to_disk(self):
        '''
        Create spacy
        jsonl to json return json object
         
        '''
    
    def train(self):
        '''
        '''
        pass
    
    def prepossed_data(self, labelled_data):
        '''
        Prepossed the data for spacy model to detect the entries
        '''
        pass