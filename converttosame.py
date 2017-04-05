# for tophat fusion.out
filename=""
with open(filename) as inputfile:
    for itemlist in inputfile:
        item=itemlist.split('\t')[0:5]
        fusion1,fusion2=item[0].split('-')
