import sys
import os
import logging

infile = sys.argv[1]
outfile = sys.argv[2]
colchar = "\t"


logging.basicConfig(level=logging.INFO)

logging.info("Reading %s into %s transposed" % (infile, outfile))

rowcount=0
colcount=0

data = None
with open(infile, "r") as f:
    data = [ x.split(colchar) for x in f.read().strip().split("\n")]

rowcount = len(data)
colcount = len(data[0])

#PP(data)
ndata = []

# for row in range(0, rowcount):
#     for col in range(0, colcount):
#         print(row, col)


for col in range(0, colcount):
    ndata.append(list(range(0, rowcount)))


for row in range(0, rowcount):
    for col in range(0, colcount):
        ndata[col][row] = data[row][col]


#print("*"*80)
#PP(ndata)

with open(outfile, 'w') as f:
    for row in ndata:
        f.write(colchar.join(row))
        f.write("\n")
