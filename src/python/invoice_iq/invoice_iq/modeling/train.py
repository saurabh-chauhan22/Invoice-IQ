import logging
import random
from pathlib import Path
import typer
from loguru import logger

from invoice_iq.config import NOTEBOOKS_DIR,REFERENCES_DIR
from invoice_iq.jsonl_to_json import jsonl_to_json
from invoice_iq.utilities import convert_data_to_spacy_format, cleaned_data

import spacy
from spacy import load
from spacy.tokens import DocBin
from spacy.cli.train import train as spacy_train
from spacy import util

app = typer.Typer()

@app.command()
class SpacyModelTrain:
    '''
    Model creation class for custom named entity recognition (NER) model
    '''
    def __init__(self, gpu=False) -> None:
        self.nlp = None
        self.docbin_train = DocBin()
        self.docbin_test = DocBin()
    
    def load_model(self, model='en_core_web_trf'):
        """
        Load a SpaCy model with error handling
        """
        logger.info(f"Using transformer model : {model}")
        try:
            self.nlp = load(model)
            logger.success("Spacy model loaded")
            return self.nlp
        except Exception as e:
            logger.error(f"Failed to load model {model}: {e}")
            raise
    
    def create_docbin(self, input_data, docbin, data_type):
        """
        Create SpaCy DocBin from annotated data
        """
        for text, annot in input_data:
            doc = self.nlp.make_doc(text)
            entities = list()
            
            for annotation_dict in annot.get("entities", []):
                start = int(annotation_dict.get('start_offset', 0))
                end = int(annotation_dict.get('end_offset', len(text)))
                label = annotation_dict.get('label', '')
                
                if end > start:
                    span = doc.char_span(start, end, label=label)
                    if span is not None:
                        entities.append(span)
            
            non_overlapping_entities = self.filter_overlapping_spans(entities)
            doc.ents = non_overlapping_entities
            docbin.add(doc)
        
        binary_path = Path(f"{data_type}.spacy")
        docbin.to_disk(binary_path)
        logger.debug(f"{data_type.capitalize()} DocBin created")

    def filter_overlapping_spans(self, spans):
        """
        Filter overlapping spans, keeping the longer span
        """
        sorted_spans = sorted(spans, key=lambda span: (span.start, -span.end))
        non_overlapping = []

        for span in sorted_spans:
            if not non_overlapping or span.start >= non_overlapping[-1].end:
                non_overlapping.append(span)

        return non_overlapping
    
    def save_to_disk(self, output_path):
        """
        Save DocBin to disk
        
        :param output_path: Path to save the DocBin
        """
        with open(Path(output_path).absolute(), 'wb') as f:
            f.write(self.docbin_train.to_bytes())
        logger.debug(f"Model saved to path: {output_path}")
    
    def preprocess_data(self, labelled_data):
        """
        Preprocess data for SpaCy model training
        
        :param labelled_data: Path to labelled data file
        :return: Training and testing data splits
        """
        json_obj = jsonl_to_json(labelled_data)
        data = convert_data_to_spacy_format(json_obj)
        processed_data = cleaned_data(data)
        
        random.shuffle(processed_data)
        training_data_len = int(len(processed_data) * 0.8)
        
        training_data = processed_data[:training_data_len]
        testing_data = processed_data[training_data_len:]
        
        return training_data, testing_data
        
    def create_spacy_binaries(self, labelled_data):
        """
        Create SpaCy binaries for training and testing
        
        :param labelled_data: Path to labelled data file
        """
        train_data, test_data = self.preprocess_data(labelled_data)
        self.create_docbin(train_data, self.docbin_train, data_type="train")
        self.create_docbin(test_data, self.docbin_test, data_type="test")
            
    def train_model(self, output_path):
        """
        Train SpaCy model from binaries
        
        :param output_path: Path to save trained model
        """
        try:
            config_path = Path(f"{REFERENCES_DIR}\\config.cfg").absolute()
            spacy_train(config_path, output_path=output_path)
        except Exception as ex:
            logger.exception(f"Failed to train model: {ex}")
            raise
        
def main():
    spacy_train = SpacyModelTrain(gpu=False)
    # spacy.prefer_gpu()
    try:
        spacy_train.load_model("en_core_web_trf")
        labelled_data = f"{NOTEBOOKS_DIR}\\labelled_data.jsonl"
        spacy_train.create_spacy_binaries(labelled_data)
        spacy_train.train_model('model_output')
    except Exception as ex:
        logger.exception(f"Could not create SpaCy model: {ex}")
    
if __name__ == '__main__':
    main()