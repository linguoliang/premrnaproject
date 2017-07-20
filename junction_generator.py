#!/usr/bin/env python3
#  coding=utf-8
__author__ = 'Guoliang Lin'
Softwarename = "junction_generator"
version = '0.0.1'
bugfixs = ''
__date__ = "2017/6/26"
import optparse
import time
from functools import reduce

GTFDict = {}
JunctionList = []


def printinformations():
    print("%s software version is %s in %s" % (Softwarename, version, __date__))
    print(bugfixs)
    print('Starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


class GTFfile:
    def __init__(self, listitem):
        self.GeneID = ''
        self.TranscriptID = ''
        self.ExonStart = int(listitem[3]) - 1
        self.ExonEnd = int(listitem[4]) + 1
        self.Scaffold1 = listitem[0]
        self.Fpkm = []
        self.Chain = listitem[6]
        self.Getinfo(listitem[8])

    def Getinfo(self, info):
        tmp = info.split('; ')
        self.GeneID=tmp[0].split(' ')[1].replace('"', '')
        self.TranscriptID=tmp[1].split(' ')[1].replace('"', '')
        mm=tmp[3].split(' ')[1]
        self.Fpkm=float(tmp[3].split(' ')[1].replace('"', ''))

class Junction:
    def __init__(self,listitem:list) -> None:
        """
        :param listitem:list [scaffold,pos,chain,depth]
        
        """
        super().__init__()
        self.GeneID=[]
        self.Scaffold=listitem[0]
        self.Pos=int(listitem[1])
        self.Chain=listitem[2]
        # self.Depth=listitem[3]
        self.Fpkm=[]
        self.TranscriptID=[]

    def AddGeneID(self,GeneID:str):   # type: (Junction, str) -> None
        if GeneID not in self.GeneID:
            self.GeneID.append(GeneID)

    def AddTranscriptID(self,TranscriptID:str):    # type: (Junction, str) -> None
        if TranscriptID not in self.TranscriptID:
            self.TranscriptID.append(TranscriptID)

    def AddFpkm(self,Fpkm:float):
        self.Fpkm.append(Fpkm)

    def ToString(self):  # type: (Junction) -> str
        String = '\t'.join([self.Scaffold, str(self.Pos), self.Chain, '@'.join(self.GeneID), str((len(self.Fpkm) and max(self.Fpkm)) or "0"),
                            str((len(self.Fpkm) and reduce(lambda x,y:x+y,self.Fpkm)) or "0")])
        return String


class JunctionCombie:
    def __init__(self, listitem):
        self.JunctionS=Junction(listitem)
        self.JunctionE=Junction(listitem[3:])

    def AddGeneID(self, m: list, GeneId):
        if GeneId not in m:
            m.append(GeneId)

    def AddTranscriptID(self, m: list, TranscriptID):
        if TranscriptID not in m:
            m.append(TranscriptID)

    def ToString(self):
        String = '\t'.join([self.JunctionS.ToString(),self.JunctionE.ToString()])
        return String

    def Iscontain(self,GTFitem: GTFfile, Junctionitem: Junction):
        if GTFitem.ExonStart <= Junctionitem.Pos <= GTFitem.ExonEnd:
            Junctionitem.AddGeneID(GTFitem.GeneID)
            Junctionitem.AddTranscriptID(GTFitem.TranscriptID)
            Junctionitem.Fpkm.append(GTFitem.Fpkm)


def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i junctionfile  -g gtffile -o OUTPREFIX'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input junction file ')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    parser.add_option('-g', '--gtf', dest='gtf', help='gtf file')
    parser.add_option('-o', '--output', dest='output', type='string', help='input variation information file')
    parser.add_option('-d', '--depth', dest='depth', type='int', default=5, help='depth')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


if __name__ == '__main__':
    options = _parse_args()
    with open(options.gtf) as gtffile:
        with open(options.input) as junctionfile:
            with open(options.output, 'w') as outputfile:
                for item in gtffile:
                    item = item.strip()
                    itemlist = item.split('\t')
                    assert isinstance(itemlist, list)
                    if itemlist[2] == 'exon':
                        tmpgtf = GTFfile(itemlist)
                        if tmpgtf.Scaffold1 in GTFDict:
                            GTFDict[tmpgtf.Scaffold1][tmpgtf.Chain].append(tmpgtf)
                        else:
                            GTFDict[tmpgtf.Scaffold1] = {}
                            GTFDict[tmpgtf.Scaffold1]['-'] = []
                            GTFDict[tmpgtf.Scaffold1]['+'] = []
                            GTFDict[tmpgtf.Scaffold1]['.'] = []
                            GTFDict[tmpgtf.Scaffold1][tmpgtf.Chain].append(tmpgtf)
                for key in GTFDict.keys():
                    GTFDict[key]['+'].sort(key=lambda x: (x.ExonStart, x.ExonEnd))
                    GTFDict[key]['-'].sort(key=lambda x: (x.ExonStart, x.ExonEnd))
                for item in junctionfile:
                    itemlist = item.split('\t')
                    junctionlist=[itemlist[0],itemlist[1],itemlist[3],itemlist[0],itemlist[2],itemlist[3]]
                    tmpjunction = JunctionCombie(junctionlist)
                    for Gtfitem in GTFDict[tmpjunction.JunctionS.Scaffold][tmpjunction.JunctionS.Chain]:
                        tmpjunction.Iscontain(Gtfitem, tmpjunction.JunctionS)
                    for Gtfitem in GTFDict[tmpjunction.JunctionE.Scaffold][tmpjunction.JunctionE.Chain]:
                        tmpjunction.Iscontain(Gtfitem, tmpjunction.JunctionE)
                    string = tmpjunction.ToString()
                    outputfile.write(string + '\n')
