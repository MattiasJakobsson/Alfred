import re
import sys
import string


def run_python_code(data, global_dict=None, local_dict=None, error_logger=None):
    if global_dict is None:
        global_dict = {}

    eval_state = EvalState(global_dict, local_dict, error_logger)

    data = re.sub(r'(?s)\[\?\?(?P<code>.+?)\?\?\]', eval_state.eval_python, data)
    return data


class EvalState:
    def __init__(self, global_dict, local_dict, error_logger):
        self.global_dict = global_dict
        self.local_dict = local_dict
        if error_logger:
            self.errorLogger = error_logger
        else:
            self.errorLogger = sys.stdout.write

        self.global_dict['sys'] = sys
        self.global_dict['string'] = string
        self.global_dict['__builtins__'] = __builtins__

    def eval_python(self, result):
        code = result.group('code')
        code = code.replace('\t', '    ')

        try:
            if self.local_dict:
                result = eval(code, self.global_dict, self.local_dict)
            else:
                result = eval(code, self.global_dict)
            return str(result)
        except:
            self.errorLogger('\n---- Error parsing: ----\n')
            self.errorLogger(code)
            self.errorLogger('\n------------------------\n')
            raise
