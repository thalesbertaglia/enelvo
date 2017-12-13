from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext


ext_modules = [
    Extension("enelvo.metrics.cythonlcs", ["enelvo/metrics/cythonlcs.pyx"], include_dirs=['.'])]

setup(
    name='Enelvo',
    version='0.0.3',
    packages=['enelvo', 'enelvo.preprocessing', 'enelvo.candidate_generation',
    'enelvo.candidate_scoring', 'enelvo.metrics', 'enelvo.utils', 'enelvo.preprocessing.tokenizer'],
    package_data = {'enelvo' : ['../requirements.txt', 'resources/lexicons/*',
                    'resources/corr-lexicons/*', 'resources/embeddings/norm_lexicon.pickle',
                    '../setup_cython.py', '../build/*',
                    'preprocessing/tokenizer/lexicons/*'] },
    license='MIT',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Thales Bertaglia',
    author_email='contact@thalesbertaglia.com',
    url='https://github.com/tfcbertaglia/enelvo',
    python_requires='~=3',
    include_package_data=True,
    install_requires=[
        'gensim>=2.2.0',
        'emoji>=0.4.5',
        'tabulate>=0.7.7',
        'editdistance>=0.3.1',
        'numpy>=1.13.3', 'cython'],
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    options={'build_ext':{'inplace':True, 'force':True}},
)
