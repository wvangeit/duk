[![Build Status](https://travis-ci.org/wvangeit/duk.svg?branch=master)](https://travis-ci.org/wvangeit/duk)

Introduction
============

Duk is a commandline utility that wraps around the linux 'du -ks' command.
It will show you a histogram of the disk usage in a directory:

```bash
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Statistics of directory "." :

in kByte       in %   histogram            Name      
4              1.39   #                    .gitignore
4              1.39   #                    setup.py  
4              1.39   #                    .travis.yml
4              1.39   #                    README.md 
12             4.17   ##                   dist/     
12             4.17   ##                   duk/      
12             4.17   ##                   build/    
16             5.56   ##                   duk.egg-info/
220            76.39  #################### .git/     

Total directory size: 288 kByte
```

Installation                                                                     
============

The easiest way to install duk is to use [pip](https://pip.pypa.io)             

```bash                                                                          
pip install duk                                                                 
```          

In case you're not in a python virtualenv, or don't have administrator access on your computer, you could use:

```bash                                                                          
pip install --user duk                                                                 
```    
