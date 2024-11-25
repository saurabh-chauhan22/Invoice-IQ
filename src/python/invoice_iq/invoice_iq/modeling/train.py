import logging

from pathlib import Path

from invoice_iq.config import MODELS_DIR, PROCESSED_DATA_DIR, NOTEBOOKS_DIR

import spacy
from spacy import load, blank
from spacy.tokens import DocBin
from spacy.cli.train import train

logger = logging.getLogger(__name__)

class SpacyModelTrain:
    '''
    Model creation class for custom large language en model
    '''
    def __init__(self, use_gpu=False) -> None:
        if use_gpu:
            spacy.prefer_gpu()
        self.nlp = None
        self.docbin = DocBin()
    
    def load_model(self, model):
        if model =='en':
            self.nlp = blank(model)
        elif model =='en_core_web_trf':
            self.nlp = load(model)
        else:
            logger.error("Model not valid")
        return self.nlp
    
    def create_docbin(self, input_data, data_type):
        '''
        Create spacy
        jsonl to json return json object
        '''
        entities = list()
        for text, annot in input_data:
            doc = self.nlp.make_doc(text)
            for start,end,label in annot["entities"]:
                if end>start:
                    span = doc.char_span(int(start),int(end),label=label, alignment_mode="strict")
                    if span is not None:
                        entities.append(span)
        doc.ents = entities
        self.docbin.add(doc)
        logger.debug("Doc bin created with text and annotations")
        binary_path = f".\\{data_type}.spacy"
        self.docbin.to_disk(binary_path)
        
    def save_to_disk(self,output_path):
        '''
        Save the DocBin object to disk
        '''
        with open(Path(output_path).absolute(), 'wb') as f:
            f.write(self.docbin.to_bytes())
        logger.debug(f"Model saved to path :{output_path}")
    
    
    def prepossed_data(self, labelled_data):
        '''
        Prepossed the data for spacy model to detect the entries
        '''
        
            
    def train_model_from_binaries(self, output_path):
        try:
            train(Path(f"{NOTEBOOKS_DIR}\\config.cfg").absolute(),output_path=output_path)
        except Exception as ex:
            logger.exception("Failed to train the model to the output path",ex)
        
if __name__ =='__main__':
    spacy_train = SpacyModelTrain(True)
    spacy_train.load_model('en_core_web_trf')