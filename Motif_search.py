#!/usr/bin/env python

import sys
import re

myformat = "{:<12}{:<12}{:<30}"

def getChrbase(filepath):
    with open (filepath,'r') as f:
        genome = f.read()
        g_list = re.findall(r'(>Chr\d{1,2}\n)([atcgATCGN\n]+)',genome,re.M)
        print(g_list[0][1][1110:1140])
        #g_list列表中每个元组包含每条染色体的头信息文本和染色体的碱基序列文本
    return g_list

def deal(x):
    return [x.span(),x.group(0)]

def searchMotif(mylist):
    amotif = r'[acg][cg][ctg][t][gt][a][at][acgt]{4}[ctg][atcg][atg][cag][ct][cta][cg][act][at][tac]'
    l_mylist = len(mylist)
    for i in range(l_mylist):
        print('='*20,'Chr ',i+1,'Motif Status','='*20)
        print(myformat.format('START','END','DETAILS'))
        mybasestring = mylist[i][1]
        mystring = mybasestring.replace('\n','')
        b = re.finditer(amotif,mystring,re.I&re.M)
        chr_motif_details = list(map(deal,b))
        l_chr = len(chr_motif_details)
        for j in chr_motif_details:
            print(myformat.format(j[0][0]+1,j[0][1],j[1]))
        print('-'*10,'TOTAL:',l_chr,'-'*10)

def main():
    myfile = sys.argv[1]
    mylist = getChrbase(myfile)
    searchMotif(mylist)
main()




