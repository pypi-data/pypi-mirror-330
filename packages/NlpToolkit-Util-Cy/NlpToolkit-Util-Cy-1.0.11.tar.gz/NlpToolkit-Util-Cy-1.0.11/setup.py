from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Util/*.pyx"], compiler_directives={'language_level' : "3"}),
    name='NlpToolkit-Util-Cy',
    version='1.0.11',
    packages=['Util'],
    package_data={'Util': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/StarlangSoftware/Util-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Simple Utils',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
