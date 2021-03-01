#!/usr/bin/env python3

from jeffy.framework import get_app

from lib.config.container import Container

app = get_app()


@app.handlers.common()
def handler(event, context):
    app.logger.info('========start execution========')
    app.logger.info(event)

    container: Container = Container()
    container.slack_inject()
    res = container.controller.execute(event)

    app.logger.info('========end execution========')
    return res
