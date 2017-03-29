#!/usr/bin/env python3
# coding=utf-8
"""
This scripts is for detect patterns of the transcription.

"""
__author__ = 'Guoliang Lin'
Softwarename = 'detect junctions in tophat'
version = '0.0.1'
bugfixs = ''
__date__ = '2017-03-21'
import optparse
import time
import GTF_decoding

def printinformations():
    print("%s software version is %s in %s" % (Softwarename, version, __date__))
    print(bugfixs)
    print('Starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
class Junction:
    def __init__(self,listitem):
        self.scaffold=listitem[0]
        self.start=int(listitem[1])
        self.end=int(listitem[2])
        self.chain=listitem[3]
        self.depth=listitem[4]
        self.isnormal=0
        self.istranssplice=False
        self.transspan=0

    def istranscpliced(self,isnormal,flag):
        self.isnormal=isnormal
        if flag>0:
            self.istranssplice=True
        self.transspan=flag


class Normaljunction:
    def __init__(self):
        """
        normaljucntion 为正常的junction,GTF文件中可以找到的
        noveljunction 新生的junction， GTF文件中找不到的
        transplicead 可能发生了transsplice的junction,而且为临近的序列
        transplicefa 可能发生了transsplice的junction,而且为非临近的序列
        """
        self.normaljucntion=[]
        self.noveljunction=[]
        self.transplicead=[]
        self.transplicefa=[]
        self.length=[0,0,0,0]

    def addnormal(self,junc):
        self.normaljucntion.append(junc)

    def addnovel(self,junc):
        self.noveljunction.append(junc)

    def addtransad(self,junc):
        self.transplicead.append(junc)

    def addtransfa(self,junc):
        self.transplicefa.append(junc)

    def addjunc(self,junc):
        assert isinstance(junc,Junction)
        if junc.isnormal==2:
            self.addnormal(junc)
        elif junc.isnormal==1:
            self.addnovel(junc)
        elif junc.transspan==1:
            self.addtransad(junc)
        else:
            self.addtransfa(junc)

    def returnlength(self):
        self.length[0]=len(self.normaljucntion)
        self.length[1]=len(self.noveljunction)
        self.length[2]=len(self.transplicead)
        self.length[3]=len(self.transplicefa)
        return self.length

    def parsertostring(self,junc,c='\t'):
        assert isinstance(junc,Junction)
        m=map(str,[junc.scaffold,junc.start,junc.end,junc.chain,junc.depth,junc.isnormal,junc.transspan])
        string=c.join(m)
        return string

    def writejunction(self,prefix,postfix,listitem):
        if not (prefix=="" or prefix==None):
            prefix=prefix+"_"
        with open(prefix+postfix+".txt",'w') as outfile:
            for junc in listitem:
                tmp=self.parsertostring(junc)
                outfile.write(tmp+'\n')

    def writetodisk(self,prefix):
        self.writejunction(prefix,"normal",self.normaljucntion)
        self.writejunction(prefix,"novel",self.noveljunction)
        self.writejunction(prefix,"transad",self.transplicead)
        self.writejunction(prefix,"transfa",self.transplicefa)

class Fusionjunction(Junction):
    def __init__(self,listitem):
        Junction.__init__(self,listitem)


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))

def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -j JUNCTION -g FILE.gff3 -o OUTPREFIX'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input junction file ')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    parser.add_option('-g', '--gtf', dest='gtf',type="string",default='', help='gtf file')
    parser.add_option('-o', '--output', dest='output', type='string',default='', help='output prefix')
    parser.add_option('-j','--junction',dest='junction',type='int',default=0,help='junction type, 0 is normal type,1 for fusion jucntions')
    options, args = parser.parse_args()
    # parser.print_help()
    # positional arguments are ignored
    return options,parser


def options_hindler(options,parser):
    if options.gtf=="":
        parser.print_help()
        raise ValueError("GTF is NULL")
    if options.input=="":
        parser.print_help()
        raise ValueError("Input file is NULL")

def normaljunction(filename,prefix,Njunction,):
    with open(filename) as inputfile:
        for element in inputfile:
            element=element.strip()
            listitem=element.split('\t')
            junc=Junction(listitem)
            flag,isnormal=GTF_decoding.classfynormaljunction(junc.start+1,junc.end+1,junc.scaffold)
            junc.istranscpliced(isnormal,flag)
            Njunction.addjunc(junc)
        Njunction.writetodisk(prefix)


if __name__ == '__main__':
    Njunction=Normaljunction()
    options,parser=_parse_args()
    options_hindler(options,parser)
    printinformations()
    GTF_decoding.decodegtf(options.gtf)
    if options.junction==0:
        normaljunction(options.input,options.output,Njunction)

