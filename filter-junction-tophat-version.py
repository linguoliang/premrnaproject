#!/bin/env python3
# coding=utf-8
# this file is for filtering junction from tophat junction.bed 
# The junction will be filter when the scores is less than 1 and the overhang is less than 20
import sys

with open(sys.argv[1]) as inputfile:
    with open(sys.argv[1]+'a','w') as outfile:
        inputfile.readline()
        for element in inputfile:
            tmp=element.split('\t')
            depth=int(tmp[4])
            overhangleft=int(tmp[10].split(',')[0])
            overhangright=int(tmp[10].split(',')[1])
            if depth >=3 and overhangleft>=20 and overhangright>=20:
                outfile.write(element)
