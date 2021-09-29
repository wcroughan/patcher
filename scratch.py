import os
from enum import Enum

patchdir = os.path.join(os.getcwd(), "patches")
fn1 = os.path.join(patchdir, "keys0.ksd")
fn2 = os.path.join(patchdir, "organ0.ksd")


class OPS(Enum):
    SAME = 0
    INS = 0
    DEL = 0


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
    cur = range(cols)
    cur_s = [("-"*i, s2[0:i]) for i in range(cols)]
    for r in range(1, rows):
        prev, cur = cur, [r] + [0] * (cols - 1)
        prev_s, cur_s = cur_s, [(s1[0:r], "-"*r)] + [("", "")]*(cols-1)

        print("p1: r={}, prev={}, cur={}".format(r, prev, cur))
        print("\tprev_s={}".format(prev_s))
        print("\tcur_s={}".format(cur_s))
        for c in range(1, cols):
            deletion = prev[c] + 1
            insertion = cur[c - 1] + 1
            if s1[r - 1] == s2[c - 1]:
                edit = prev[c - 1]
                print("p3: r={}, c={}".format(r, c))
            else:
                edit = prev[c - 1] + 1

            if edit < deletion and edit < insertion:
                cur[c] = edit
                cur_s[c] = (prev_s[c-1][0] + s1[r-1], prev_s[c-1][1] + s2[c-1])
            elif deletion < insertion:
                cur[c] = deletion
                cur_s[c] = (prev_s[c-1][0] + "-", prev_s[c-1][1] + s2[c-1])
            else:
                cur[c] = insertion
                cur_s[c] = (prev_s[c-1][0] + s1[r-1], prev_s[c-1][1] + "-")
        print("p2", cur, cur_s)

    return (cur[-1], cur_s[-1])


print(levenshtein("ABC", "FAB"))
