#!/usr/bin/env python

import os
import shutil
import sys
from tempfile import TemporaryDirectory

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from jac.contrib.flask import get_template_dirs

from kido import app


def main():

    env = app.jinja_env

    static_dir = env.compressor_output_dir
    with TemporaryDirectory() as tempdir:

        env.compressor_output_dir = os.path.abspath(tempdir)
        os.chmod(tempdir, 0o775)

        template_dirs = [os.path.join(app.root_path, x)
                         for x in get_template_dirs(app)]

        print('Compressing static assets into {output_dir}'
              .format(output_dir=env.compressor_output_dir))
        compressor = env.extensions['jac.extension.CompressorExtension'].compressor
        compressor.offline_compress(env, template_dirs)

        if os.path.exists(static_dir):
            print('Moving {old} folder to {bak}...'.format(old=static_dir, bak=static_dir + '_old'))
            os.rename(static_dir, static_dir + '_old')
        else:
            print('Old static folder did not exist...')

        print('Moving compressed files into {dest}...'.format(dest=static_dir))
        os.mkdir(static_dir)
        for f in os.listdir(tempdir):
            if f.startswith('.'):
                continue
            os.rename(os.path.join(tempdir, f), os.path.join(static_dir, f))

        if os.path.exists(static_dir + '_old'):
            print('Cleaning up {old}...'.format(old=static_dir + '_old'))
            shutil.rmtree(static_dir + '_old')

    print('Finished.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
