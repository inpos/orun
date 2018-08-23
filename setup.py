import setuptools
import os

def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk('orun/' + directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

extra_files = package_files('examples')
extra_files.extend(package_files(os.path.join('extjs', 'static')))
extra_files.append(os.path.join('orun', 'extjs', 'app.html'))


setuptools.setup(
    name='Orun',
    version='0.4.0',
    author='Alexandre L. Dias, Roman Borodin (inpos@yandex.ru)',
    author_email='alexandre@katrid.com',
    packages=setuptools.find_packages(),
    package_data={'': extra_files},
    data_files=[('',extra_files)],
    include_package_data=True,
    zip_safe=False,
    url='http://pypi.python.org/pypi/Orun/',
    license='LICENSE',
    description='Orun (Object RUNtime) Python JavaScript RIA framework.',
    long_description=open('README').read(),
)
