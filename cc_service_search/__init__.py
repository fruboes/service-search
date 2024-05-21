"""Top-level package for EuroCC Service Search."""

__author__ = """Tomasz Fruboes"""
__email__ = 'Tomasz.Fruboes@ncbj.gov.pl'
__version__ = '1.0.0'

from dotenv import load_dotenv
load_dotenv() 

from .db import *

