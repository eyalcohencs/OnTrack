import logging

from flask import render_template, make_response, current_app

from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/status')
def status():
    current_app.logger.debug('Site status: OK')
    return make_response('Status: OK', 200)
