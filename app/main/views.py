from flask import render_template, make_response, current_app

from app.main import bp


# Client routing
@bp.route('/')
@bp.route('/register')
@bp.route('/login')
@bp.route('/track-map')
@bp.route('/manager-page')
def index():
    return render_template('index.html')


@bp.route('/status')
def status():
    current_app.logger.debug('Site status: OK')
    return make_response({'message': 'Status: OK'}, 200)
