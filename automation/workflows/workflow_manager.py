from automation.event_publisher import subscribe, publish_event
import copy
from data_access.database_manager import DatabaseManager
import importlib
import uuid
import logging


database_manager = DatabaseManager()
in_memory_workflows = {}
active_triggers = []


def get_workflow_definition(workflow_id):
    return in_memory_workflows[workflow_id] if workflow_id in in_memory_workflows \
        else database_manager.get_by_id('workflows', workflow_id)


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
    logging.info('Starting to execute workflowstep "%s" for workflow "%s"' % (step_id, workflow_id))

    workflow = get_workflow_definition(workflow_id)
    step_definition = get_step_definition(workflow, step_id)

    step = get_step(step_definition)

    def step_executed(result):
        logging.info('Workflowstep "%s" for workflow "%s" executed with result: %s' %
                     (step_id, workflow_id, str(result)))

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

    logging.info('Going to execute workflowstep %s with state %s' % (step_id, str(data['state'])))

    step.execute(step_definition, data['state'], step_executed)


def bootstrap():
    def execute_next_step(data):
        workflow_id = data['workflow_id']
        step_id = data['next_step']

        if step_id:
            execute_workflow_step(workflow_id, step_id, data)
        else:
            publish_event('workflow_finished', {'state': data['state']})

    def start_workflow(data):
        workflow_id = data['workflow_id']

        workflow = get_workflow_definition(workflow_id)

        step_id = workflow['initial_step']['id']

        initial_state = {step_id: data['initial_state'], 'initial_state': data['initial_state']}

        execute_workflow_step(workflow_id, step_id,
                              {'workflow_instance_id': str(uuid.uuid4()), 'state': initial_state})

    subscribe('workflow_step_executed', execute_next_step)
    subscribe('new_workflow_instance_requested', start_workflow)

    triggers = database_manager.get_all('workflow_triggers')

    for trigger in triggers:
        trigger_module = importlib.import_module(trigger['config']['type'], package='automation')

        trigger_instance = trigger_module.set_up(trigger['workflow_id'], trigger['config'])

        active_triggers.append({
            'instance': trigger_instance,
            'workflow_id': trigger['workflow_id'],
            'trigger_id': trigger.eid
        })

    publish_event('workflows_started', {})


def shut_down():
    logging.info('Shutting down workflows')

    publish_event('workflows_stopped', {})

    logging.info('Workflows shut down')


def define_workflow(workflow_definition, triggers, store=True):
    def add_in_memory_workflow(definition):
        new_workflow_id = str(uuid.uuid4())

        in_memory_workflows[new_workflow_id] = definition

        return new_workflow_id

    workflow_id = database_manager.insert('workflows', workflow_definition) if store \
        else add_in_memory_workflow(workflow_definition)

    for trigger in triggers:
        trigger_id = ''

        if store:
            trigger_id = database_manager.insert('workflow_triggers', {
                'workflow_id': workflow_id,
                'config': trigger
            })

        trigger_module = importlib.import_module(trigger['type'], package='automation')

        trigger_instance = trigger_module.set_up(workflow_id, trigger)

        active_triggers.append({
            'instance': trigger_instance,
            'workflow_id': workflow_id,
            'trigger_id': trigger_id
        })

    return workflow_id


def remove_workflow(workflow_id):
    stored = workflow_id not in in_memory_workflows

    if stored:
        database_manager.delete('workflows', workflow_id)
    else:
        del in_memory_workflows[workflow_id]

    triggers = [trigger for trigger in active_triggers if trigger['workflow_id'] == workflow_id]

    for trigger in triggers:
        trigger['instance']['dispose']()

        active_triggers.remove(trigger)

        if stored:
            database_manager.delete('workflow_triggers', trigger['trigger_id'])
