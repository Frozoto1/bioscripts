#!/usr/bin/env python

'''
CHH island
==========
tss_tts_file format e.g:
Chr1    LOC_Os01g01010  2903    10817   +

'''


import sys
import re

#chh pattern
chhpattern = re.compile(r'C[ATC][ATC]',re.I)
#定义一些会用到的小函数
def cut3nuc(nucstr):
    list3nuc = []
    nucstr_len = len(nucstr)
    for i in range(nucstr_len):
        if i+3 < nucstr_len:
            list3nuc.append(nucstr[i:i+3])
        else:
            break
    return list3nuc

def change(x):
    if x == 'a' or x =='A':
        return 'T'
    if x == 'g' or x =='G':
        return 'C'
    if x == 'c' or x =='C':
        return 'G'
    if x == 't' or x =='T':
        return 'A'
    if x == 'n' or x == 'N':
        return 'N'

def seqReverse(sequence):
    rev_seq = sequence[::-1]
    a_list = list(map(change,rev_seq))
    rev_string = ''.join(a_list)
    return rev_string

def up_tail_CHH_pt(astring):
    chh_num = 0
#    chg_num = 0
#    cg_num = 0
    astring = astring.upper()
    rev_astring = seqReverse(astring)
    for letter3 in cut3nuc(astring):
        if chhpattern.match(letter3):
            chh_num += 1
        else:
            pass
    return str(chh_num/100)
def dw_tail_CHH_pt(bstring):
    chh_num = 0
    bstring = bstring.upper()
    rev_bstring = seqReverse(bstring)
    for letter3 in cut3nuc(rev_bstring):
        if chhpattern.match(letter3):
            chh_num += 1
        else:
            pass
    return str(chh_num/100)

def chhisland(genome_file,tss_tts_file,flank=2000,window=100):
    flank = int(flank)
    window = int(window)
    num_tail = flank//window
#get genome sequence information
    with open(genome_file,'r') as f:
        genome = f.read()
        gstore = re.findall(r'^>(.+)([^>]+)',genome,re.M)
        gstore = dict(gstore)
        for key in gstore.keys():
            gstore[key] = gstore[key].replace('\n','')
    with open(tss_tts_file,'r') as f:
        for eachline in f:
            chro,geneid,pos1,pos2,strand = eachline.split('\t')
            chrom_seq = gstore[chro]
            tss_chh_percentage = []
            tts_chh_percentage = []
            if strand == '+':
                tss = int(pos1)
                start_tss = tss-flank+1
                #tss_us = range(start_tss,tss+1)
                tts = int(pos2)
                tts_end = tts+flank
                #tts_ds = range(tts,tts_end)
                for i in range(num_tail):
                    tss_chh_percentage.append(up_tail_CHH_pt(chrom_seq[start_tss+window*i:start_tss+window*(i+1)]))
                    tts_chh_percentage.append(up_tail_CHH_pt(chrom_seq[tts+window*i:tts+window*(i+1)]))
            else:
                tss = int(pos2)
                tss_end = tss+flank
                #tss_us = range(tss,tss_end)
                tts = int(pos1)
                start_tts = tts-flank+1
                #tts_ds = range(start_tts,tts+1)
                for j in range(num_tail):
                    tss_seq = chrom_seq[tss+window*j:tss+window*(j+1)]
                    #print(tss_seq)
                    tts_seq = chrom_seq[start_tts+window*j:start_tts+window*(j+1)]
                    tss_chh_percentage.append(dw_tail_CHH_pt(tss_seq))
                    tts_chh_percentage.append(dw_tail_CHH_pt(tts_seq))
                tss_chh_percentage = tss_chh_percentage[::-1]
                tts_chh_percentage = tts_chh_percentage[::-1]
            if [p for p in tss_chh_percentage if float(p) >= 0.25] :
                tss_island = 'true'
            else:
                tss_island = 'false'
            if [q for q in tts_chh_percentage if float(q) >= 0.25]:
                tts_island = 'true'
            else:
                tts_island = 'false'
            print(geneid+'\t'+'\t'.join(tss_chh_percentage)+'\t'+'\t'.join(tts_chh_percentage)+'\t'+tss_island+'\t'+tts_island)
if __name__ == '__main__':
    chhisland(sys.argv[1],sys.argv[2])
    #chhisland('Tigr7.fa','japo_tss_tts.txt')












