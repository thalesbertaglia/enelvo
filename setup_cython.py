from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup, Extension

ext_modules = [
    Extension(
        "enelvo.metrics.cythonlcs", ["enelvo/metrics/cythonlcs.pyx"], include_dirs=["."]
    )
]

setup(
    name="cythonlcs",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    script_args=["build_ext"],
    options={"build_ext": {"inplace": True, "force": True}},
)

print("********CYTHON COMPLETE******")
