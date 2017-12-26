#!/usr/bin/env python

import sys
def cal(file):
    #filename = file[:-4]
    count = 0
    asum = 0
    i = 1
    with open(file,'r') as f:
        pre_chr = f.readline().split('\t')[0]
    with open(file,'r') as f:
            for eachline in f:
                if eachline != '\n':
                    chrom,_,pos,_,_,lev,_,_ = eachline.split('\t')
                    pos = int(pos)
                    lev = float(lev)
                    if chrom == pre_chr:
                        if pos <= 1000000*i:
                            count += 1
                            asum = asum + lev
                        else:
                            print(asum/count,end='\t')
                            count = 0
                            asum = lev
                            i += 1
                    else:
                        print(pre_chr)
                        i = 1
                        pre_chr = chrom
                else:
                    pass
cal(sys.argv[1])
