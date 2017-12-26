#!/usr/bin/env python
''' 读取每条染色体前后1000bp序列
'''
import re
def details(filepath):
    print('='*20,filepath.split('\\')[-1],'='*20)
    with open (filepath) as f:
        genome = f.read()
        b = re.findall(r'(^>.+?chromosome [0-9] sequence)([^>]+)',genome,re.M)
        c = len(b)
        print('chr num:',c)
        store_dict = {}
        store_list = []
        for i in range(c):
            str_no_n = b[i][1].replace("\n",'')
            chr_bp_num = len(str_no_n)
            print('chr',i+1,':',chr_bp_num,'bp')
            key_name = 'chr'+str(i+1)
            q = str_no_n[:1000]
            h = str_no_n[chr_bp_num-1000:]
            store_list.append(q)
            store_list.append(h)
            store_dict[key_name] = store_list
            store_list = []
    return [store_dict,c]
def deal(mystore):
    myformat = "{0:<2}{1:2}"
    for j in range(mystore[1]):
        ky = 'chr'+ str(j + 1)
        my_qian_string = mystore[0][ky][0]
        print('='*22,ky,' Before 1000bp','='*22)
        print('   ','0123456789'*5)
        k = 0
        while k < 20:
            print(myformat.format(str(k+1),'>'),end='')
            print(my_qian_string[50*k:50*(k+1)])
            k += 1
        my_hou_string = mystore[0][ky][1]
        print('='*22,ky,' After 1000bp','='*22)
        print('   ','0123456789'*5)
        m = 0
        while m < 20:
            print(myformat.format(str(m+1),'>'),end='')
            print(my_hou_string[50*m:50*(m+1)])
            m += 1

if __name__ =='__main__':
    filepath = r'G:\at_genome\GCF_000001735.3_TAIR10_genomic.fna'
    mystore = details(filepath)
    deal(mystore)

