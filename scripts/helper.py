#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os, zipfile, subprocess

def unzip(zip_file, obj_folder):
    z = zipfile.ZipFile(zip_file, 'r')
    for f in z.namelist():
        new_filename = os.path.join(obj_folder, f)
        if not os.path.exists(os.path.dirname(new_filename)):
            os.makedirs(os.path.dirname(new_filename))
        if new_filename[-1:][0] not in ('\\', '/'):
            file(new_filename, 'wb').write(z.read(f))

def run(target, **args):
    process = subprocess.Popen(target, shell=True, **args)
    (stdoutput,erroutput) = process.communicate()
    return stdoutput

if __name__ == '__main__':
    print run('dir')
