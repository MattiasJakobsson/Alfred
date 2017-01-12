from plugins.plugin_manager import get_query_result


def execute(config, data):
    plugin_id = config['plugin_id']
    query = config['query']
    parameters = config['parameters']

    return get_query_result(plugin_id, query, parameters)
