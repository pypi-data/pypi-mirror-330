"""Top-level package for filelean."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '0.1.0'

from pathlib import Path
import click
import os
from .proof import FileLean, FileState, TacticFailure, LeanOutput, TacticFailure, LeanError
from .utils import execute_lean_code
from .cli import read_mathlib_cache