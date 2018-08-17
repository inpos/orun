import setuptools
import os

def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
# setuptools
extra_files = package_files('examples')
extra_files.extend(package_files(os.path.join('orun', 'extjs', 'static')))
extra_files.append(os.path.join('orun', 'extjs', 'app.html'))
# distutils
d_files = package_files(os.path.join('orun', 'examples'))
d_files.extend(package_files(os.path.join('orun', 'extjs', 'static')))
d_files.append(os.path.join('orun', 'extjs', 'app.html'))

setuptools.setup(
    name='Orun',
    version='0.4.0',
    author='Alexandre L. Dias, Roman Borodin (inpos@yandex.ru)',
    author_email='alexandre@katrid.com',
    packages=setuptools.find_packages(),
    package_data={'': extra_files},
    data_files=[('',[ os.path.join('orun', x) for x in extra_files  ])],
    include_package_data=True,
    url='http://pypi.python.org/pypi/Orun/',
    license='LICENSE',
    description='Orun (Object RUNtime) Python JavaScript RIA framework.',
    long_description=open('README').read(),
)