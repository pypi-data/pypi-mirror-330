import sys

from certx import app
from certx.conf import config
from certx.db.model.models import db

CONF = config.CONF


def start():
    config.init(sys.argv[1:])

    with app.app_context():
        db.create_all()

    app.run(host=CONF.host, port=CONF.port, debug=CONF.flask.debug, threaded=CONF.flask.threaded)


if __name__ == '__main__':
    start()
