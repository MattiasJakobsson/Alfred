import json
from data_access.database_manager import DatabaseManager
from automation.workflows.workflow_manager import define_workflow, remove_workflow, get_available_steps, \
    get_available_triggers


def bootstrap(application):
    automation_list = AutomationList()
    workflow_delete = WorkflowDelete()
    available_automations = AvailableAutomations()

    application.add_route('/automations', automation_list)
    application.add_route('/automations/{workflow_id}/remove', workflow_delete)
    application.add_route('/automations/available', available_automations)


class AutomationList:
    def __init__(self):
        self._database_manager = DatabaseManager()

    def on_get(self, req, resp):
        data = [{'definition': workflow, 'id': workflow.eid}
                for workflow in self._database_manager.get_all('workflows')]

        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(data))

    def on_post(self, req, resp):
        data = json.loads(req.bounded_stream.read().decode())

        define_workflow(data['definition'], data['triggers'])


class WorkflowDelete:
    def on_post(self, req, resp, workflow_id):
        remove_workflow(int(workflow_id))


class AvailableAutomations:
    def on_get(self, req, resp):
        data = {
            'steps': get_available_steps(),
            'triggers': get_available_triggers()
        }

        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(data))
