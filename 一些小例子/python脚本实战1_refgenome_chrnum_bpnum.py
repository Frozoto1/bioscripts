#!/usr/bin/env python

'''
This is a module for some genome details.
    Now,it include chromosome number and
    the number of bp per chromosome.
'''



import re
import sys
def details(filepath):
    print('='*20,filepath.split('\\')[-1],'='*20)
    with open (filepath) as f:
        genome = f.read()
        b = re.findall(r'(^>.+)([^>]+)',genome,re.M)
        print('chr num:',len(b))
        print(b)
        for i in range(len(b)):
            chr_bp_num = len(b[i][1].replace("\n",''))
            print('chr',i+1,':',chr_bp_num,'bp')
details(sys.argv[1])





