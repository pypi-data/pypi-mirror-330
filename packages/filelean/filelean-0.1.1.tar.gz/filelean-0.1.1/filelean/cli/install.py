from filelean.utils import working_directory, execute_command, execute_popen_command
from filelean import constants
from .utils import get_github_object, github_url_to_repo_name
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

script = """
#!/bin/bash

check_cmd() {
    command -v "$1" > /dev/null 2>&1
}

if ! check_cmd elan || ! check_cmd lean || ! check_cmd lake; then
    curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | bash -s -- -y --default-toolchain none
    source ~/.profile # source ~/.bashrc
fi
"""

def install_lean():
    if all(check_cmd(cmd) for cmd in ['lean', 'lake', 'elan']):
        logger.info("Lean already installed")
        return True
    logger.info("Installing Lean...")
    with working_directory() as tmp_dir:
        temp_sh = Path(tmp_dir) / 'install_lean.sh'
        temp_sh.write_text(script)
        _, _, code = execute_command(['bash', 'install_lean.sh'], cwd=tmp_dir)
    if code == 0:
        logger.info("Lean installed successfully")
        return True
    return False

def list_repo_cache(prefix:str) -> List[str]:
    """
    Get the list of cached Lean versions.

    Returns:
        List[str]: The list of cached Lean versions.

    Example:
        >>> list_repo_cache()
        ['v4.7.0', 'v4.8.0', 'v4.10.0']
    """
    cache_dir = Path(constants.LEAN_CACHE_DIR)
    if not cache_dir.exists():
        return []
    
    # search for prefix-v* directories
    version_pattern = re.compile(f'{prefix}-(v.*)')
    versions = []
    for path in cache_dir.iterdir():
        if path.is_dir():
            match = version_pattern.match(path.name)
            if match:
                versions.append(match.group(1))
    return sorted(versions)

def read_repo_cache(repo:str, version: str) -> Optional[Path]:
    """
    Read the repo cache for a given version.

    Args:
        version: The version of repo to read

    Returns:
        Path: The path to the repo cache directory. None if not found.
    """
    cache_dir = Path(constants.LEAN_CACHE_DIR)
    repo_dir = cache_dir / f"{repo}-{version}"
    if repo_dir.exists():
        return repo_dir.resolve()
    return None

def read_mathlib_cache(version: str) -> Optional[Path]:
    """
    Read the Mathlib cache for a given version.

    Args:
        version: The version of Mathlib to read
    """
    return read_repo_cache("mathlib4", version)

def install_github_repo(url:str, version: str,
                        prefix:str=None,
                        force: bool = False, 
                        dest_dir: Optional[str] = None,
                        lake_update:bool=False) -> Path:
    """
    Download and build Lean 4 Repo.
    
    Args:
        url: GitHub repository URL
        version: Lean version (e.g. 'v4.10.0')
        prefix: Prefix for the installation directory, default is the repository name
        force: If True, overwrite existing installation
        dest_dir: Custom installation directory
        lake_update: If True, update dependencies, default is False
        
    Returns:
        Path: Installation directory path
        
    Raises:
        InstallationError: If installation fails
    """

    if not all(check_cmd(cmd) for cmd in ['lean', 'lake', 'elan']):
        install_lean()
    
    # Setup paths
    dest_dir = dest_dir and Path(dest_dir).resolve()
    if dest_dir is not None and not force and dest_dir.exists():
        logger.info(f"Destination directory {dest_dir} already exists")
        return dest_dir

    # Check cache
    repo_name = github_url_to_repo_name(url)
    prefix = repo_name.split('/')[1] if prefix is None else prefix
    logger.debug(f'{repo_name}, {prefix}')
    cache_dir = Path(constants.LEAN_CACHE_DIR)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{prefix}-{version}"
    
    if cache_path.exists() and not force:
        logger.info(f"Version {version} already installed at {cache_path}")
        if dest_dir is not None:
            _, err, code = execute_command(["cp", "-r", cache_path, dest_dir])
            if code != 0:
                raise InstallationError(f"Failed to copy installation to destination directory: {err}")
            return dest_dir
        return cache_path
    
    # Check GitHub | this could result in a rate limit error
    # g = get_github_object()
    # repo = g.get_repo(repo_name)
    # if repo.get_git_ref(f"tags/{version}").ref is None:
    #     raise InstallationError(f"Unknown version: {version}")

    work_dir = dest_dir and dest_dir.parent
    with working_directory(work_dir, chdir=True) as work_dir:
        if dest_dir is None:
            repo_path = Path(work_dir) / f"{prefix}-{version}"
            logger.debug(f"Working in temporary directory: {work_dir}")
        else:
            repo_path = dest_dir
            logger.debug(f"Working in directory: {work_dir}")
            if repo_path.exists(): # remove existing directory
                shutil.rmtree(repo_path)

        # Create new project
        try:
            logger.info(f"Cloning repository: {url}")
            Repo.clone_from(url, repo_path, branch=version)
        except BadName:
            raise InstallationError(f"Invalid version: {version}")

        # NOTE: This will change the lean-toolchain for mathlib
        if lake_update:
            logger.info("Updating dependencies...")
            _, err, code = execute_command(['lake', 'update', '-R'], cwd=repo_path, capture_output=False)
            if code != 0:
                raise InstallationError(f"Failed to update dependencies: {err}")

        logger.info(f"Getting {prefix} cache...")
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
        _, err, code = execute_command(["mv", repo_path, cache_path])
        if code != 0:
            raise InstallationError(f"Failed to save installation to cache: {err}")
    if dest_dir is None:
        repo_path = cache_path # return the cache path
    logger.info(f"Setup completed successfully in {repo_path}")
    return repo_path

def install_mathlib(version: str, force: bool = False, dest_dir: Optional[str] = None) -> Path:
    """
    Install Lean 4 Mathlib.
    
    Args:
        version: Lean version (e.g. 'v4.10.0')
        force: If True, overwrite existing installation
        dest_dir: Custom installation directory
    """
    return install_github_repo(constants.MATHLIB_URL,
                               version, force=force, dest_dir=dest_dir, lake_update=False)