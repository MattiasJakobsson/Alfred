from automation.event_publisher import publish_event, subscribe
import importlib
import inspect
from threading import Thread


def get_available_settings():
    return ['task', 'parameters']


class BackgroundTask(Thread):
    def __init__(self, task, start_workflow):
        super(BackgroundTask, self).__init__(target=self.start_task)
        self._task = task
        self._start_workflow = start_workflow

    def start_task(self):
        self._task.start(self._start_workflow)

    def stop_task(self):
        self._task.stop()


def set_up(workflow_id, data):
    def start_workflow(state):
        publish_event('new_workflow_instance_requested', {'workflow_id': workflow_id, 'initial_state': state})

    module_name, class_name = data['task'].rsplit('.', 1)

    task = getattr(importlib.import_module(module_name), class_name)

    parameters = data['parameters'] if 'parameters' in data else {}

    arguments = [parameters[p] if p in parameters else None
                 for p in list(inspect.signature(task).parameters) if p != 'self']

    task_instance = task(*arguments)

    background_task = BackgroundTask(task_instance, start_workflow)

    background_task.start()

    def stop_task(_, __):
        background_task.stop_task()

    subscription = subscribe('workflows_stopped', stop_task)

    def dispose():
        subscription['dispose']()
        background_task.stop_task()

    return {
        'dispose': dispose
    }
