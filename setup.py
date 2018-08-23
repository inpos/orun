import setuptools

setuptools.setup(
    name='Orun',
    version='0.4.0',
    author='Alexandre L. Dias, Roman Borodin (inpos@yandex.ru)',
    author_email='alexandre@katrid.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='http://pypi.python.org/pypi/Orun/',
    license='LICENSE',
    description='Orun (Object RUNtime) Python JavaScript RIA framework.',
    long_description=open('README').read(),
)
