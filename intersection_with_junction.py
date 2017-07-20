#!/usr/bin/env python3
"""
intersection_with_junction.py
Created by Guoliang Lin on 2017-03-07
Copyright (c) 2017 Guoliang Lin. All rights reserved.
"""
import sys
import getopt

help_message='''
This scripts intersect the junctions betweeen the results of star and tophat.
Usage:
      
'''

dict1={}
dict2={}
dict3={}
with open(sys.argv[1],'r') as tophat:
    with open(sys.argv[2],'r') as star1:
        with open(sys.argv[3],'r') as star2:
            with open(sys.argv[4],'w') as outputfile:
                for item in tophat:
                    tmp = item.split('\t')
                    dict1[tmp[0]+str(int(tmp[1])+2)+tmp[2]+tmp[3]]=item
                for item in star1:
                    tmp = item.split('\t')
                    di=tmp[0]+tmp[1]+tmp[2]+tmp[3]
                    if di in dict1:
                        dict2[di]=dict1[di]
                for item in star2:
                    tmp = item.split('\t')
                    di=tmp[0]+tmp[1]+tmp[2]+tmp[3]
                    if di in dict2:
                        dict3[di]=dict2[di]
                for key in dict3:
                    outputfile.write(dict3[key])
