import json
from data_access.database_manager import DatabaseManager
from automation.workflows.workflow_manager import define_workflow


def bootstrap(application):
    automation_list = AutomationList()

    application.add_route('/automations', automation_list)


class AutomationList:
    def __init__(self):
        self._database_manager = DatabaseManager()

    def on_get(self, req, resp):
        data = self._database_manager.get_all('workflows')

        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(data))

    def on_post(self, req, resp):
        data = json.loads(req.bounded_stream.read().decode())

        define_workflow(data['definition'], data['triggers'])
