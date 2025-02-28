from os import PathLike, makedirs
from os.path import expanduser, expandvars, isfile, join, normpath
from typing import Union, Dict, Callable, Any, Optional
import re
import ast
import pickle
import base64

def check_path(
    path: Union[str, PathLike],
    exist: bool = True,
    file: bool = True,
    parents: bool = True,
) -> str:
    """
    Check path and return corrected path.
    """
    # normalize and expand a path
    path = normpath(expandvars(expanduser(path)))
    if exist and file and not isfile(path):
        raise FileNotFoundError(path)
    else:
        if file:
            dir_path = normpath(join(path, ".."))
        else:
            dir_path = path
        if parents:
            makedirs(dir_path, exist_ok=True)
    return path


def compile_func(func_code: str, global_env: Optional[Dict[str, Any]] = None) -> Callable:
    """
Compile a Python function string into an executable function and return it.

Args:
    func_code (str): A string containing Python function code
    global_env (str): Packages and global variables used in the Python function


Examples:
    
    from lazyllm.common import compile_func
    code_str = 'def Identity(v): return v'
    identity = compile_func(code_str)
    assert identity('hello') == 'hello'
    """
    fname = re.search(r'def\s+(\w+)\s*\(', func_code).group(1)
    module = ast.parse(func_code)
    func = compile(module, filename="<ast>", mode="exec")
    local_dict = {}
    exec(func, global_env, local_dict)
    return local_dict[fname]

def obj2str(obj: Any) -> str:
    return base64.b64encode(pickle.dumps(obj)).decode('utf-8')

def str2obj(data: str) -> Any:
    return None if data is None else pickle.loads(base64.b64decode(data.encode('utf-8')))
