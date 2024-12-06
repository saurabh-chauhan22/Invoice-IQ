from pathlib import Path

from loguru import logger

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

TEMP_FILE_PATH = PROJ_ROOT / "notebooks" / "temp.text"

MODELS_DIR = PROJ_ROOT / "models" 

MODEL_ONE_PATH = MODELS_DIR / "model1" / "model-best"
MODEL_TWO_PATH = MODELS_DIR / "model2" / "model-best"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
NOTEBOOKS_DIR = PROJ_ROOT / "notebooks"
REFERENCES_DIR = PROJ_ROOT / "references"


try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
