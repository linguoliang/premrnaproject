# coding=utf-8
__author__ = 'Guoliang Lin'
Softwarename = "filter_by_fkpm"
version = '0.0.1'
bugfixs = ''
__date__ = "2017/6/21"
import optparse
import time


def printinformations():
    print("%s software version is %s in %s" % (Softwarename, version, __date__))
    print(bugfixs)
    print('Starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i Gtf -o OUTPREFIX'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input segment.out file ')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    # parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='input variation information file')
    # parser.add_option('-d', '--depth', dest='depth', type='int', default=5, help='depth')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


if __name__ == '__main__':
    options=_parse_args()
    with open(options.input,'r') as inputfile:
        with open(options.output,'w') as outfile:
            for item in inputfile:
                assert isinstance(item,str)
                listitems=item.split('\t')
                if listitems[2]=='exon':
                    tmp = listitems[8].split(';')
                    fpkm = float(tmp[3].split(' ')[2].replace('"', ''))
                    if fpkm >=0.3:
                        outfile.write(item)