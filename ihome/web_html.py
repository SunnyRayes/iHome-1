from flask import Blueprint, current_app

html = Blueprint('html', __name__)


@html.route('/<re(r".*"):file_name>')
def get_html(file_name):
    if file_name == '':
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        file_name = 'html/%s' % file_name
    return current_app.send_static_file(file_name)