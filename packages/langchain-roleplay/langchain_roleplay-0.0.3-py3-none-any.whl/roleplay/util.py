import ast
import atexit
import builtins
from getpass import getpass
from os import environ
import os
import sys
import runpy
import signal
import tempfile
import time
from yaml import load, dump, FullLoader

def get_yaml(file_path):
    """
    Reads a yaml file and returns the content as a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as stream:
        return load(stream, Loader=FullLoader)

def get_yaml_from_string(yaml_string):
    """
    Reads a yaml string and returns the content as a dictionary.
    """
    return load(yaml_string, FullLoader)

def write_yaml(data, file_path):
    """
    Writes a dictionary to a yaml file.
    """
    with open(file_path, 'w', encoding='utf-8') as stream:
        dump(data, stream)

def set_if_undefined(var: str) -> None:
    """
    If the environment variable is not set, prompt the user to provide it.
    """
    if not environ.get(var):
        environ[var] = getpass(f"Please provide your {var}")

def get_env_var(var: str) -> str | None:
    """
    Get the value of an environment variable.
    """
    set_if_undefined(var)
    return environ.get(var)

class CodeRunner:
    def __init__(self):
        # 生成临时文件路径并立即关闭文件描述符（解决Windows文件占用问题）
        fd, self.temp_file_path = tempfile.mkstemp(suffix='.py')
        os.close(fd)
        
        atexit.register(self.cleanup)
        self.register_signal_handlers()

    def run(self, code_string, init_globals):
        try:
            with open(self.temp_file_path, 'w', encoding='utf-8') as f:
                f.write(code_string)
            return runpy.run_path(self.temp_file_path, init_globals=init_globals)
        except Exception as e:
            print(f"An error occurred while running the code: {e}")
            return {'result': f"An error occurred while running the code: {e}"}

    def cleanup(self):
        # 增加重试机制处理Windows文件锁问题
        if os.path.exists(self.temp_file_path):
            for _ in range(3):  # 最多重试3次
                try:
                    os.remove(self.temp_file_path)
                    print(f"Temporary file {self.temp_file_path} cleaned up")
                    break
                except Exception as e:
                    print(f"Cleanup failed: {e}, retrying...")
                    time.sleep(0.1)

    def register_signal_handlers(self):
        # Windows兼容的信号处理
        if sys.platform == 'win32':
            signal.signal(signal.SIGINT, self.handle_exit)
            # 注册Windows控制台关闭事件
            if hasattr(signal, 'SIGBREAK'):
                signal.signal(signal.SIGBREAK, self.handle_exit)
        else:
            signal.signal(signal.SIGINT, self.handle_exit)
            signal.signal(signal.SIGTERM, self.handle_exit)

    def handle_exit(self, signum, frame):
        print(f"\nReceived termination signal ({signum}), cleaning up...")
        self.cleanup()
        os._exit(1 if signum else 0)

_code_runner = CodeRunner()
_show_map = {}

class SafeEval:
    """
    A class to evaluate expressions safely with a blacklist approach.
    Only import operations are prohibited; otherwise, most built-in functions are allowed.
    """
    LIST = {
        # 'ChatOpenAI': ChatOpenAI,
        '__name__': '__safe_eval__',
        '_show_map': _show_map,
        # 'AIMessage': AIMessage,
        # 'AgentAction': AgentAction,
        # 'AgentFinish': AgentFinish,
        # 'BaseOutputParser': BaseOutputParser,
        # 'OutputParserException': OutputParserException,
    }
    BLACKLIST = {
        'import', 'exec', 'eval', '__import__', 'globals', 'locals', 'open',
        'os', 'sys', 'exit', 'quit', 'getattr', 'setattr', 'delattr', 'execfile',
        'compile', 'input', 'repr', 'eval', 'exec', 'exit', 'os.system'
    }

    def __init__(self, extra_functions=None) -> None:
        self.code_runner = _code_runner
        # We will allow all built-ins except those in the blacklist
        self.safe_builtins = {name: func for name, func in builtins.__dict__.items() if name not in self.BLACKLIST}
        # self.safe_builtins = builtins.__dict__
        self.safe_builtins.update(self.LIST)
        if extra_functions:
            self.safe_builtins.update(extra_functions)

    def eval(self, expr: str, **variables):
        if not isinstance(expr, str):
            raise TypeError("Expression must be a string")

        # Check blacklist for dangerous operations
        self._check_blacklist(ast.parse(expr, mode='exec'))

        safe_builtins = self.safe_builtins.copy()
        safe_builtins.update(variables)
        # self.safe_builtins['_variables'] = variables
        try:
            # Execute the expression or statement
            # exec(expr, self.safe_builtins, variables)
            result = self.code_runner.run(expr, safe_builtins)
        except Exception as e:
            # Handle the exception and print the error message
            print(f"[SafeEval]: Error occurred: {e}")
            raise
        if 'result' in result:
            # If 'result' is in the variables, return its value
            return result['result']
        raise ValueError("No result found")

    def _check_blacklist(self, tree):
        for node in ast.walk(tree):
            # Check for import statements
            # if isinstance(node, (ast.Import, ast.ImportFrom)):
            #     raise ValueError("Import statements are not allowed")
            # Check for blacklisted names
            if isinstance(node, ast.Name) and node.id in self.BLACKLIST:
                raise ValueError(f"Operation '{node.id}' is not allowed")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                        and node.func.id in self.BLACKLIST:
                raise ValueError(f"Function '{node.func.id}' is not allowed")
