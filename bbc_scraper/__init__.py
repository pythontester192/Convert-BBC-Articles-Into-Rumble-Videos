from .app import NewsScraper
from .core import ScraperBBC
from .utils import *
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
