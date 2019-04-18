# forward/backward -- no
import math

# read in fasta format input file
fileName = raw_input("What is the name of your input file: ")
f = open(fileName, 'r')

sequence = ""
# put sequence name and sequences into arrays
for line in f:
    sequence = line
f.close()

rsequence = ""
n = len(sequence)
while n > 0:
    n -= 1
    rsequence += sequence[n]

sequence = "-0" + sequence
rsequence = "-0" + rsequence

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


vMatrix = [[0 for x in range(len(states) + 1)] for y in range(len(sequence) + 1)]
vMatrix[0][0] = '-'
rMatrix = [[0 for x in range(len(states) + 1)] for y in range(len(sequence) + 1)]
rMatrix[0][0] = '-'

# initialize i,0
for i in range(1, len(sequence)):
    vMatrix[i][0] = sequence[i]
    rMatrix[i][0] = sequence[i]

# intialize 0,j
for j in range(1, len(states)):
    vMatrix[0][j] = states[j]
    rMatrix[0][j] = states[j]

vMatrix[1][1] = 1
rMatrix[1][1] = 1
# initialize second row/col
for c in range(2, len(sequence) - 1):
    vMatrix[c][1] = 0
    rMatrix[c][1] = 0
    # print vMatrix[c][2]
# print "next"
for r in range(2, len(states)):
    vMatrix[1][r] = 0
    rMatrix[1][r] = 0


for letter in range(2, len(sequence)):
    for state in range(2, len(states)):
        if letter == 2:
            vMatrix[letter][state] = start * emission[states[state]][sequence[letter]]
            rMatrix[letter][state] = 1 * emission[states[state]][rsequence[letter]]

        else:
            # if state = 2 : in hi state
            if state == 2:
                l = emission[states[state]][sequence[letter]]
                pos = vMatrix[letter-1][state] * transition[states[state]][states[state]]
                neg = vMatrix[letter-1][state+1] * transition[states[state+1]][states[state]]

                rl = emission[states[state]][rsequence[letter]]
                rpos = rMatrix[letter-1][state] * transition[states[state]][states[state]]
                rneg = rMatrix[letter-1][state+1] * transition[states[state+1]][states[state]]

                vMatrix[letter][state] = l*(pos + neg)
                rMatrix[letter][state] = rl*(rpos + rneg)

            # if state = 3 : in low state
            elif state == 3:
                l = emission[states[state]][sequence[letter]]
                pos = vMatrix[letter - 1][state - 1] * transition[states[state-1]][states[state]]
                neg = vMatrix[letter - 1][state] * transition[states[state]][states[state]]

                rl = emission[states[state]][rsequence[letter]]
                rpos = rMatrix[letter-1][state - 1] * transition[states[state-1]][states[state]]
                rneg = rMatrix[letter-1][state] * transition[states[state]][states[state]]

                vMatrix[letter][state] = l * (pos + neg)
                rMatrix[letter][state] = rl * (rpos + rneg)


            else:
                print "you messed up indexing"

file1 = open("4.04.txt", 'w')
file2 = open("4.06", 'w')

forward_p = vMatrix[-2][2] + vMatrix[-2][3]
backward_p = rMatrix[-2][2] + rMatrix[-2][3]

total = forward_p + backward_p
file1.write(str(total))
#posterior probability for H and L
hp_prob = (vMatrix[6][2]*rMatrix[6][2])/total
lp_prob = (vMatrix[6][3]*rMatrix[6][3])/total

file2.write(str(hp_prob))
file2.write('\n')
file2.write(str(lp_prob))

file1.close()
file2.close()