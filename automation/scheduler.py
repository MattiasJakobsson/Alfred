from apscheduler.schedulers.background import BackgroundScheduler
import logging


_scheduler = BackgroundScheduler()


def add_job(*args, **kwargs):
    return _scheduler.add_job(*args, **kwargs)


def shut_down():
    logging.info('Shutting down scheduler')

    _scheduler.shutdown()

_scheduler.start()
