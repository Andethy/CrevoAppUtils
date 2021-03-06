from typing import Tuple, List, Union

from src.application.gui import *
from src.application.gui import LabelCustom

DEFAULT_LOGO: str = 'resources/logo.png'
DEFAULT_DPI: float = 0.14
DEFAULT_DIMENSIONS: tuple[int, int] = (500, 500)
DEFAULT_DIMENSIONS_LOCK: bool = True
DEFAULT_TITLE: str = 'Crevolution Placeholder App'
DEFAULT_BACKGROUND: str = 'black'
DEFAULT_SCREEN: list[str, dict[str, list[str, list[WidgetCustom, float, float]]]] = ['Test',
                                                                                     dict(placeholder=[
                                                                                         LabelCustom('Test'),
                                                                                         0.5,
                                                                                         0.25])]

# Edit this in correspondence with the fields for the export location
FIELD_KEYS: tuple = ('Team #',
                     'Match #',
                     'U-A[+]',
                     'U-A[X]',
                     'L-A[+]',
                     'L-A[X]',
                     'TMC',
                     'HP Shot',
                     'Taxi',
                     'Ground',
                     'HP',
                     'U-T[+]',
                     'U-T[X]',
                     'L-T[+]',
                     'L-T[X]',
                     'Climb',
                     'Climb Time',
                     'Comments')

FIELD_COUNT: int = len(FIELD_KEYS)
