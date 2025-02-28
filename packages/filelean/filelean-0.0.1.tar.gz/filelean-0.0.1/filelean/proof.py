
from dataclasses import dataclass
from typing import List, Tuple, Union, Any, Dict, Optional
from loguru import logger
from pathlib import Path
from filelean.constants import LEAN_CACHE_DIR, DEFAULT_LEAN4_VERSION
from filelean.utils import execute_command, execute_lean_code
from filelean.cli import read_mathlib_cache
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

    def __init__(self, raw:str):
        self.raw = raw

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

    def __init__(self, goals:List[str], code_before:str):
        self.goals = goals
        self.code_before = code_before
        if not self.goals:
            self.pp = "No goals"
        else:
            self.pp = "\n\n".join(str(goal) for goal in self.goals)

    @classmethod
    def from_lean_output(cls,
                         output:LeanOutput,
                         code_before:str) -> List['FileState']:
        """通过 REPL 输出的 sorries 字段构造 ProofState"""
        if output.lean_error:
            raise LeanError(output.lean_error)
        text = TextSlice(code_before)
        states = []
        for err in output.errors:
            msg = err.get('data')
            start_pos, end_pos = err.get('pos'), err.get('endPos')
            err['text'] = text[start_pos, end_pos]
            if msg in valid_errors:
                pass
            elif msg.startswith('unsolved goals'):
                goals = msg.split('unsolved goals')[1].strip()
                goals = goals.split('\n\n') if goals else []
                states.append(cls(goals, text[:, end_pos], TextSlice(code_before, start_pos, end_pos)))
            elif raise_for_error:
                raise TacticFailure(msg)
        # TODO: run tactic without sorries
        info = output.info
        sorry_states = []
        if 'sorries' in info: # 先解析 sorries
            for sorry in info.get('sorries'):
                start_pos, end_pos = sorry.get('pos'), sorry.get('endPos')
                sorry['text'] = text[start_pos, end_pos]
                goals = [sorry["goal"]] if 'goal' in sorry else sorry['goals']
                sorry_states.append(cls(goals, text[:, start_pos], TextSlice(code_before, start_pos, end_pos)))
        return sorry_states, states
    
    def __str__(self):
        return self.pp
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def is_solved(self):
        return len(self.goals) == 0


class FileLean():
    def __init__(self,
                 cwd: Optional[Path] = None,
                 timeout: int = 600,
                 header: Optional[str] = None):
        # initialize
        cwd = cwd or read_mathlib_cache(DEFAULT_LEAN4_VERSION)
        assert cwd is not None, "Mathlib cache not found. Try running `filelean install [version]`"
        self.cwd = Path(cwd).resolve()
        self.timeout = timeout
        self.header = header
        self.version = self.lean_version()
    
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

    def run_tac(self, state:FileState, tactic:str) -> FileState:
        if state.is_solved:
            raise LeanError("No goals to be solved.")
        code_before = f"{state.code_before}\n{tactic}"
        new_state = self.from_proof(code_before)
        if new_state.is_solved:
            return new_state
        return new_state
    
    def init_state(self, theorem:str) -> FileState:
        """Initial state for theorem
        
        Example:
            >>> fl = FileLean()
            >>> fl.init_state('theorem foo (a b : Nat) : a + b = b + a')"""
        code_before = f"{theorem} := by"
        return self.from_proof(code_before)
    
    def from_proof(self, proof) -> FileState:
        """Get proof state from proof"""
        output = self.run_command(proof)
        sorries, states = FileState.from_lean_output(output, proof)
        if len(sorries):
            raise NotImplementedError("Sorries are not supported.")
        if len(states) == 0:
            states = [FileState([], proof)]
        if not len(states) == 1:
            raise TacticFailure(f"Expected 1 state, got {len(states)}")
        return states[0]

    def run_command(self, command:str) -> LeanOutput:
        """Run lean command"""
        if self.header:
            command = f"{self.header}\n{command}"
        msg, err, code = execute_lean_code(command, cwd=self.cwd, timeout=self.timeout)
        output = LeanOutput(msg)
        if code != 0:
            output.lean_error = err
        return output