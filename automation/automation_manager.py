from data_access.database_manager import DatabaseManager
from automation.event_publisher import subscribe
from plugins.plugin_manager import execute_command

database_manager = DatabaseManager()


def bootstrap():
    automation_jobs = database_manager.get_all('automationjobs')

    for job in automation_jobs:
        start_automation_job(job)


def start_automation_job(job):
    def execute(event_data):
        execute_command(job['target_id'], job['command'], job['parameters'])

    subscribe(job['subscribe_to'], execute)


def add_automation(job):
    database_manager.insert('automationjobs', job)

    start_automation_job(job)
