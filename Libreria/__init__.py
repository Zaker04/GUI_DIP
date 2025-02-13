# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:54:07 2019

@author: turtw
"""
import os


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('Libreria', parent_package, top_path)

    config.add_subpackage('MyLib/')


    # def add_test_directories(arg, dirname, fnames):
        # if dirname.split(os.path.sep)[-1] == 'tests':
            # config.add_data_dir(dirname)

    #Add test directories
    # from os.path import isdir, dirname, join
    # rel_isdir = lambda d: isdir(join(curpath, d))

    # curpath = join(dirname(__file__), './')
    # subdirs = [join(d, 'tests') for d in os.listdir(curpath) if rel_isdir(d)]
    # subdirs = [d for d in subdirs if rel_isdir(d)]
    # for test_dir in subdirs:
        # config.add_data_dir(test_dir)
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup

    config = configuration(top_path='').todict()
    setup(**config)

#Imagenologia/                           #Top-level package
#__init__.py                 #Initialize the sound package
#            FuzzyFunctions/             #Subpackage for file format conversions
#                  __init__.py
#                  Function.py
#                  wavwrite.py
#                  aiffread.py
#                  aiffwrite.py
#                  auread.py
#                  auwrite.py
 #                 ...
 #           XFunctions/                #Subpackage for Imagenologia effects
 #                 __init__.py
#                  echo.py
#                  surround.py
#                  reverse.py
#                  ...
  #          YFunctions/                #Subpackage for YFunctions
   #               __init__.py
#                  equalizer.py
#                  vocoder.py
#                  karaoke.py