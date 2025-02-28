import os
import resource
import subprocess
from typing import Optional, Tuple, Generator, Union
from loguru import logger
from filelean import constants
from contextlib import contextmanager
from pathlib import Path
from filelean import constants
import tempfile
import time, signal

def execute_command(command: list, 
        cwd: Optional[str] = None,
        text: bool = True,
        input: Union[str, None]=None,
        capture_output:bool=True) -> Tuple[str, str, int]:
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=text,
            check=True,
            cwd=cwd,
            input=input
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        logger.warning(f"Failed to execute command: {e}")
        return "", str(e), -1


@contextmanager
def working_directory(
    path: Optional[Union[str, Path]] = None,
    chdir: bool = False,
) -> Generator[Path, None, None]:
    """Context manager setting the current working directory (CWD) to ``path`` (or a temporary directory if ``path`` is None).

    The original CWD is restored after the context manager exits.

    Args:
        path (Optional[Union[str, Path]], optional): The desired CWD. Defaults to None.
        chdir (bool, optional): Whether to change the CWD. Defaults to False.

    Yields:
        Generator[Path, None, None]: A ``Path`` object representing the CWD.
    """
    origin = Path.cwd()
    if path is None: # use temporary directory if path is None
        tmp_dir = tempfile.TemporaryDirectory(dir=constants.TMP_DIR)
        path = tmp_dir.__enter__()
        is_temporary = True
    else:
        is_temporary = False

    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
    if chdir:
        os.chdir(path)

    try:
        yield path
    finally:
        if chdir:
            os.chdir(origin)
        if is_temporary:
            tmp_dir.__exit__(None, None, None)

def execute_popen_command(command: list,
        cwd: Optional[str] = None, 
        text: bool = True,
        input: Union[str, None] = None,
        capture_output: bool = True,
        timeout: Optional[int] = None,
        max_memory_GB: Optional[float] = None) -> Tuple[str, str, int]:
    try:
        stdout_pipe = subprocess.PIPE if capture_output else None
        stderr_pipe = subprocess.PIPE if capture_output else None
        
        def set_limits():
            if max_memory_GB is not None:
                max_memory_bytes = int(max_memory_GB * 1024 * 1024 * 1024)
                resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))
            os.setsid() # make the process a new process group leader
        # create the process
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=stdout_pipe,
            stderr=stderr_pipe,
            text=text,
            preexec_fn=set_limits
        )
        start_time = time.time()
        if timeout is not None:
            while True:
                if process.poll() is not None:
                    break
                if time.time() - start_time > timeout:
                    # terminate the process
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait()
                    raise TimeoutError("Timeout exceeded, process terminated.")
                time.sleep(0.1)
        # wait for the process to finish
        stdout, stderr = process.communicate(input=input)
        returncode = process.returncode
        return stdout or "", stderr or "", returncode
    except Exception as e:
        logger.warning(f"命令执行失败: {e}")
        return "", str(e), -1

def execute_lean_code(text: str,
                     working_dir: Optional[str] = None,
                     max_memory_GB: Optional[float] = None,
                     timeout: Optional[int] = None):
    working_dir = working_dir or Path.cwd()
    if working_dir is None:
        raise ValueError("No mathlib installation found")
    with working_directory() as tmpdir:
        lean_file = tmpdir / "temp_code.lean"
        lean_file.write_text(text)
        msg, err, code = execute_popen_command(
            ["lake", "env", 'lean', lean_file],
            capture_output=True, text=True,
            cwd=working_dir, max_memory_GB=max_memory_GB, timeout=timeout)
        # strip the tmpdir of the output
        msg = msg.replace(str(tmpdir) + '/', "")
        err = err.replace(str(tmpdir) + '/', "")
    return msg, err, code
   