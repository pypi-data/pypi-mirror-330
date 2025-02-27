import warnings


def showwarning(message, category, filename, lineno, file=None, line=None):
    print(f"{category.__name__}: {message}", file=file)


warnings.showwarning = showwarning

from .main_client import SwitchAI
from .superclients import Browser, ImageRetriever, Classifier, Illustrator
