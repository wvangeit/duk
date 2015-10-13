""" Duk setup """

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension  # pylint: disable=E0611,F0401

setup(
    name='duk',
    version=0.2,
    install_requires=[],
    packages=['duk'],
    author='Werner Van Geit',
    author_email='werner.vangeit@gmail.com',
    description='Duk',
    long_description="",
    entry_points={'console_scripts': ['duk=duk.duk:main'], },
    license="LGPLv3",
    keywords=(),
    url='https://github.com/wvangeit/duk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities'])
