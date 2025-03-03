__all__ = [
    'list_opts',
]

import itertools

from certx.conf import config


def list_opts():
    return [
        ('DEFAULT', itertools.chain(config.default_opts, )),
        (config.database_group.name,
         itertools.chain(config.database_opts, )),
        (config.certificate_repository_group.name,
         itertools.chain(config.certificate_repository_opts, )),
        (config.certificate_file_repository_group.name,
         itertools.chain(config.certificate_file_repository_opts, )),
        (config.flask_group.name,
         itertools.chain(config.flask_opts, ))
    ]
