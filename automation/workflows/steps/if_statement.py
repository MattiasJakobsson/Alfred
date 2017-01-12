from plugins.parameter_handler import run_python_code


def execute(config, state, step_executed):
    if run_python_code(config['if_statement'], local_dict={'state': state}):
        step_executed({'next_step': config['true_step']})
    else:
        step_executed({'next_step': config['false_step']})
