""" Duk setup """

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension  # pylint: disable=E0611,F0401

import versioneer

setup(
    name='duk',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[],
    packages=['duk'],
    author='Werner Van Geit',
    author_email='werner.vangeit@gmail.com',
    description='Python wrapper around the du -ks command',
    long_description="Duk is a commandline utility that wraps around the "
    "linux 'du -ks' command. It will show you a histogram of the "
    "disk usage in a directory",
    entry_points={'console_scripts': ['duk=duk.duk:main'], },
    license="LGPLv3",
    keywords=(),
    url='https://github.com/wvangeit/duk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities'])
