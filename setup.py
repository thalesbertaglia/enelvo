import codecs
import os.path
import re
import sys
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup, Extension

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

REQUIRED_PYTHON = (3, 6)

ext_modules = [
    Extension("enelvo.metrics.cythonlcs",
              ["enelvo/metrics/cythonlcs.pyx"], include_dirs=['.'])]

setup(
    name='Enelvo',
    version=find_version("enelvo", "__init__.py"),
    packages=['enelvo', 'enelvo.preprocessing', 'enelvo.candidate_generation',
              'enelvo.candidate_scoring', 'enelvo.metrics',
              'enelvo.utils', 'enelvo.preprocessing.tokenizer'],
    package_data={'enelvo': ['../requirements.txt', 'resources/lexicons/*',
                             'resources/corr-lexicons/*',
                             'resources/embeddings/norm_lexicon.pickle',
                             '../setup_cython.py', '../build/*',
                             'preprocessing/tokenizer/lexicons/*']},
    license='MIT',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Thales Bertaglia',
    author_email='contact@thalesbertaglia.com',
    url='https://github.com/tfcbertaglia/enelvo',
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    include_package_data=True,
    install_requires=[
        'gensim>=3.6.0',
        'emoji>=0.5.1',
        'tabulate>=0.8.2',
        'editdistance>=0.5.2',
        'numpy>=1.16.0',
        'cython==0.29.10'],
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    options={'build_ext': {'inplace': True, 'force': True}},
)
