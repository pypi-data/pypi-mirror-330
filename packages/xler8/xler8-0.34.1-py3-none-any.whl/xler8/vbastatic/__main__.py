import xler8
import argparse
import copy
from pprint import pprint as PP
import sys


print("usage: $1=textfile with line number line by line, $2=vba outfile")

lines = None
with open(sys.argv[1], 'r') as f:
    lines = [ int(x.strip()) for x in f.read().strip().split("\n") ]

outfile = sys.argv[2]


lines = list(reversed(sorted(lines)))


with open(outfile, 'w') as f:
    f.write("' auto generated xler8.vba row-killer\n");
    f.write("\n");
    f.write("Sub ReverseRowKiller()\n");
    f.write("  With Sheet1\n");
    for i in lines:
        f.write("    .Rows(%d).EntireRow.Delete\n" % i);
    f.write("  End With\n");
    f.write("End Sub\n");
    f.write("\n");

PP(outfile)