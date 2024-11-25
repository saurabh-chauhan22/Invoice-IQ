import logging
import random

from pathlib import Path

from invoice_iq.config import NOTEBOOKS_DIR
from invoice_iq.jsonl_to_json import jsonl_to_json
from invoice_iq.utilities import convert_data_to_spacy_format, cleaned_data
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
            for index, annotation_dict in enumerate(annot["entities"]):
                for annot in annotation_dict.keys():
                    start = annotation_dict.get('start_offset')
                    end = annotation_dict.get('end_offset')
                    label = annotation_dict.get('label') 
                    if end >= start:
                        span = doc.char_span(int(start),int(end),label=label)
                    if span is not None:
                        entities.append(span)
        non_overlapping_entities = self.filter_overlapping_spans(entities)
        doc.ents = non_overlapping_entities
        self.docbin.add(doc)
        logger.debug("Doc bin created with text and annotations")
        binary_path = f".\\{data_type}.spacy"
        self.docbin.to_disk(binary_path)

    def filter_overlapping_spans(self,spans):
        """
        Filters overlapping spans and returns a list of non-overlapping spans.
        Keeps the longer span in case of overlap.

        :param spans: List of SpaCy Span objects.
        :return: List of non-overlapping Span objects.
        """
        sorted_spans = sorted(spans, key=lambda span: (span.start, -span.end))  # Sort by start, then by longest first
        non_overlapping = []

        for span in sorted_spans:
            if not non_overlapping or span.start >= non_overlapping[-1].end:
                non_overlapping.append(span)  # Add span if it doesn't overlap with the last one

        return non_overlapping
    
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
        json_obj = jsonl_to_json(labelled_data)
        data = convert_data_to_spacy_format(json_obj)
        processed_data = cleaned_data(data)
        random.shuffle(processed_data)
        training_data_len = int(len(json_obj) *0.8)
        training_data = processed_data[:training_data_len]
        testing_data = processed_data[training_data_len+1:]
        return training_data,testing_data
        
    def create_spacy_binaries(self, labelled_data):
        '''
        Create the large nlp model spacy binaries for training
        '''
        train_data, test_data = self.prepossed_data(labelled_data)
        self.create_docbin(train_data,data_type="train")
        self.create_docbin(test_data,data_type="test")
            
    def train_model_from_binaries(self, output_path):
        try:
            train(Path(f"{NOTEBOOKS_DIR}\\config.cfg").absolute(),output_path=output_path)
        except Exception as ex:
            logger.exception("Failed to train the model to the output path",ex)
        
if __name__ =='__main__':
    spacy_train = SpacyModelTrain(False)
    try:
        spacy_train.load_model('en_core_web_trf')
        labelled_data = f"{NOTEBOOKS_DIR}\\labeled_data.jsonl"
        spacy_train.create_spacy_binaries(labelled_data)
        spacy_train.train_model_from_binaries('model_output')
    except Exception as ex:
        logger.exception(f"Could not create spacy model for labelled data",ex)
    finally:
        exit(0)
        