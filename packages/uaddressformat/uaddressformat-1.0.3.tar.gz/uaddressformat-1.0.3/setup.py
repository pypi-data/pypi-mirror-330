try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to "
        "https://pypi.python.org/pypi/setuptools and follow the instructions "
        "for installing setuptools"
    )

setup(
    name='uaddressformat',
    description='Library for uaddress package. Format types addresses',
    version='1.0.3',
    author='Evgen Kytonin',
    author_email='killfess@gmail.com',
    license='MIT',
    keywords=['module', 'parse', 'uaddress'],
    url='https://github.com/RapidappsIT/uaddressformat',
    packages=['uaddressformat']
)