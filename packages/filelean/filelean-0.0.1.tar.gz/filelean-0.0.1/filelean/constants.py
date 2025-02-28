import os
from pathlib import Path
import platformdirs

DEFAULT_LEAN4_VERSION = os.getenv("DEFAULT_LEAN4_VERSION", "v4.14.0")
"""Default version"""

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN", None)

TMP_DIR = os.getenv("TMP_DIR", None)
"""Tempeorary working directory"""

MATHLIB_URL = "https://github.com/leanprover-community/mathlib4"

# cache dirs
LEAN_CACHE_DIR = Path(os.getenv('LEAN_CACHE_DIR', platformdirs.user_cache_dir("filelean")))
"""Cache directory for repositories"""

REPO_ABSLOUTE_PATH = Path(__file__).absolute().parent.parent

