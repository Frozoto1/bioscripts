#!/usr/bin/env python

'''
==================
input file format:
(from CGmap format file extract CHH and sorted it by Chrom and position)
e.g.:
Chr1    C       1102    CHH     CC      0.50    1       2
Chr1    G       1133    CHH     CT      0.50    1       2
Chr1    C       1136    CHH     CC      0.60    3       5
Chr1    G       1147    CHH     CC      0.50    1       2
Chr1    C       1159    CHH     CA      0.33    2       6
==================
'''

#import sys
import argparse
#import linecache
def find_mCHH_islands(CGmapfile,tile,min_cov,min_chh_num,min_chh_lev):
    tile = int(tile)
    min_cov = int(min_cov)
    min_chh_num = int(min_chh_num)
    min_chh_lev = float(min_chh_lev)
    chh_site_count = 0
    meth_lev_sum = 0
    i = 1
#    pre_chr = linecache.getline(CGmapfile,1).split('\t')[0]
    with open(CGmapfile,'r') as f:
        pre_chr = f.readline().split('\t')[0]
    with open(CGmapfile,'r') as f:
        for eachline in f:
            if eachline != '\n':
                chrom,_,pos,_,_,lev,_,cov = eachline.split('\t')
                pos = int(pos)
                lev = float(lev)
                cov = int(cov)
                if chrom == pre_chr:
                    if pos in range(100*(i-1)+1,100*i+1):
                        if cov >= min_cov:
                            chh_site_count += 1
                            meth_lev_sum = meth_lev_sum + lev
                        else:
                            pass
                    else:
                        if chh_site_count >= min_chh_num:
                            avg_meth_lev = meth_lev_sum/chh_site_count
                            if avg_meth_lev >= min_chh_lev:
                                print('{0}\t{1}\t{2}\t{3}'.format(chrom,(i-1)*100+1,100*i,avg_meth_lev))
                        chh_site_count = 0
                        meth_lev_sum = 0
                        i = pos // 100 + 1
                        if cov >= min_cov:
                            chh_site_count = 1
                            meth_lev_sum = lev
                        else:
                            pass
                else:
                    i = pos // 100 + 1
                    pre_chr = chrom
                    if cov >= min_cov:
                        chh_site_count = 1
                        meth_lev_sum = lev
                    else:
                        pass
            else:
                pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate mCHH islands')
    parser.add_argument('-i',dest='CGmapfile',metavar='CGmapfile',action='store',required=True,help='input file<CGmap format>')
    parser.add_argument('--tile',dest='tile',metavar='tiles',action='store',required=True,default=100,help='tile size<default:100>')
    parser.add_argument('--cov',dest='min_cov',metavar='minimum coverage',action='store',required=True,help='minumum coverage of CHH site')
    parser.add_argument('-n',dest='min_chh_num',metavar='min CHH site num',action='store',required=True,help='minumum mCHH site number of a tile')
    parser.add_argument('--lev',dest='min_chh_lev',metavar='min avg mCHH level of a tile',required=True,help='minumum average mCHH level of a tile')
    parser.add_argument('--version',action='version',version='Find mCHH islands v1.0.0')
    options = parser.parse_args()
    find_mCHH_islands(**vars(options))


