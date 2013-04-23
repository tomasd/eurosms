from setuptools import setup, find_packages


setup(
    name='eurosms',
    version='0.1',
    py_modules= ['eurosms'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url='https://github.com/tomasd/eurosms',
    license='',
    include_package_data=True,
    author='Tomas Drencak',
    author_email='tomas@drencak.com',
    description='',
    install_requires=['requests'],
    tests_require=['pyhamcrest', 'nose', 'mock'],
    test_suite='nose.collector'
)
