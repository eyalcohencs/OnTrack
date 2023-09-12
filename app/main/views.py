import logging

from flask import render_template, make_response, current_app

from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/status')
def status():
    # current_app.logger.setLevel(logging.DEBUG)
    #
    # current_app.logger.info('Site status: INFO check - DEBUG level - app.logger')
    # current_app.logger.error('Site status: ERROR check - DEBUG level - app.logger')
    #
    # logger = logging.getLogger()
    # logger.info('Site status: INFO check - DEBUG level - logger')
    # logger.error('Site status: ERROR check - DEBUG level - logger')
    #
    # current_app.logger.setLevel(logging.INFO)
    #
    # current_app.logger.info('Site status: INFO check - INFO level - app.logger')
    # current_app.logger.error('Site status: ERROR check - INFO level - app.logger')
    #
    # logger = logging.getLogger()
    # logger.info('Site status: INFO check - INFO level - logger')
    # logger.error('Site status: ERROR check - INFO level - logger')
    #
    # console_handler = logging.StreamHandler()
    # logger.addHandler(console_handler)
    #
    # logger.info('Site status: INFO check - INFO level - logger with stream handler')
    # logger.error('Site status: ERROR check - INFO level - logger with stream handler')
    #
    # current_app.logger.setLevel(logging.DEBUG)
    #
    # logger.info('Site status: INFO check - DEBUG level - logger with stream handler')
    # logger.error('Site status: ERROR check - DEBUG level - logger with stream handler')

    current_app.logger.setLevel(logging.INFO)
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    current_app.logger.info('INFO - Site status: OK')
    return make_response('Status: OK', 200)
