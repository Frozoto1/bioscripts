#!/usr/bin env python

'''
DNA sequence reverse

'''


def change(x):
    if x == 'a' or x =='A':
        return 'T'
    if x == 'g' or x =='G':
        return 'C'
    if x == 'c' or x =='C':
        return 'G'
    if x == 't' or x =='T':
        return 'A'

def seqReverse(sequence):
    rev_seq = sequence[::-1]
    a_list = list(map(change,rev_seq))
    rev_string = ''.join(a_list)

    print("The reverse complementary sequence(5'-->3') is :",rev_string)

yourseq = input("Input your DNA seq(5'-->3'):")
seqReverse(yourseq)


