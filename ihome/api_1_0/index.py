from . import api
from ihome import session


@api.route('/')
def index():
    # session['name'] = 123
    return 'index'
