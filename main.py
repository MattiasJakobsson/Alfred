#!/usr/bin/python3

import logging
from waitress import serve
import automation.workflows.workflow_manager
import plugins.plugin_manager
from api.app import configure


def main():
    logging.basicConfig(level=logging.ERROR)

    logging.info('Starting application')

    automation.workflows.workflow_manager.bootstrap()

    plugins.plugin_manager.bootstrap()

    api = configure()

    logging.info('Starting web api')

    serve(api, listen='*:8000')

    logging.info('Stopping application')

    automation.workflows.workflow_manager.shut_down()

    logging.info('Application shut down')

if __name__ == '__main__':
    main()
