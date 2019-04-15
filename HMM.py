# Viterbi Algorithm -- log
# forard/backward -- no log

import math

# read in fasta format input file
fileName = raw_input("What is the name of your input file: ")
f = open(fileName, 'r')

# seqNames = []
# sequence = []
# nameCt = 1
# seqCt = 0
sequence = ""
# put sequence name and sequences into arrays
for line in f:
    sequence = line
f.close()
print sequence

# A: P(x) given model
# hmm:
start = 0.5
emission = {'H': {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2}, 'L': {'A': 0.3, 'C': 0.2, 'G': 0.2, 'T': 0.3}}
transition = {'H': {'H': 0.5, 'L': 0.5}, 'L': {'H': 0.4, 'L': 0.6}}

# B: write complete viterbi table

# C: write most probable path

# D: p(most probable path)

# E: Are there multiple optimal paths?

# F: posterior probability of states H and L at position 4

# G: bonus... report all most probable paths
