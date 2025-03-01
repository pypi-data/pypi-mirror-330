#!/usr/bin/env python
import io, os, re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


# Enable code coverage for C code; `FLAGS=-coverage` cannot be used in tox.ini, since that may interfere with compiling
# dependencies. Rather, set `SETUPPY_CFLAGS=-coverage` in tox.ini and copy it to CFLAGS here (after
# deps have been safely installed).
if 'TOXENV' in os.environ and 'SETUPPY_CFLAGS' in os.environ:
    os.environ['CFLAGS'] = os.environ['SETUPPY_CFLAGS']


extras_require = {
    'shellcomplete': ['click_completion'],
    'tensorflow':    ['tensorflow~=2.0', 'tensorflow-probability~=0.10'],
    'jax': ['jax~=0.1,>0.1.72', 'jaxlib~=0.1,>0.1.51']
}
extras_require['backends'] = sorted(
    set(extras_require['tensorflow'] + extras_require['jax'])
)



setup(
    name='elle',
    version='0.0.4',
    description='A namespace for finite element libraries targeted at research into neural network architectures.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        ""
#       re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.md'))
    ),
    long_description_content_type= 'text/markdown',
    author='Claudio M. Perez',
#   author_email='claudio_perez@berkeley.edu',
#   url='https://github.com/claudioperez/elle',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Organization': 'https://veux.io',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.6',
    install_requires=[
        "opensees", "veux"
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require=extras_require,
)
