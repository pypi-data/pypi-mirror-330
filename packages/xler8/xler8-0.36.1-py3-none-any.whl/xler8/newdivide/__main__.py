import sys

if len(sys.argv) == 1:
    sys.stderr.write("""
usage: PROGRAM col_start_incl col_stop_excl [ divider_string ] [ test ]
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

s_command = None
try:
    s_command = sys.argv[4]
except:
    pass

segmentation_count = 1

prev_item = None
curr_item = None

prev_line = None
curr_line = None

line_no = 0

for line in sys.stdin.readlines():
    line_no += 1

    curr_line = line
    curr_item = curr_line[i_from:i_to]

    if s_command != None:
        sys.stderr.writelines("(ii) line %d\n" % line_no)
        sys.stderr.writelines("(ii) item = [%s]\n" % curr_item)
        sys.stderr.writelines("(ww) premature test exit, only processed 1 line\n")
        sys.stderr.flush()
        sys.exit(1)

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

sys.stderr.write("(ii) segments in total: %d\n" % segmentation_count)
sys.stderr.flush()
