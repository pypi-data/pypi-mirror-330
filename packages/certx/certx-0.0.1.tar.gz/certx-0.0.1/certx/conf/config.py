from oslo_config import cfg
from oslo_log import log as logging

default_opts = [
    cfg.StrOpt('host', help='the server ip', default='127.0.0.1'),
    cfg.IntOpt('port', help='Port for server', default='9999')
]

database_group = cfg.OptGroup(
    'database',
    title='Database Options',
    help='Configuration options for Database Connection'
)
database_opts = [
    cfg.StrOpt('url', help='Database Connection url', default='sqlite:///certx.db'),
    cfg.BoolOpt('enable_track_modifications', help='Enable trace modifications', default=False),
]

certificate_repository_group = cfg.OptGroup(
    'certificate_repository',
    title='Certificate Repository Options',
    help='Configuration options for Certificate Repository'
)
certificate_repository_opts = [
    cfg.StrOpt('default', help='Default Certificate repository type', default='db')
]

certificate_file_repository_group = cfg.OptGroup(
    'certificate_file_repository',
    title='Certificate File Repository Options',
    help='Configuration options for Certificate File Repository'
)
certificate_file_repository_opts = [
    cfg.StrOpt('path', help='The base path for save CA and certificate files', default='cert-repo')
]

flask_group = cfg.OptGroup(
    'flask',
    title='Database Options',
    help='Configuration options for Database Connection'
)
flask_opts = [
    cfg.BoolOpt('threaded', help='Make server run in multi-thread', default=True),
    cfg.BoolOpt('debug', help='Flask run on debug mode', default=True)
]

CONF = cfg.CONF
CONF.register_opts(default_opts)
CONF.register_opts(database_opts, group=database_group)
CONF.register_opts(certificate_repository_opts, group=certificate_repository_group)
CONF.register_opts(certificate_file_repository_opts, group=certificate_file_repository_group)
CONF.register_opts(flask_opts, group=flask_group)

logging.register_options(CONF)


def init(args, **kwargs):
    cfg.CONF(args=args, project='certx', **kwargs)
    logging.setup(CONF, 'certx')
