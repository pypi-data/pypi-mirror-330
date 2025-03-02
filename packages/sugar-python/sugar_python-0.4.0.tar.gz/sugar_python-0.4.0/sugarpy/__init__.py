from .morphemes import *
from .sentences import *
from .metrics import get_metrics
from .norms import get_norms, is_within_norms
from .enum import MetricName

import importlib

__version__ = importlib.metadata.version("sugar-python")
