import os
from enum import Enum
from pathlib import Path
from struct import iter_unpack

patchdir = os.path.join(os.getcwd(), "patches")
fn1 = os.path.join(patchdir, "keys0.ksd")
fn2 = os.path.join(patchdir, "organ0.ksd")


class OPS(Enum):
    START = 0
    INSERT = 1
    DELETE = 2
    NOP = 3
    EDIT = 4


def levenshtein(s1, s2):
    if s1 == s2:
        return 0
    rows = len(s1) + 1
    cols = len(s2) + 1

    if not s1:
        return cols - 1
    if not s2:
        return rows - 1

    prev = None
    prev_s = None
    prev_ops = None
    cur = range(cols)
    cur_s = [("-"*i, s2[0:i]) for i in range(cols)]
    cur_ops = [".," + "ins,"*i for i in range(cols)]
    for r in range(1, rows):
        if r % 25 == 0:
            print("{}/{}".format(r, rows))
        prev, cur = cur, [r] + [0] * (cols - 1)
        prev_s, cur_s = cur_s, [(s1[0:r], "-"*r)] + [("", "")]*(cols-1)
        prev_ops, cur_ops = cur_ops, [".," + "del,"*r] + [""]*(cols-1)

        # print("p1: r={}, prev={}, cur={}".format(r, prev, cur))
        # print("\tprev_s={}".format(prev_s))
        # print("\tcur_s={}".format(cur_s))
        for c in range(1, cols):
            deletion = prev[c] + 1
            insertion = cur[c - 1] + 1
            if s1[r - 1] == s2[c - 1]:
                edit = prev[c - 1]
                # print("p3: r={}, c={}".format(r, c))
                editDiff = False
            else:
                edit = prev[c - 1] + 1
                editDiff = True

            if edit < deletion and edit < insertion:
                cur[c] = edit
                cur_s[c] = (prev_s[c-1][0] + s1[r-1], prev_s[c-1][1] + s2[c-1])
                cur_ops[c] = prev_ops[c-1] + ("edt," if editDiff else "nop,")
            elif deletion < insertion:
                cur[c] = deletion
                cur_s[c] = (prev_s[c][0] + s1[r-1], prev_s[c][1] + "-")
                cur_ops[c] = prev_ops[c] + "ins,"
            else:
                cur[c] = insertion
                cur_s[c] = (cur_s[c-1][0] + "-", cur_s[c-1][1] + s2[c-1])
                cur_ops[c] = cur_ops[c-1] + "del,"
        # print("p2", cur, cur_s, cur_ops)

    return (cur[-1], cur_s[-1], cur_ops[-1])


# print(levenshtein("AGBC", "FAIB"))

d1 = Path(fn1).read_bytes()
d2 = Path(fn2).read_bytes()
print(d1)

d1ar = iter_unpack('B', d1)
d2ar = iter_unpack('B', d2)

s1 = ""
for c in d1ar:
    s = hex(c[0])
    ss = s[2:]
    if len(ss) == 1:
        ss = "0" + ss
    s1 += ss
print(s1)

s2 = ""
for c in d2ar:
    s = hex(c[0])
    ss = s[2:]
    if len(ss) == 1:
        ss = "0" + ss
    s2 += ss
print(s2)

d, ss, ops = levenshtein(s1, s2)
opar = ops.split(',')
# print(d, ss, ops, opar)
print(len(ss[0]), len(ss[1]))

for oi, op in enumerate(opar):
    if oi == 0 or oi == len(opar)-1:
        continue
    if op != "nop":
        print("{}: {} ({}, {})".format(oi, op, ss[0][oi-1], ss[1][oi-1]))
