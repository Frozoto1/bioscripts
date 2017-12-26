#!/usr/bin/env python
'''
大文件的读取的以使用with打开文件并并逐行读取
'''
import re
with open ('zebrafish_refgenome.fna','r') as f:
    count = 0
    for line in f:
        match = re.match(r'^>.+',line)
        if match:
            print(match.group(0),'\n\n',' '*8,'0123456789'*8)
            count = 0
        else:
            print('%09d'%(count),line.strip())
        count += 1
