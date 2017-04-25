file="fusions.out.out"
m=list(range(1,23))
m.append('X')
m.append('Y')
m.append('x')
m.append('y')
chrome=list(map(str,m))
with open(file) as inputfile:
    with open(file+".out",'w') as outfile:
        for element in inputfile:
            itemlist=element.split()
            if itemlist[1] in chrome and itemlist[4] in chrome and int(itemlist[0])>=3:
                outfile.write('\t'.join(itemlist)+'\n')