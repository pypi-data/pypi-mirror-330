import xler8
import sys
import csv
import copy
from openpyxl.utils import get_column_letter


custom_del = ','

infile = sys.argv[1]
sheetname = sys.argv[2]
outfile = sys.argv[3]

try:
    if sys.argv[4] == "tab":
        custom_del = "\t"
except:
    pass

print("Reading %s into sheet %s in file %s" % (infile, sheetname, outfile))

data = []
cw = {}
colf = 1.4

col_chars = []

with open(infile, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=custom_del, quotechar='"')


    hdrs=[]
    h_mode=True
    for row in csvreader:
        if h_mode:
            h_mode = False
            hdrs = copy.deepcopy(row)
            data.append(hdrs)
            for hdr in hdrs:
                col_chars.append(len(hdr))
            continue

        for rvi in range(0, len(row)):
            new_length = len(str(row[rvi]))
            if new_length > col_chars[rvi]:
                col_chars[rvi] = new_length

        data.append(row)
        # rd = dict(zip(hdrs, row))
        # print(rd)

    for hci in range(0, len(hdrs)):
        cw[get_column_letter(1+hci)] = int(col_chars[hci] * colf)
    
    print(cw)

xler8.xlsx_out(filename=outfile, sheets={
    sheetname: {
        'data': data,
        'cw': cw
    }
})
