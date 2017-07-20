#!/usr/bin/env python3
"""
intersection_with_fusion.py
Created by Guoliang Lin on 2017-04-25
Copyright (c) 2017 Guoliang Lin. All rights reserved.
"""
import sys
import getopt

help_message = '''
This scripts intersect the fusion junctions betweeen the results of star and tophat.
Usage:

'''


def combineGenerator(list1):
    # 生成所有组合
    listr = []
    listr.append('_'.join(list1[0:4]))
    listr.append('_'.join([list1[2], list1[3], list1[0], list1[1]]))
    listr.append('_'.join([list1[0], str(int(list1[1]) + 2), list1[2], list1[3]]))
    listr.append('_'.join([list1[0], list1[1], list1[2], str(int(list1[3]) + 2)]))
    if list1[0] == list1[2]:
        listr.append('_'.join([list1[0], list1[3], list1[2], str(int(list1[1]) + 2)]))
        listr.append('_'.join([list1[0], str(int(list1[3]) + 2), list1[2], list1[1]]))
    return listr


dict1 = {}
dict2 = {}
dict3 = {}
with open(sys.argv[1], 'r') as tophat:
    with open(sys.argv[2], 'r') as star1:
        # with open(sys.argv[3], 'r') as star2:
        with open(sys.argv[3], 'w') as outputfile:
            for item in star1:
                item=item.strip()
                tmp = item.split('\t')
                dict1['_'.join([tmp[1], tmp[2], tmp[4], tmp[5]])] = item
            # for item in star2:
            #     item=item.strip()
            #     tmp = item.split('\t')
            #     di = '_'.join(tmp[1:7])
            #     di2 = '_'.join([tmp[1], tmp[2], tmp[4], tmp[5]])
            #     if di in dict1:
            #         dict2[di2] = dict1[di]
            for item in tophat:
                item=item.strip()
                tmp = item.split('\t')
                di = combineGenerator([tmp[1], tmp[2], tmp[4], tmp[5]])
                for di2 in di:
                    if di2 in dict1:
                        dict3[di2] = dict1[di2]+'\t'+item
                        break
            for key in dict3:
                outputfile.write(dict3[key]+'\n')
