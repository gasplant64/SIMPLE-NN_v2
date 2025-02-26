from setuptools import setup, find_packages, Extension
# To use a consistent encoding
from codecs import open
from os import path, listdir
from pkg_resources import DistributionNotFound, get_distribution
from subprocess import check_output
import sys

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version number.
exec(open('simple_nn/_version.py').read())

def git_sha():
    try:
        sha = check_output(['git', 'rev-parse', 'HEAD'], cwd=here).decode('ascii').strip()[:7]
    except:
        sha = 'unknown'
    return sha

with open('simple_nn/_version.py', 'w') as fp:
    fp.write('__version__ = "{0:}"\n'.format(__version__))
    fp.write('__git_sha__ = "{0:}"\n'.format(git_sha()))

# required module
# TODO: version check
install_requires = [
    'matplotlib<3.4.0,>=3.1.0',
    'scikit-learn<1.0',
    'numpy>=1.22',
    'scipy<1.6.0',
    'ase==3.22.0',
    'pyyaml',
    'cffi',
    'psutil',
    'tqdm',
    'braceexpand',
]

setup_requires = [
    'cffi',
]

def is_installed(pkg):
    try:
        a = get_distribution(pkg)
        return True
    except DistributionNotFound:
        return False

#if is_installed('torch'):
#install_requires.append('torch')
#else:
#    install_requires.append('torch')

# TODO: install requires add
# FIXME: fill the empty part
setup(
    name='simple-nn',
    version=__version__,
    description='Package for generating atomic potentials using neural network.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MDIL-SNU/SIMPLE-NN', # temperary url 
    author='Kyuhyun Lee, Dongsun Yoo, Jisu Jung, Seungwoo Hwang, Sangmin Oh',
    author_email='khlee1992@naver.com',
    license='GPL-3.0',
    classifiers=[   # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Stable',

        # other arguments are listed here.
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

    ],
    #keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={'':['*.cpp', '*.h']},
    #project_urls={},
    python_requires='>=3.6',
    install_requires=install_requires,
    setup_requires=setup_requires,
    cffi_modules=[
        "simple_nn/features/symmetry_function/libsymf_builder.py:ffibuilder",
        "simple_nn/utils/libgdf_builder.py:ffibuilder",
    ],
)

with open('simple_nn/_version.py', 'w') as fp:
    fp.write('__version__ = "{0:}"\n'.format(__version__))
    fp.write('__git_sha__ = "unknown"\n')
