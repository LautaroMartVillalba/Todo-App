from enum import Enum
from pathlib import Path

class File(Enum):
    THIS_FOLDER = Path(__file__).resolve().parent
    CRAB_NEBULA_PDF = THIS_FOLDER / 'crab_nebula.pdf'
    HEIC_1311_A_JPG = THIS_FOLDER / 'Heic1311a.jpg'
    NGC_1514_PDF = THIS_FOLDER / 'NGC 1514.pdf'
    STARS_CSV = THIS_FOLDER / 'stars.csv'
    DEEP_SPACE_CSV = THIS_FOLDER / 'deep_space.csv'
    SOMBRERO_GALAXY_JPG = THIS_FOLDER / 'Sombrero-Galaxy.jpg'
