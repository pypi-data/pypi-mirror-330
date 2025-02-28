import click
import filelean
from filelean import __version__
from filelean.utils import working_directory, execute_lean_code
from filelean.constants import LEAN_CACHE_DIR, MATHLIB_URL
from typing import Optional
from loguru import logger
from .log_config import pass_info, Info, setup_logging
from .utils import get_github_object, get_repo_versions
from .install import (
    InstallationError,  
    install_mathlib, list_mathlib_cache
)


help_message = """
Lean REPL management CLI

A tool for managing Lean repositories.
"""

@click.group(help=help_message)
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """Lean4 management tool"""
    level = setup_logging(verbose)
    if verbose > 0:
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={level})",
                fg="yellow",
            )
        )
    info.verbose = verbose

## mathlib
@cli.group()
def mathlib():
    """Manage Lean mathlib installations"""
    pass

@mathlib.command(name='install')
@click.argument('version', required=False)
@click.option('-f', '--force', is_flag=True, help='Force reinstall if already exists')
@click.option('-d', '--dest-dir', type=click.Path(), help='Destination directory for installation')
@pass_info
def install_mathlib_version(info: Info, version: Optional[str], force: bool, dest_dir: Optional[str]):
    """Install mathlib"""
    try:
        # Validate version
        if version is None:
            version = filelean.constants.DEFAULT_LEAN4_VERSION
            logger.info(f"Using default version: {version}")
        
        # Check GitHub
        g = get_github_object()
        repo = g.get_repo("leanprover-community/mathlib4")
        if repo.get_git_ref(f"tags/{version}").ref is None:
            raise InstallationError(f"Unknown version: {version}")
        
        # Install mathlib
        install_path = install_mathlib(version, force, dest_dir)

        # Test installation
        logger.info('Testing command: import Mathlib\\n#eval s!"v{Lean.versionString}"')
        msg, err, code = execute_lean_code('import Mathlib\n#eval s!"v{Lean.versionString}"', working_dir=install_path)
        if code != 0:
            raise InstallationError(f"Installation failed: {err}")
        logger.info(f"Lean Version: {msg.strip()}")
        if err:
            logger.warning(f"Installation error: {err}")
        
        click.echo(
            click.style(
                f"Successfully installed mathlib {version} to {install_path}",
                fg="green"
            )
        )
        
    except InstallationError as e:
        logger.error(f"Installation failed: {e}")
        raise click.Abort() from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise click.Abort() from e

@mathlib.command(name='list')
@click.option('-n', '--max-num', type=int, default=10, help='Maximum number of versions to show')
@pass_info
def list_mathlib_versions(info: Info, max_num:int=10):
    """List available mathlib versions and their installation status"""
    try:
        available_versions = get_repo_versions(MATHLIB_URL, max_num=max_num)
        cached_versions = list_mathlib_cache()

        click.echo("Available mathlib versions(latest {}):".format(max_num))
        click.echo()

        for version in available_versions:
            if version in cached_versions:
                click.echo(
                    f"{version} " +
                    click.style("(installed)", fg="green")
                )
            else:
                click.echo(version)
        for version in cached_versions[::-1]:
            if version not in available_versions:
                click.echo(
                    f"{version} " +
                    click.style("(installed)", fg="green")
                )
    except Exception as e:
        click.echo(f"Failed to fetch versions: {e}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()