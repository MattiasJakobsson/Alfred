from data_access.database_manager import DatabaseManager
from automation.event_publisher import subscribe
from automation.scheduler import add_job

database_manager = DatabaseManager()


def bootstrap(execute_command):
    automation_jobs = database_manager.get_all('automationjobs')

    for job in automation_jobs:
        start_automation_job(job, execute_command)


def start_automation_job(job, execute_command):
    def start_subscription(job_data):
        def execute(event_data):
            execute_command(job_data['target_id'], job_data['command'], job_data['parameters'])

        subscribe(job_data['subscribe_to'], execute)

    def start_interval(job_data):
        def execute():
            execute_command(job_data['target_id'], job_data['command'], job_data['parameters'])

        add_job(execute, 'interval', seconds=job_data['interval'])

    job_types_executions = {'subscription': start_subscription, 'interval': start_interval}

    job_types_executions[job['type']](job)


def add_automation(job, execute_command):
    database_manager.insert('automationjobs', job)

    start_automation_job(job, execute_command)
