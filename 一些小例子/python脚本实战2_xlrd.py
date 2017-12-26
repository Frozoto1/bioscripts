#!/usr/bin/env python

import xlrd
    data = xlrd.open_workbook('test.xlsx')
    refgenome_table = data.sheets()[0]
    reads_table = data.sheets()[1]
    print('='*20,'Start','='*20)
    g_rows = refgenome_table.nrows
    r_rows = reads_table.nrows

    g = []
    r = []
    for i in range(g_rows):
        g.append(refgenome_table.row_values(i))
    for j in range(r_rows):
        r.append(reads_table.row_values(j))
    c_gene = 0
    c_promoter = 0
    c_intergenic =0
    for ir in r:
        print('=',end='')
        for ig in g:
            if ir[0] == ig[0]:
                a = range(int(ig[1]),int(ig[2])+1)
                b = range(int(ig[1])-1000,int(ig[1]))
                if int(ir[1]) in a:
                    c_gene += 1
                if int(ir[1]) in b:
                    c_promoter += 1
    c_intergenic = r_rows - c_promoter - c_gene
    print('\nIn gene region:{0}\nIn Promoter region:{1}\nIn\
    intergenic region:{2}'.format(c_gene,c_promoter,c_intergenic))


