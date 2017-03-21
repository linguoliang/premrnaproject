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


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))

def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i FILE.bcf -g FILE.gff3 -o OUTPREFIX'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input segment.out file ')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    parser.add_option('-g', '--gtf', dest='gtf',type="string",default='', help='gtf file')
    parser.add_option('-o', '--output', dest='output', type='string', help='input variation information file')
    parser.add_option('-d','--depth',dest='depth',type='int',default=5,help='depth')
    options, args = parser.parse_args()
    parser.print_help()
    # positional arguments are ignored
    return options,parser


def options_hindler(options,parser):
    if options.gtf=="":
        parser.print_help()
        raise ValueError("GTF is NULL")
    if options.input=="":
        parser.print_help()
        raise ValueError("Input file is NULL")



if __name__ == '__main__':
    options,parser=_parse_args()
    options_hindler()
    printinformations(options,parser)
    GTF_decoding.decodegff()
