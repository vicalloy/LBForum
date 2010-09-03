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

def do_easy_install():
    easy_install = os.path.join(LBFORUM_ENV, "Scripts/easy_install.exe")
    if os.name == 'posix':
        easy_install = os.path.join(LBFORUM_ENV, "bin/easy_install")
    print '== do_easy_install =='
    run('%s %s' % (easy_install, 'http://code.djangoproject.com/svn/django/trunk/'))
    run('%s %s' % (easy_install, 'PIL'))
    run('%s %s' % (easy_install, 'django-pagination'))
    run('%s %s' % (easy_install, 'South'))

if __name__ == '__main__':
    do_unzip()
    virtualenv_py = os.path.join(TOOLS_FOLDER, "virtualenv.py")
    print '== create LBFORUM_ENV =='
    run('python %s %s' % (virtualenv_py, LBFORUM_ENV))
    do_easy_install()
