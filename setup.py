import setuptools
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('examples')
extra_files.extend(package_files('extjs/static'))

setuptools.setup(
    name='Orun',
    version='0.1.0',
    author='Alexandre L. Dias',
    author_email='alexandre@katrid.com',
    packages=setuptools.find_packages(),
    package_data={'': extra_files},
    include_package_data=True,
    url='http://pypi.python.org/pypi/Orun/',
    license='LICENSE',
    description='Orun (Object RUNtime) Python JavaScript RIA framework.',
    long_description=open('README').read(),
)