#!/usr/bin/env python

import os
import sys


from kido.models import db

from alembic import command
from alembic.config import Config


def main():

    if not os.path.exists('alembic/versions'):
        os.mkdir('alembic/versions')

    force = True if len(sys.argv) > 1 and sys.argv[1] == '--force' else False
    if force or raw_input('Really drop and recreate all tables? (y/N)') == 'y':
        db.drop_all()
        db.session.execute('DROP TABLE IF EXISTS alembic_version')
        db.session.commit()
        db.create_all()
        print('Created all tables.')
        alembic_cfg = Config('alembic.ini')
        command.stamp(alembic_cfg, 'head')
        print('Setup Alembic for database migrations.')
    else:
        print('Exiting.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
