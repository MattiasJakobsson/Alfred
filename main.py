#!/usr/bin/env python3

import logging
from waitress import serve
import automation.workflows.workflow_manager
import plugins.plugin_manager
from api.app import configure
import sys
import deamon


def main():
    logging.basicConfig(level=logging.INFO)

    logging.info('Starting application')

    automation.workflows.workflow_manager.bootstrap()

    plugins.plugin_manager.bootstrap()

    api = configure()

    logging.info('Starting web api')

    serve(api, listen='*:8000')

    logging.info('Stopping application')

    automation.workflows.workflow_manager.shut_down()

    logging.info('Application shut down')


class MyDaemon(deamon.Daemon):
    def run(self):
        main()

if __name__ == '__main__':
    daemon = MyDaemon('/alfred_deamon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('Unknown command')
            sys.exit(2)

        sys.exit(0)
    else:
        main()
