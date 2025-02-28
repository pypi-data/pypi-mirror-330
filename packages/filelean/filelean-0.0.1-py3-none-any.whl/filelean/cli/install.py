from filelean.utils import working_directory, execute_command, execute_popen_command
from filelean.constants import LEAN_CACHE_DIR, MATHLIB_URL, REPO_ABSLOUTE_PATH
from .utils import get_github_object
import toml, subprocess, shutil, re
from pathlib import Path
from typing import Tuple, Optional, List
from loguru import logger
from git import Repo, BadName

class InstallationError(Exception):
    pass

def check_cmd(cmd: str) -> bool:
    """Check if command exists"""
    return shutil.which(cmd) is not None

def install_lean():
    if all(check_cmd(cmd) for cmd in ['lean', 'lake', 'elan']):
        logger.info("Lean already installed")
        return
    logger.info("Installing Lean...")
    _, _, code = execute_command(['bash', 'install_lean.sh'], cwd=REPO_ABSLOUTE_PATH / 'scripts')
    return code == 0

def list_mathlib_cache() -> List[str]:
    """
    Get the list of cached Lean versions.

    Returns:
        List[str]: The list of cached Lean versions.

    Example:
        >>> list_mathlib_cache()
        ['v4.7.0', 'v4.8.0', 'v4.10.0']
    """
    cache_dir = Path(LEAN_CACHE_DIR)
    if not cache_dir.exists():
        return []
    
    # search for mathlib-v* directories
    version_pattern = re.compile(r'mathlib-(v.*)')
    versions = []
    for path in cache_dir.iterdir():
        if path.is_dir():
            match = version_pattern.match(path.name)
            if match:
                versions.append(match.group(1))
    return sorted(versions)

def read_mathlib_cache(version: str) -> Optional[Path]:
    """
    Read the Mathlib cache for a given version.

    Args:
        version: The version of Mathlib to read

    Returns:
        Path: The path to the Mathlib cache directory. None if not found.
    """
    cache_dir = Path(LEAN_CACHE_DIR)
    mathlib_dir = cache_dir / f"mathlib-{version}"
    if mathlib_dir.exists():
        return mathlib_dir
    return None

def install_mathlib(version: str, force: bool = False, dest_dir: Optional[str] = None) -> Path:
    """
    Download and build Lean 4 Mathlib.
    
    Args:
        version: Lean version (e.g. 'v4.10.0')
        force: If True, overwrite existing installation
        dest_dir: Custom installation directory
        
    Returns:
        Path: Installation directory path
        
    Raises:
        InstallationError: If installation fails
    """
    
    # Setup paths
    dest_dir = dest_dir and Path(dest_dir).resolve()
    if dest_dir is not None and not force and dest_dir.exists():
        logger.info(f"Destination directory {dest_dir} already exists")
        return dest_dir

    # Check cache
    cache_dir = Path(LEAN_CACHE_DIR)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"mathlib-{version}"
    
    if cache_path.exists() and not force:
        logger.info(f"Version {version} already installed at {cache_path}")
        if dest_dir is not None:
            _, err, code = execute_command(["cp", "-r", cache_path, dest_dir])
            if code != 0:
                raise InstallationError(f"Failed to copy installation to destination directory: {err}")
            return dest_dir
        return cache_path
    
    # Check GitHub
    g = get_github_object()
    repo = g.get_repo("leanprover-community/mathlib4")
    if repo.get_git_ref(f"tags/{version}").ref is None:
        raise InstallationError(f"Unknown version: {version}")

    work_dir = dest_dir and dest_dir.parent
    with working_directory(work_dir, chdir=True) as work_dir:
        if dest_dir is None:
            repo_path = Path(work_dir) / f"mathlib-{version}"
            logger.debug(f"Working in temporary directory: {work_dir}")
        else:
            repo_path = dest_dir
            logger.debug(f"Working in directory: {work_dir}")
            if repo_path.exists(): # remove existing directory
                shutil.rmtree(repo_path)

        # Create new project
        logger.info(f"Cloning repository: {repo.clone_url}")
        repo = Repo.clone_from(repo.clone_url, repo_path)
        try:
            repo.git.checkout(version)
        except BadName:
            raise InstallationError(f"Invalid version: {version}")

        # NOTE: Update dependencies and build, this will change the lean-toolchain
        # logger.info("Updating dependencies...")
        # _, err, code = execute_command(['lake', 'update', '-R'], cwd=repo_path, capture_output=False)
        # if code != 0:
        #     raise InstallationError(f"Failed to update dependencies: {err}")

        logger.info("Getting mathlib cache...")
        _, err, code = execute_command(['lake', 'exe', 'cache', 'get'], cwd=repo_path, capture_output=False)
        if code != 0:
            raise InstallationError(f"Failed to get cache: {err}")

        logger.info("Building project...")
        _, err, code = execute_command(['lake', 'build'], cwd=repo_path, capture_output=False)
        if code != 0:
            raise InstallationError(f"Failed to build project: {err}")

        # Save to cache
        if cache_path.exists():
            shutil.rmtree(cache_path)
        logger.debug(f"Saving installation to cache: {cache_path}")
        _, err, code = execute_command(["cp", "-r", repo_path, cache_path])
        if code != 0:
            raise InstallationError(f"Failed to save installation to cache: {err}")
    if dest_dir is None:
        repo_path = cache_path # return the cache path
    logger.info(f"Setup completed successfully in {repo_path}")
    return repo_path
