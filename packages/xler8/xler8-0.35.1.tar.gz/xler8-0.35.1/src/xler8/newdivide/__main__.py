import sys

if len(sys.argv) == 1:
    sys.stderr.write("""
usage: PROGRAM col_start_incl col_stop_excl [ divider_string ]
hint: columns start an 0 - so for example just regarding the first 4 characters would mean '0 5'
""")
    sys.exit(1)

i_from = int(sys.argv[1])
i_to = int(sys.argv[2])

s_newdivide = ""
try:
    s_newdivide = sys.argv[3]
except:
    pass

segmentation_count = 1

prev_item = None
curr_item = None

prev_line = None
curr_line = None

for line in sys.stdin.readlines():
    curr_line = line
    curr_item = curr_line[i_from:i_to]

    if prev_item == None:
        prev_line = curr_line
        prev_item = prev_line[i_from:i_to]
        sys.stdout.write(curr_line)
        continue

    if curr_item != prev_item:
        segmentation_count += 1
        sys.stdout.write("%s\n" % s_newdivide)

    sys.stdout.write(curr_line)
    prev_line = curr_line
    prev_item = curr_item

sys.stdout.flush()

sys.stderr.write("Segments in total: %d\n" % segmentation_count)
sys.stderr.flush()
