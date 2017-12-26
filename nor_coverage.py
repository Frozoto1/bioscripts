#!/usr/bin/env python

'''
=====================================
input file format:
<chrom> <startpos> <endpos> <coverage>
e.g.:
Chr1    0   2943    0
Chr1    2943    2974    1
Chr1    2974    2978    2
====================================
output file format:
<normalized coverage>

'''
import sys
from collections import OrderedDict
def nor_coverage(filename,all_mapped_reads,chromo,start,end):
    start = int(start)
    end = int(end)
    nor_num = round(1000000/int(all_mapped_reads),5)
    store = OrderedDict()
    with open(filename,'r') as f:
        for eachline in f:
            chrom,spos,epos,cov = eachline.split('\t')
            spos = int(spos)
            epos = int(epos)
            cov = int(cov)
            if chrom != chromo:
                continue
            else:
                if epos < start:
                    continue
                elif spos < start and epos >= start:
                    nor_cov = round(cov*nor_num,6)
                    store[start] = [epos,nor_cov]
                elif spos >= start and epos < end:
                    nor_cov = round(cov*nor_num,6)
                    store[spos] = [epos,nor_cov]
                elif spos <= end and epos >= end:
                    nor_cov = round(cov*nor_num,6)
                    store[spos] = [end+1,nor_cov]
                else:
                    break
    for key in store.keys():
        pend = store[key][0]
        pcov = store[key][1]
        for i in range(key,pend):
            print(pcov)
nor_coverage(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])



