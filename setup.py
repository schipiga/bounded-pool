from setuptools import setup


setup(
    name='bounded_pool',
    version='0.1',
    description='Bounded processes & threads pool executor',
    url='https://github.com/schipiga/bounded-pool/',
    author='Sergei Chipiga <chipiga86@gmail.com>',
    author_email='chipiga86@gmail.com',
    py_modules=['bounded_pool'],
    install_requires=[
        'Pebble==4.4.0',
        'multilock @ git+https://github.com/schipiga/multilock@v0.1'],
)
