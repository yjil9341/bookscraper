import os


def filename_extractor(path):
    lst = []
    files = os.listdir(path)
    for filename in files: lst.append(filename)
    return lst

categorylist =  filename_extractor('good_isbns/')
isbns = []

for category in categorylist:
    print category
    print "Opening {}".format(category)
    f = open('good_isbns/' + category,'r')
    isbns_single = f.read().strip().split()
    isbns = isbns + isbns_single
    print "ISBN scraped and saved"

isbns = list(set(isbns))
mainf = open('isbns.txt','w')
for isbn in isbns:
    mainf.write(isbn + '\n')
mainf.close()
    

