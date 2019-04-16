# Viterbi Algorithm -- log
# forard/backward -- no log

import math


# fill matrix using viterbi
def findColMax(letter, matrix):
    h = matrix[letter - 1][state]
    l = matrix[letter - 1][state - 1]
    return max(h, l)


# read in fasta format input file
fileName = raw_input("What is the name of your input file: ")
f = open(fileName, 'r')

sequence = ""
# put sequence name and sequences into arrays
for line in f:
    sequence = line
f.close()

# model for forward/backward:
states = ("-", "0", "Hi", "Lo")
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

sequence = "-0" + sequence
vMatrix = [[0 for x in range(len(states) + 1)] for y in range(len(sequence) + 1)]
vMatrix[0][0] = '-'

# initialize i,0
for i in range(1, len(sequence)):
    vMatrix[i][0] = sequence[i]

# intialize 0,j
for j in range(1, len(states)):
    vMatrix[0][j] = states[j]

vMatrix[1][1] = 1
# initialize second row/col
for c in range(2, len(sequence) - 1):
    vMatrix[c][1] = 0
    # print vMatrix[c][2]
# print "next"
for r in range(2, len(states)):
    vMatrix[1][r] = 0
    # print vMatrix[1][r]

hi_opt = []
lo_opt = []
mult_opt = "NO"

for letter in range(2, len(sequence)):
    for state in range(2, len(states)):
        if letter == 2:
            vMatrix[letter][state] = start * log_emission[states[state]][sequence[letter]]
            if state == 2:
                hi_opt.append('H')
            else:
                lo_opt.append('L')
        else:
            # if state = 2 : in hi state -- check hi-hi, hi-lo
            if state == 2:
                pos_pos = vMatrix[letter - 1][state] * log_emission[states[state]][sequence[letter]] * \
                          log_transition[states[state]][states[state]]
                pos_neg = vMatrix[letter - 1][state + 1] * log_emission[states[state]][sequence[letter]] * \
                          log_transition[states[state + 1]][states[state + 1]]

                if pos_pos > pos_neg:
                    max_val = pos_pos
                    hi_opt.append('H')
                elif pos_neg > pos_pos:
                    max_val = pos_neg
                    hi_opt.append('L')
                else:
                    max_val = pos_pos
                    hi_opt.append('=')
                    mult_opt = 'YES'
                vMatrix[letter][state] = max_val

            # if state = 3 : in low state -- check lo-hi, lo-lo
            elif state == 3:
                neg_neg = vMatrix[letter - 1][state] * log_emission[states[state]][sequence[letter]] * \
                          log_transition[states[state]][states[state]]
                neg_pos = vMatrix[letter - 1][state - 1] * log_emission[states[state]][sequence[letter]] * \
                          log_transition[states[state - 1]][states[state - 1]]
                if neg_neg > neg_pos:
                    max_val = neg_neg
                    lo_opt.append('L')
                elif neg_pos > neg_neg:
                    max_val = neg_pos
                    lo_opt.append('H')
                else:
                    max_val = neg_pos
                    lo_opt += '='
                    mult_opt = 'YES'
                vMatrix[letter][state] = max_val

            else:
                print "you messed up indexing"



print "matrix"
for item in range(len(states)):
    for another in range(len(vMatrix) - 1):
        if another == len(vMatrix) - 2:
            print vMatrix[another][item]
        else:
            print vMatrix[another][item],

for something in hi_opt:
    print something,
print
print mult_opt
print
for e in lo_opt:
    print e,
# # initialize table
# vtable = [{}]
#
# for s in states:
#     vtable[0][s] = {"probability": start * log_emission[s][sequence[0]], "previous": None}
#
# for t in range(1, len(sequence)):
#     vtable.append({})
#     for st in states:
#         max_tr_prob = vtable[t - 1][states[0]]["probability"] * log_transition[states[0]][st]
#         prev_prob_sel = states[0]
#         for prev_st in states[1:]:
#             tr_prob = vtable[t - 1][prev_st]["probability"] * log_transition[prev_st][st]
#             if tr_prob > max_tr_prob:
#                 max_tr_prob = tr_prob
#                 prev_prob_sel = prev_st
#         max_prob = max_tr_prob * log_emission[st][sequence[t]]
#         vtable[t][st] = {"probability": max_prob, "previous": prev_prob_sel}
# # for i in range(len(vtable)):
# #     print " ".join(sequence[i])
# #     for state in vtable[0]:
# #         for v in vtable:
# #             print state, " ".join(v[state]["probability"])
# optimal = []
# max_prob = max(value["probability"] for value in vtable[-1].values())
# previous = None
# for st, data in vtable[-1].items():
#     if data["probability"] == max_prob:
#         optimal.append(st)
#         previous = st
#         break
#
# for t in range(len(vtable)-2, -1, -1):
#     optimal.insert(0, vtable[t+1][previous]["previous"])
#     previous = vtable[t+1][previous]["previous"]
#
# print optimal
# print max_prob

# A: P(x) given model

# B: write complete viterbi table

# C: write most probable path

# D: p(most probable path)

# E: Are there multiple optimal paths?

# F: posterior probability of states H and L at position 4

# G: bonus... report all most probable paths
