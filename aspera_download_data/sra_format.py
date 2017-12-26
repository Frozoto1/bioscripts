#!/usr/bin/env python3

import sys
import os
def sra_format(sra_list_name):
    with open(sra_list_name,'r') as f:
        data = f.read().split('\n')
    alist = []
    for i in data:
        if 'DRR' in i:
            path='/sra/sra-instant/reads/ByRun/sra/DRR/{0}/{1}/{2}'.format(i[0:6],i,i+".sra")
        elif 'ERR' in i:
            path='/sra/sra-instant/reads/ByRun/sra/ERR/{0}/{1}/{2}'.format(i[0:6],i,i+".sra")
        elif 'SRR' in i:
            path='/sra/sra-instant/reads/ByRun/sra/SRR/{0}/{1}/{2}'.format(i[0:6],i,i+".sra")
        else:
            pass
        alist.append(path)
    if os.path.exists('sra_download_path.txt'):
        os.remove('sra_download_path.txt')
        os.mknod('sra_download_path.txt')
    else:
        os.mknod('sra_download_path.txt')
    with open ('sra_download_path.txt','w') as f:
        for j in alist:
            f.write(j+"\n")
sra_format(sys.argv[1])
