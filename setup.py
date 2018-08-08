from distutils.core import setup

setup(
    name='Orun',
    version='0.1.0',
    author='Alexandre L. Dias',
    author_email='alexandre@katrid.com',
    packages=['orun', 'orun.examples', 'orun.extjs', 'orun.servers'],
    url='http://pypi.python.org/pypi/Orun/',
    license='LICENSE.txt',
    description='Orun (Object RUNtime) Python JavaScript RIA framework.',
    long_description=open('README').read(),
)