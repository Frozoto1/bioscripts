#!/usr/bin/env python

import sys
import os
def every_point(spos,epos):
    allfile = os.listdir('./')
    spos = int(spos)
    epos = int(epos)
    store = {}
    csvcol = ''
    for file in allfile:
        if file.endswith('con.txt'):
            with open(file,'r') as f:
                for eachline in f:
                    _,pos,_,_,_,methlev,_ = eachline.split("\t")
                    pos = int(pos)
                    if pos < spos:
                        continue
                    elif pos>= spos and pos<=epos:
                        store[pos] = methlev
                    else:
                        break
            for i in range(spos,epos+1):
                if i in store.keys():
                    csvcol = csvcol+store[i]+'\n'
                else:
                    csvcol = csvcol+'0\n'
            newfilename = file.split('.')[0]+'.csv'
            with open(newfilename,'w') as f:
                print(csvcol,file=f)
            csvcol = ''
            store = {}
        else:
            pass
every_point(sys.argv[1],sys.argv[2])
