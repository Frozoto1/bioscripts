#!/usr/bin/env python
'''
============================
input file format:
<Chrom> <pos1> <pos2> <meth count> <unmeth count> <methlev> <context>
e.g.:
Chr1    4654787 4654788 0   7   0.0 CHG
Chr1    4654788 4654789 0   6   0.0 CG
============================
output file format:
<startpos> <endpos> <control_avg_methlev> <test_avg_methlev> <diff_lev> <methstats> <sigstats>
============================

USAGE:
python3 script.py <cfile> <tfile> <window> <cov> <wcp> <diffsize> <siglev> <spos> <epos>
cfile:control file
tfile:test file
window:window size
cov:the smallest coverage of every point
wcp:C site of a window that satisfied coverage/window
diffsize:the difference of two samples average methylation level on the same window
        average methylation = all_meth_count/(all_meth_count+all_unmeth_count)
siglev:significant level
spos:start position
epos:end position
===========================
others:
test file methlev > control file methlev --> up

+++++++++++++++
by.chengjiawen
2017/11/2 modified
+++++++++++++++
'''
from sys import argv
#t-test usage
try:
    from scipy.stats import ttest_ind
except ImportError :
    sys.stderr.write("Scipy package can not find!")
    exit(-1)
#fisher_exact test usage:
#from scipy.stats import fisher_exact
#fisher_exact([[a1,a2],[b1,b2]])
def find_dmr(cfile,tfile,window,cov,wcp,diffsize,siglev,spos,epos):
    window = int(window)
    cov = int (cov)
    wcp = float(wcp)
    diffsize = float(diffsize)
    siglev = float(siglev)
    spos = int(spos)
    epos = int(epos)
    cstore = {}
    tstore = {}
    dmr_err_log = 'dmr_process.log'
#read input file
    with open(cfile,'r') as f:
        for eachline in f:
            if eachline != '\n':
                _,pos,_,mcount,unmcount,_,_ = eachline.split('\t')
                cstore[int(pos)] = [int(mcount),int(unmcount)]
            else:
                pass
    with open(tfile,'r') as g:
        for gachline in g:
            if gachline != '\n':
                _,gpos,_,gmcount,gunmcount,_,_ = gachline.split('\t')
                tstore[int(gpos)] = [int(gmcount),int(gunmcount)]
            else:
                pass
    with open(dmr_err_log,'a') as f:
        print('read input file completely!\n',file=f)
#count window number
    region = epos-spos+1
    if region >= window:
        if region % window == 0:
            winum = int(region/window)
        else:
            winum = int(region/window + 1)
    else:
        print('error!your region less then your window')
    with open(dmr_err_log,'a') as f:
        print('count window number completely\n',file=f)
#caculate
    knownCsite = set(cstore.keys())
    outputdetail = ''#store final output details
    for i in range(winum):
        startwin = spos+window*i
        endwin = window*(i+1)+spos
        c_site = set(range(startwin,endwin)) & knownCsite
        c_sitecount = len(c_site)
        con_cov_pass_csite = []
        test_cov_pass_csite = []
        if c_sitecount >= wcp*window:
            for apos in c_site:
                con_methcov = cstore[apos][0]
                con_unmethcov = cstore[apos][1]
                test_methcov = tstore[apos][0]
                test_unmethcov = tstore[apos][1]
                con_cov = con_methcov + con_unmethcov
                test_cov = test_methcov + test_unmethcov
                if con_cov >= cov:
                    con_cov_pass_csite.append(apos)
                else:
                    pass
                if test_cov >= cov:
                    test_cov_pass_csite.append(apos)
                else:
                    pass
            if len(con_cov_pass_csite)/window >= wcp and len(test_cov_pass_csite)/window >= wcp:
                con_allmeth = sum(cstore[x][0] for x in con_cov_pass_csite)
                con_allunmeth = sum(cstore[y][1] for y in con_cov_pass_csite )
                test_allmeth = sum(tstore[x][0] for x in test_cov_pass_csite)
                test_allunmeth = sum(tstore[y][1] for y in test_cov_pass_csite)
                con_win_avg_methlev = round(con_allmeth/(con_allmeth+con_allunmeth),5)
                test_win_avg_methlev = round(test_allmeth/(test_allmeth+test_allunmeth),5)
                diff_lev = test_win_avg_methlev - con_win_avg_methlev
                for_p = [[con_allmeth,con_allunmeth],[test_allmeth,test_allunmeth]]
                if abs(diff_lev) >= diffsize:
                    if diff_lev <= 0:
                        methstats = 'down'
                    else:
                        methstats = 'up'
                    _,pvalue = stats.fisher_exact(for_p)
                    if pvalue <= siglev:
                        sigstats = 'Sig'
                        outputdetail = str(startwin)+'\t'+str(endwin-1)+'\t'+str(con_win_avg_methlev)+'\t'+str(test_win_avg_methlev)+'\t'+str(abs(diff_lev))+'\t'+methstats+'\t'+sigstats+'\n'
                        print(outputdetail)
                    else:
                        with open(dmr_err_log,'a') as f:
                            print(str(startwin)+'\t'+str(endwin)+'\t'+'Insig',file=f)
                else:
                    with open(dmr_err_log,'a') as f:
                        print(str(startwin)+'\t'+str(endwin)+'\t'+'Diff lev<'+str(diffsize),file = f)
            else:
                with open(dmr_err_log,'a') as f:
                    print(str(startwin)+'\t'+str(endwin)+'\t'+'wcp small',file =f)
        else:
            with open(dmr_err_log,'a') as f:
                print(str(startwin)+'\t'+str(endwin)+'\t'+'Csite small',file = f)

find_dmr(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8],argv[9])





