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

# model for forward/backward:
states = ("-", "0", "Hi", "Lo")
log_start = math.log(0.5, 2)

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

# hi_opt = []
# lo_opt = []
mult_opt = "NO"
max_val = 0
for letter in range(2, len(sequence)):
    for state in range(2, len(states)):
        if letter == 2:
            vMatrix[letter][state] = log_start + log_emission[states[state]][sequence[letter]]

        else:
            # if state = 2 : in hi state -- check hi-hi, hi-lo
            if state == 2:
                pos_pos = vMatrix[letter - 1][state] + log_emission[states[state]][sequence[letter]] + \
                          log_transition[states[state]][states[state]]
                pos_neg = vMatrix[letter - 1][state + 1] + log_emission[states[state]][sequence[letter]] + \
                          log_transition[states[state + 1]][states[state + 1]]
                # print pos_pos, pos_neg
                if pos_pos > pos_neg:
                    max_val = pos_pos
                elif pos_neg > pos_pos:
                    max_val = pos_neg
                else:
                    mult_opt = 'YES'
                vMatrix[letter][state] = max_val

            # if state = 3 : in low state -- check lo-hi, lo-lo
            elif state == 3:
                neg_neg = vMatrix[letter - 1][state] + log_emission[states[state]][sequence[letter]] + \
                          log_transition[states[state]][states[state]]
                neg_pos = vMatrix[letter - 1][state - 1] + log_emission[states[state]][sequence[letter]] + \
                          log_transition[states[state - 1]][states[state - 1]]
                # print neg_neg, neg_pos
                if neg_neg > neg_pos:
                    max_val = neg_neg
                elif neg_pos > neg_neg:
                    max_val = neg_pos
                else:
                    mult_opt = 'YES'
                vMatrix[letter][state] = max_val

            else:
                print "you messed up indexing"


#find optimum path
opt_path = []
for c in range(2, len(sequence)):
    hi_val = vMatrix[c][2]
    lo_val = vMatrix[c][3]
    if hi_val > lo_val:
        opt_path.append('H')
    elif lo_val > hi_val:
        opt_path.append('L')
    else:
        opt_path.append('=')
        mult_opt = 'YES'

file1 = open("4.01.txt", 'w')
file2 = open("4.02.txt", 'w')
file3 = open("4.03.txt", 'w')
file4 = open("4.05.txt", 'w')

for item in range(len(states)):
    for another in range(len(vMatrix) - 1):
        if another == len(vMatrix) - 2:
            file2.write(str(vMatrix[another][item]))
            file2.write('\n')
        else:
            file2.write(str(vMatrix[another][item]))
            file2.write(' ')
file2.close()

for thing in opt_path:
    file3.write(thing)
print
file3.close()

file4.write(mult_opt)
file4.close()

pos_max = vMatrix[-2][2]
neg_max = vMatrix[-2][3]
tmax = max(pos_max, neg_max)
file1.write(str(tmax))
file1.close()

