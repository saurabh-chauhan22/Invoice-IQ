from pathlib import Path

import typer
from loguru import logger
from jinja2 import Environment, PackageLoader, select_autoescape

app = typer.Typer()


@app.command()
def main():
    env = Environment(
    loader=PackageLoader("invoice_iq"),
    autoescape=select_autoescape()
)
    
    logger.success("Features generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
