#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from helper import run, unzip
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LBFORUM_ROOT = STATIC_FOLDER = os.path.join(HERE, "../")
TOOLS_FOLDER = os.path.join(LBFORUM_ROOT, "tools/")
LBFORUM_ENV = os.path.join(LBFORUM_ROOT, "lbforum_env/")
REQ_FOLDER = os.path.join(LBFORUM_ROOT, "requirements/")
STATIC_FOLDER = os.path.join(LBFORUM_ROOT, "sites/default/static/")

def do_unzip():
    print '== do_unzip =='
    tools_zip_folder = os.path.join(TOOLS_FOLDER, "zip/")
    req_zip_folder = os.path.join(REQ_FOLDER, "zip/")
    unzip(os.path.join(req_zip_folder, "registration.zip"), REQ_FOLDER)
    static_scripts_folder = os.path.join(STATIC_FOLDER, 'scripts')

def do_pip():
    pip = os.path.join(LBFORUM_ENV, "Scripts/pip.exe")
    if os.name == 'posix':
        pip = os.path.join(LBFORUM_ENV, "bin/pip")
    print '== do_pip =='
    run('%s %s' % (pip, 'Django==1.2.3'))
    run('%s %s' % (pip, 'PIL'))
    run('%s %s' % (pip, 'django-pagination'))
    run('%s %s' % (pip, 'South'))

if __name__ == '__main__':
    do_unzip()
    virtualenv_py = os.path.join(TOOLS_FOLDER, "virtualenv.py")
    print '== create LBFORUM_ENV =='
    run('python %s %s' % (virtualenv_py, LBFORUM_ENV))
    do_pip()
