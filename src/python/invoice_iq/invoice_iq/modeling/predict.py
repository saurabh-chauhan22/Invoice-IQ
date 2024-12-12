from pathlib import Path

import typer
from loguru import logger

from spacy import load

from invoice_iq.config import TEMP_FILE_PATH

app = typer.Typer()

@app.command()
class InvoiceDetector:
    '''
    Detection of invoice data parameters
    '''
    def __init__(self, model_path):
        '''
        Initilize the constructor with the valid trained model path 
        '''
        assert Path(model_path).exists() is not None
        self.nlp = load(model_path)
        logger.info("Model loaded")

    def _text_analysis(self):
        '''
        Extracted text from the pdf and store it into 
        nlp doc object
        '''
        pdf_text = ""
        with open(TEMP_FILE_PATH,'r') as f:
            pdf_text = f.read()
        doc=self.nlp(pdf_text)
        return doc   
    
    def predict(self):
        '''
        Detect the variables from the invoice pdf from the model
        '''
        doc = self._text_analysis()
        for ent in doc.ents:
            logger.info(f"Label : {ent.label_}, text: {ent.text}")
            yield ent 
            
