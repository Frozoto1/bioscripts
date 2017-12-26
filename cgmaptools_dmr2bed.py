#!/usr/bin/env python

import gzip
import sys

def dmr2bed(gzfile,lev):
    lev = float(lev)
    with gzip.open(gzfile,'rt') as f:
        for eachline in f:
            chro,spos,epos,_,pvalue,c_methlev,t_methlev,_ = eachline.split('\t')
            t_methlev = float(t_methlev)
            c_methlev = float(c_methlev)
            pvalue = float(pvalue)
            if pvalue < lev:
                if t_methlev > c_methlev:
                    dmr_stat = 'hyper-DMR'
                    print('%s\t%s\t%s\t%s'%(chro,spos,epos,dmr_stat))
                else:
                    dmr_stat = 'hypo-DMR'
                    print('%s\t%s\t%s\t%s'%(chro,spos,epos,dmr_stat))
            else:
                pass

dmr2bed(sys.argv[1],sys.argv[2])
