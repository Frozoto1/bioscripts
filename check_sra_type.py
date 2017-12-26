#!/usr/bin/env python

'''
use for:
批量检测下载的sra文件的类型，SE or PE

'''
import os
import subprocess
from sys import argv

def check_SRA_type(path):
    allfd = os.listdir(path)
    for fn in allfd:
        if os.path.isfile(fn) and '.sra' in fn:
            try:
                contents = subprocess.check_output(["fastq-dump", "-X", "1", "-Z", "--split-spot", fn])
            except subprocess.CalledProcessError as e:
                raise Exception("Error running fastq-dump on", fn)
            if(contents.decode('ascii').count("\n") == 4):
                print(fn,'is SE')
            elif(contents.decode('ascii').count("\n") == 8):
                print(fn,'is PE')
            else:
                raise Exception("Unexpected output from fastq-dump on ", fn)

check_SRA_type(argv[1])
