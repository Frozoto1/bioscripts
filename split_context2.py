#!/usr/bin/env python

'''
===================================
input file format:
Chr1    1001    +   0   0   CHH CTA
Chr1    1006    +   0   0   CHH CCC
===================================
output file format:
Chr1    23423   23424   7   1   0.875   CG
Chr1    23424   23425   11  0   1.0     CG
==================================
USAGE:
python3 script.py <contextfile> <startposition> <endposition> <tagname>

'''

import sys
import os

def extra(contextfile,spos,epos,tag):
    cgfile = 'CG_'+tag+'_'+contextfile
    chgfile = 'CHG_'+tag+'_'+contextfile
    chhfile = 'CHH_'+tag+'_'+contextfile
    allCfile = 'allC_'+tag+'_'+contextfile
    os.mknod(cgfile)
    os.mknod(chgfile)
    os.mknod(chhfile)
    os.mknod(allCfile)
    spos = int(spos)
    epos = int(epos)
    with open(contextfile,'r') as f:
        cgcontent = ''
        chgcontent = ''
        chhcontent = ''
        allcontent = ''
        for eachline in f:
            chrom,pos,_,methCount,unmethCount,context,_ = eachline.split("\t")
            if int(pos) < spos:
                continue
            elif int(pos) >= spos and int(pos) <= epos:
                methCount = int(methCount)
                unmethCount = int(unmethCount)
                if methCount == 0 and unmethCount == 0:
                    methlev = '0'
                else:
                    methlev = round(methCount/(methCount+unmethCount),4)
                    methlev = str(methlev)
                alline = chrom+'\t'+pos+'\t'+str(int(pos)+1)+'\t'+str(methCount)+'\t'+str(unmethCount)+'\t'+methlev+'\t'+context+'\n'
                allcontent = allcontent + alline
                if context == "CG":
                    cgline = chrom+'\t'+pos+'\t'+str(int(pos)+1)+'\t'+str(methCount)+'\t'+str(unmethCount)+'\t'+methlev+'\t'+context+'\n'
                    cgcontent = cgcontent + cgline
                elif context == "CHG":
                    chgline = chrom+'\t'+pos+'\t'+str(int(pos)+1)+'\t'+str(methCount)+'\t'+str(unmethCount)+'\t'+methlev+'\t'+context+'\n'
                    chgcontent = chgcontent + chgline
                elif context == "CHH":
                    chhline = chrom+'\t'+pos+'\t'+str(int(pos)+1)+'\t'+str(methCount)+'\t'+str(unmethCount)+'\t'+methlev+'\t'+context+'\n'
                    chhcontent = chhcontent + chhline
                else:
                    pass
            else:
                break
        with open(cgfile,'w') as f:
            print(cgcontent,file=f)
        with open(chgfile,'w') as f:
            print(chgcontent,file=f)
        with open(chhfile,'w') as f:
            print(chhcontent,file=f)
        with open(allCfile,'w') as f:
            print(allcontent,file=f)
extra(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
