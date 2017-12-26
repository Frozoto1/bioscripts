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
cgpattern = re.compile(r'CG',re.I)
chgpattern = re.compile(r'C[ATC]G',re.I)
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

def top_tail_pt(astring):
    chh_num = 0
    chg_num = 0
    cg_num = 0
    astring = astring.upper()
    for letter3 in cut3nuc(astring):
        if chhpattern.match(letter3):
            chh_num += 1
        elif cgpattern.match(letter3):
            cg_num += 1
        elif chgpattern.math(letter3):
            chg_num += 1
        else:
            pass
    return [str(cg_num/100),str(chg_num/100),str(chh_num/100)]
def bot_tail_pt(bstring):
    chh_num = 0
    cg_num = 0
    chg_num = 0
    bstring = bstring.upper()
    rev_bstring = seqReverse(bstring)
    for letter3 in cut3nuc(rev_bstring):
        if chhpattern.match(letter3):
            chh_num += 1
        elif cgpattern.match(letter3):
            cg_num += 1
        elif chgpattern.match(letter3):
            chg_num += 1
        else:
            pass
    return [str(cg_num/100),str(chg_num/100),str(chh_num/100)]


def count_cp(genome_file,tss_tts_file,flank=2000,window=100):
    flank = int(flank)
    window = int(window)
    num_tail = 2*flank//window
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
            tss_cg_percentage = []
            tss_chg_percentage = []
            tts_chh_percentage = []
            tts_cg_percentage = []
            tts_chg_percentage = []
            tss = int(pos1)
            up_tss = tss-flank+1
            tts = int(pos2)
            up_tts = tts-flank+1
            if strand == '+':
                for i in range(num_tail):
                    tss_seq = chrom_seq[up_tss+window*i:up_tss+window*(i+1)]
                    tts_seq = chrom_seq[up_tts+window*i:up_tts+window*(i+1)]
                    tss_cg_percentage.append(top_tail_pt(tss_seq)[0])
                    tss_chg_percentage.append(top_tail_pt(tss_seq)[1])
                    tss_chh_percentage.append(top_tail_pt(tss_seq)[2])
                    tts_cg_percentage.append(top_tail_pt(tts_seq)[0])
                    tts_chg_percentage.append(top_tail_pt(tts_seq)[1])
                    tts_chh_percentage.append(top_tail_pt(tts_seq)[2])
            else:
                for j in range(num_tail):
                    tss_seq = chrom_seq[up_tss+window*j:up_tss+window*(j+1)]
                    tts_seq = chrom_seq[up_tts+window*j:up_tts+window*(j+1)]
                    tss_cg_percentage.append(bot_tail_pt(tss_seq)[0])
                    tss_chg_percentage.append(bot_tail_pt(tss_seq)[1])
                    tss_chh_percentage.append(bot_tail_pt(tss_seq)[2])
                    tts_cg_percentage.append(bot_tail_pt(tts_seq)[0])
                    tts_chg_percentage.append(bot_tail_pt(tts_seq)[1])
                    tts_chh_percentage.append(bot_tail_pt(tts_seq)[2])
                tss_cg_percentage = tss_cg_percentage[::-1]
                tss_chg_percentage = tss_chg_percentage[::-1]
                tss_chh_percentage = tss_chh_percentage[::-1]
                tts_cg_percentage = tts_cg_percentage[::-1]
                tts_chg_percentage = tts_chg_percentage[::-1]
                tts_chh_percentage = tts_chh_percentage[::-1]
            with open ('cg_percentage.txt','at') as f:
                print(geneid+'\t'+'\t'.join(tss_cg_percentage)+'\t'+'\t'.join(tts_cg_percentage),file=f)
            with open ('chg_percentage.txt','at') as f:
                print(geneid+'\t'+'\t'.join(tss_chg_percentage)+'\t'+'\t'.join(tts_chg_percentage),file=f)
            with open('chh_percentage.txt','at') as f:
                print(geneid+'\t'+'\t'.join(tss_chh_percentage)+'\t'+'\t'.join(tts_chh_percentage),file=f)

if __name__ == '__main__':
    count_cp(sys.argv[1],sys.argv[2])
    #count_cp('Tigr7.fa','japo_tss_tts.txt')













