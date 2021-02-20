#!/usr/bin/env python3

from jeffy.framework import get_app

from lib.config.container import Container

app = get_app()


@app.handlers.common()
def handler(event, context):
    app.logger.info('========start get_file_list========')
    app.logger.info(event)

    container: Container = Container()
    container.slack_inject()
    res = container.file_controller.list(event)

    app.logger.info('========end get_file_list========')
    return res
