import time
from pathlib import Path

import typer

from loguru import logger

import spacy
from spacy import displacy

from invoice_iq.config import FIGURES_DIR, MODEL_ONE_PATH, TEMP_FILE_PATH

app = typer.Typer()


@app.command()
def main():
    input_path: Path = TEMP_FILE_PATH
    output_path: Path = FIGURES_DIR / "entities.xml"
    model_path: Path = MODEL_ONE_PATH
    # -----------------------------------------
    logger.info(f"Loading spaCy model from {model_path}...")
    nlp = spacy.load(model_path)
    pdf_text = ""
    with open(input_path,'r') as f:
        pdf_text = f.read()
    logger.info("Processing text with spaCy model...")
    doc = nlp(pdf_text)
    logger.info("Generating plot ....")
    time.sleep(2)
    logger.info("Generating entity visualization in XML format...")
    xml = displacy.render(doc, style="span")
    output_path.open("w",encoding="utf-8").write(xml)
    logger.success("Plot generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
