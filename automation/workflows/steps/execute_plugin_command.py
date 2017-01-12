from plugins.plugin_manager import execute_command


def execute(config, data):
    plugin_id = config['plugin_id']
    command = config['command']
    parameters = config['parameters']

    execute_command(plugin_id, command, parameters)
