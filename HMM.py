# Viterbi Algorithm -- log
# forard/backward -- no log

import math

# read in fasta format input file
fileName = raw_input("What is the name of your input file: ")
f = open(fileName, 'r')

sequence = ""
# put sequence name and sequences into arrays
for line in f:
    sequence = line
f.close()
print sequence

# sequence = "0" + s

# model for forward/backward:
states = ("Hi", "Lo")
start = 0.5
emission = {
    'Hi': {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2},
    'Lo': {'A': 0.3, 'C': 0.2, 'G': 0.2, 'T': 0.3}
}
transition = {
    'Hi': {'Hi': 0.5, 'Lo': 0.5},
    'Lo': {'Hi': 0.4, 'Lo': 0.6}
}

# log model for viterbi
log_emission = {
    'Hi': {'A': math.log(0.2, 2), 'C': math.log(0.3, 2), 'G': math.log(0.3, 2), 'T': math.log(0.2, 2)},
    'Lo': {'A': math.log(0.3, 2), 'C': math.log(0.2, 2), 'G': math.log(0.2, 2), 'T': math.log(0.3, 2)}
}
log_transition = {
    'Hi': {'Hi': math.log(0.5, 2), 'Lo': math.log(0.5, 2)},
    'Lo': {'Hi': math.log(0.4, 2), 'Lo': math.log(0.6, 2)}
}

# initialize table
vtable = [{}]

for s in states:
    vtable[0][s] = {"probability": start * log_emission[s][sequence[0]], "previous": None}

for t in range(1, len(sequence)):
    vtable.append({})
    for st in states:
        max_tr_prob = vtable[t - 1][states[0]]["probability"] * log_transition[states[0]][st]
        prev_prob_sel = states[0]
        for prev_st in states[1:]:
            tr_prob = vtable[t - 1][prev_st]["probability"] * log_transition[prev_st][st]
            if tr_prob > max_tr_prob:
                max_tr_prob = tr_prob
                prev_prob_sel = prev_st
        max_prob = max_tr_prob * log_emission[st][sequence[t]]
        vtable[t][st] = {"probability": max_prob, "previous": prev_prob_sel}
# for i in range(len(vtable)):
#     print " ".join(sequence[i])
#     for state in vtable[0]:
#         for v in vtable:
#             print state, " ".join(v[state]["probability"])
optimal = []
max_prob = max(value["probability"] for value in vtable[-1].values())
previous = None
for st, data in vtable[-1].items():
    if data["probability"] == max_prob:
        optimal.append(st)
        previous = st
        break

for t in range(len(vtable)-2, -1, -1):
    optimal.insert(0, vtable[t+1][previous]["previous"])
    previous = vtable[t+1][previous]["previous"]

print optimal
print max_prob

# A: P(x) given model

# B: write complete viterbi table

# C: write most probable path

# D: p(most probable path)

# E: Are there multiple optimal paths?

# F: posterior probability of states H and L at position 4

# G: bonus... report all most probable paths
