"""
PlainQAFact: A framework for evaluating plain language summaries using question answering.
"""

__version__ = '0.2.0'

from .plainqafact import PlainQAFact
from .classifier import Classifier
from .default_config import DefaultConfig

__all__ = ['PlainQAFact', 'Classifier', 'DefaultConfig'] 