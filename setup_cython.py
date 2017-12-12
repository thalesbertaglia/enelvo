from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("enelvo.metrics.cythonlcs", ["enelvo/metrics/cythonlcs.pyx"], include_dirs=['.'])]

setup(
  name='cythonlcs',
  cmdclass={'build_ext': build_ext},
  ext_modules=ext_modules,
  script_args=['build_ext'],
  options={'build_ext':{'inplace':True, 'force':True}}
)

print('********CYTHON COMPLETE******')
