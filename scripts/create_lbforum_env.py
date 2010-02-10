#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from helper import run, unzip
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LBFORUM_ROOT = STATIC_FOLDER = os.path.join(HERE, "../")
TOOLS_FOLDER = os.path.join(LBFORUM_ROOT, "tools/")
TOOLS_ZIP_FOLDER = os.path.join(TOOLS_FOLDER, "zip/")
LBFORUM_ENV = os.path.join(LBFORUM_ROOT, "lbforum_env/")

#print run('dir', env=None)
#echo python %~dp0..\tools\virtualenv.py %~dp0..\lbforum_env
#call %~dp0..\lbforum_env\Scripts\activate.bat
def do_unzip():
    print '== do_unzip =='
    print 'unzip virtualenv'
    unzip(os.path.join(TOOLS_ZIP_FOLDER, "virtualenv.zip"), TOOLS_FOLDER)

if __name__ == '__main__':
    #do_unzip()
    virtualenv_py = os.path.join(TOOLS_FOLDER, "virtualenv.py")
    print '== create LBFORUM_ENV =='
    run('python %s %s' % (virtualenv_py, LBFORUM_ENV))
