#!/bin/env python3
# coding=utf-8
# this file is for filtering junction from tophat junction.bed 
# The junction will be filter when the scores is less than 3 and the overhang is less than 20
#Users can also changes the scores just add the score
import sys
pre_depth=3
pre_overhang=20
if len(sys.argv)>=3:
    pre_depth=int(sys.argv[2])
    if len(sys.argv)>=4:
         pre_overhang=int(sys.argv[3])
with open(sys.argv[1]) as inputfile:
    with open(sys.argv[1]+'a','w') as outfile:
        for element in inputfile:
            tmp=element.split('\t')
            overhang=int(tmp[8])
            depth= int(tmp[6])
            if depth >=pre_depth and overhang >= pre_overhang :
                if tmp[3]=='1':
                    string='\t'.join([tmp[0],tmp[1],tmp[2],'+',tmp[6]])
                else:
                    string='\t'.join([tmp[0],tmp[1],tmp[2],'-',tmp[6]])
                outfile.write(string+'\n')
