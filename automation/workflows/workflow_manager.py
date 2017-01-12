from automation.event_publisher import subscribe, publish_event
import copy
from data_access.database_manager import DatabaseManager
import importlib
import uuid


database_manager = DatabaseManager()


def get_workflow_definition(workflow_id):
    return database_manager.get_by_id('workflows', workflow_id)


def get_step_definition(workflow, step_id):
    def get_step_from(parent):
        if parent['id'] == step_id:
            return parent

        if 'children' not in parent:
            return None

        for child in parent['children']:
            step = get_step_from(child)

            if step:
                return step

        return None

    return get_step_from(workflow['initial_step'])


def get_step(step_definition):
    return importlib.import_module(step_definition['type'], package='automation')


def execute_workflow_step(workflow_id, step_id, data):
    workflow = get_workflow_definition(workflow_id)
    step_definition = get_step_definition(workflow, step_id)

    step = get_step(step_definition)

    def step_executed(result):
        state = copy.deepcopy(data['state'])

        state[step_definition['id']] = result

        publish_event('workflow_step_executed', {
            'workflow_id': workflow_id,
            'workflow_instance_id': data['workflow_instance_id'],
            'next_step': result['next_step'] if result and 'next_step' in result
            else step_definition['children'][0]['id']
            if 'children' in step_definition and len(step_definition['children']) > 0 else None,
            'state': state
        })

    step.execute(step_definition, data['state'], step_executed)


def bootstrap():
    def execute_next_step(data):
        workflow_id = data['workflow_id']
        step_id = data['next_step']

        if step_id:
            execute_workflow_step(workflow_id, step_id, data)

    def start_workflow(data):
        workflow_id = data['workflow_id']

        workflow = get_workflow_definition(workflow_id)

        step_id = workflow['initial_step']['id']

        initial_state = {step_id: data['initial_state']}

        execute_workflow_step(workflow_id, step_id, {'workflow_instance_id': str(uuid.uuid4()), 'state': initial_state})

    subscribe('workflow_step_executed', execute_next_step)
    subscribe('new_workflow_instance_requested', start_workflow)

    triggers = database_manager.get_all('workflow_triggers')

    for trigger in triggers:
        module = importlib.import_module(trigger['config']['type'], package='automation')

        module.set_up(trigger['workflow_id'], trigger['config'])


def define_workflow(workflow_definition, triggers):
    workflow_id = database_manager.insert('workflows', workflow_definition)

    for trigger in triggers:
        database_manager.insert('workflow_triggers', {
            'workflow_id': workflow_id,
            'config': trigger
        })

        module = importlib.import_module(trigger['type'], package='automation')

        module.set_up(workflow_id, trigger)
