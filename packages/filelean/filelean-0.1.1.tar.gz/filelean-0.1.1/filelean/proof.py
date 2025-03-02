
from dataclasses import dataclass
from typing import List, Tuple, Union, Any, Dict, Optional
from loguru import logger
from pathlib import Path
from filelean.constants import LEAN_CACHE_DIR, DEFAULT_LEAN4_VERSION
from filelean.utils import execute_command, execute_lean_code, text_slice
from filelean.cli import read_mathlib_cache
import json
import re


valid_errors = [
    "unexpected end of input; expected '{'"
]

@dataclass
class LeanOutput:
    raw: str
    info: Dict[str, Any]
    warning: str = ""
    error: str = ""
    lean_error :str = ""
    infos: List[str] = None
    errors: List[str] = None
    warnings: List[str] = None

    def __init__(self, msg:str, err:str):
        self.info = {'message': err}
        lines = [json.loads(line.strip()) for line in msg.split('\n') if line.strip()]
        for line in lines:
            line.pop('fileName')
        self.info['messages'] = lines
        self.raw = json.dumps(self.info, ensure_ascii=False)
        # parse infos
        warnings, errors, infos = [], [], []
        for msg in self.info.get('messages'):
            if msg.get('severity') == 'warning':
                warnings.append(msg)
            elif msg.get('severity') == 'error':
                errors.append(msg)
            elif msg.get('severity') == 'information':
                infos.append(msg)
        self.warnings = warnings
        self.errors = errors
        self.infos = infos
        self.warning = '\n'.join(msg.get('data') for msg in warnings)
        self.error = '\n'.join(msg.get('data') for msg in errors)
        self.lean_error = err

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.raw

class TacticFailure(Exception):
    """
    Indicates a tactic failed to execute
    """

class LeanError(Exception):
    """
    Indicates a Lean error
    """

class FileState():
    goals: List[str]
    code_before:str
    pos: Tuple[int, int]

    def __init__(self, goals:List[str], code_before:str, pos:Tuple[int, int]):
        self.goals = goals
        self.code_before = code_before
        self.pos = pos
        if not self.goals:
            self.pp = "No goals"
        else:
            self.pp = "\n\n".join(str(goal) for goal in self.goals)

    @classmethod
    def from_lean_output(cls,
                         output:LeanOutput,
                         code_before:str) -> List['FileState']:
        if output.lean_error:
            raise LeanError(output.lean_error)
        states = []
        for err in output.errors:
            msg, pos, end_pos = err.get('data'), err.get('pos'), err.get('endPos')
            if msg in valid_errors:
                pass
            elif msg.startswith('unsolved goals'):
                text = text_slice(code_before, {"line":1, "column":0}, end_pos)
                goals = msg.split('unsolved goals')[1].strip()
                goals = goals.split('\n\n') if goals else []
                states.append(cls(goals, text, pos))
            else:
                raise TacticFailure(msg)
        return states
    
    def __str__(self):
        return self.pp
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, state:'FileState'):
        return self.goals == state.goals
    @property
    def is_solved(self):
        return len(self.goals) == 0


class FileLean():
    def __init__(self,
                 cwd: Optional[Path] = None,
                 timeout: int = 600):
        # initialize
        cwd = cwd or read_mathlib_cache(DEFAULT_LEAN4_VERSION)
        self.cwd = cwd or Path().cwd()
        self.timeout = timeout
        self.version = self.lean_version()
        self._last_output = None
    
    @property
    def last_output(self):
        return self._last_output
    
    def lean_version(self):
        # Lean (version 4.16.0-rc2, x86_64-unknown-linux-gnu, commit 128a1e6b0a82, Release)
        LEAN_REGX = r"Lean \(version (.*?),.*\)"
        try:
            msg, err, code = execute_command(['lean', '--version'], cwd=self.cwd)
            if code != 0:
                logger.error(f"Failed to get lean version: {err}")
                return ""
            ver = re.search(LEAN_REGX, msg).group(1)
            return f"v{ver}"
        except Exception as e:
            logger.error(f"Error getting lean version: {e}")
            return ""

    def run_tac(self, state:FileState, tactic:str, allow_sorries:bool=True) -> FileState:
        if state.is_solved:
            raise LeanError("No goals to be solved.")
        code_before = f"{state.code_before}\n{tactic.rstrip()}"
        new_state = self.from_proof(code_before, allow_sorries=allow_sorries)
        if new_state.is_solved:
            return new_state
        if new_state.pos != state.pos:
            raise TacticFailure(f"unsolved goals\n{new_state}")
        return new_state
    
    def init_state(self, theorem:str, header:str=None) -> FileState:
        """Initial state for theorem
        
        Example:
            >>> fl = FileLean()
            >>> fl.init_state('theorem foo (a b : Nat) : a + b = b + a')"""
        code_before = f"{theorem} := by"
        return self.from_proof(code_before, header=header)
    
    def from_proof(self, proof:str, allow_sorries:bool=True, header:str=None) -> FileState:
        """Get proof state from proof"""
        if header:
            proof = f"{header}\n{proof}"
        output = self.run_command(proof)
        if not allow_sorries:
            if "declaration uses 'sorry'" in output.warning:
                raise TacticFailure("declaration uses 'sorry'")
        states = FileState.from_lean_output(output, proof)
        if len(states) == 0:
            states = [FileState([], proof, {"line":1, "column":0})]
        if not len(states) == 1:
            raise TacticFailure(f"Expected 1 state, got {len(states)}")
        return states[0]
    
    def states_from_sketch(self, sketch:str)-> List[FileState]:
        """Get proof states from sketch"""
        output = self.run_command(sketch.replace('sorry', '-- sorry'))
        return FileState.from_lean_output(output, sketch)

    def run_command(self, command:str) -> LeanOutput:
        """Run lean command"""
        msg, err, _ = execute_lean_code(command, cwd=self.cwd, timeout=self.timeout)
        output = LeanOutput(msg, err)
        self._last_output = output
        return output
    
    def check(self):
        """Check if the workspace is valid"""
        self.run_command("#eval Lean.versionString")