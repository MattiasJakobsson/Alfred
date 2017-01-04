import json
from data_access.database_manager import DatabaseManager
from automation.automation_manager import add_automation


def bootstrap(application):
    automation_list = AutomationList()

    application.add_route('/automations', automation_list)


class AutomationList:
    def __init__(self):
        self._database_manager = DatabaseManager()

    def on_get(self, req, resp):
        data = self._database_manager.get_all('automationjobs')

        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(data))

    def on_post(self, req, resp):
        data = json.loads(req.bounded_stream.read().decode())

        add_automation(data)
