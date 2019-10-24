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
        'Pebble @ git+https://github.com/schipiga/pebble@v4.4.1',
        'multilock @ git+https://github.com/schipiga/multilock@v0.1'],
)
