# for tophat fusion.out
filename="fusions.out"
with open(filename) as inputfile:
    with open(filename+".out",'w') as outfile:
        for itemlist in inputfile:
            item=itemlist.split('\t')[0:5]
            fusion1,fusion2=item[0].split('-')
            chain=list(item[3].replace('r','-').replace('f','+'))
            if int(item[4])>=3 and fusion2!="MT" and fusion1 != "MT":
                towrite=[item[4],fusion1,item[1],chain[0],fusion2,item[2],chain[1]]
                outfile.write('\t'.join(towrite)+"\n")
