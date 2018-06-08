################################
# winner.py -- Winner Computation
#

from random import *
from sys import *


# import rule package

from bloc_rule import *


# read in the data in our format
# m (number of candidates)
# C1: gender_1 age_1 locality_1 (sensitive attributes of m candidates: gender: male/female, age: junior/middle-aged/senior, locality: city/countryside)
# ...
# score_1 score_2 ... score_m  (the votes of each candidate)

# return (C,score)
def readData(f, k):
    C = []
    score = {}
    lines = f.readlines()
    m = lines[0].split()

    for l in lines[1:int(m[0]) + 1]:
        s = l.split(" ")[0:3]
        s = [int(x) for x in s]
        C += [s]

    score = np.array(lines[int(m[0]) + 1].split())


    return (C, score)


#
# print winners
#

# print an optimal committee
def printWinners(W, S, cand, score):

    print "Committee:", "".join([str(int(i)+1)+" " for i in W]) # the optimal committee

    print "Total votes of the selected optimal committee: %d" % (int(S)) # the total votes

    for i in W:
        print "Candidate %d: %s, %s, %s, votes = %s" % (i+1, cand[i][0], cand[i][1], cand[i][2], score[i])

    # compute the number of specified sensitive attributes in the selected committee
    nM = 0
    nF = 0
    nJ = 0
    nA = 0
    nS = 0
    nC = 0
    nT = 0
    for i in W:
        if cand[i][0] == "male":
            nM += 1
        elif cand[i][0] == "female":
            nF += 1

        if cand[i][1] == "junior":
            nJ += 1
        elif cand[i][1] == "middle-aged":
            nA += 1
        elif cand[i][1] == "senior":
            nS += 1

        if cand[i][2] == "city":
            nC += 1
        elif cand[i][2] == "countryside":
            nT += 1

    print "Male: %d" % (nM)
    print "Female: %d" % (nF)
    print "Junior: %d" % (nJ)
    print "Middle-aged: %d" % (nA)
    print "Senior: %d" % (nS)
    print "City: %d" % (nC)
    print "Countryside: %d" % (nT)




# print all optimal committees
def printWinners_allsolution(W, S, cand, score):

    num = len(W) # the number of optimal feasible committees
    print "Total number of optimal committees: %d" % (num)

    print "Total votes of an optimal committee: %d" % (int(S)) # the total votes

    for j in range(num):
        print ""
        print "Optimal committee %d" % (j+1)
        sol = list(W[j])
        for i in sol:
            print "Candidate %d: %s, %s, %s, votes = %s" % (i + 1, cand[i][0], cand[i][1], cand[i][2], score[i])

        # compute the number of specified sensitive attributes in the selected committee
        nM = 0
        nF = 0
        nJ = 0
        nA = 0
        nS = 0
        nC = 0
        nT = 0
        for i in sol:
            if cand[i][0] == "male":
                nM += 1
            elif cand[i][0] == "female":
                nF += 1

            if cand[i][1] == "junior":
                nJ += 1
            elif cand[i][1] == "middle-aged":
                nA += 1
            elif cand[i][1] == "senior":
                nS += 1

            if cand[i][2] == "city":
                nC += 1
            elif cand[i][2] == "countryside":
                nT += 1

        print "Male: %d" % (nM)
        print "Female: %d" % (nF)
        print "Junior: %d" % (nJ)
        print "Middle-aged: %d" % (nA)
        print "Senior: %d" % (nS)
        print "City: %d" % (nC)
        print "Countryside: %d" % (nT)


if __name__ == "__main__":

    data_in = stdin
    data_out = stdout

    seed()

    # default settings
    R = bloc_pro # voting rule
    k = 10       # number of winners
    lM = 5       # lower bound for selected male
    uM = 5       # upper bound for selected male
    lF = 5       # lower bound for selected female
    uF = 5       # upper bound for selected female
    lJ = 2       # lower bound for selected young people
    uJ = 2       # upper bound for selected young people
    lA = 6       # lower bound for selected adult
    uA = 6       # upper bound fro selected adult
    lS = 2       # lower bound for selected old people
    uS = 2       # upper bound for selected old people
    lC = 8       # lower bound for selected citizen
    uC = 8       # upper bound for selected citizen
    lT = 2       # lower bound for selected Country people
    uT = 2       # upper bound for selected Country people

    if (len(argv) >= 3):
        R = eval(argv[1])
        k = int(argv[2])
        if (len(argv) >= 4 and "bloc_" in str(R)):
            lM = int(argv[3])
            uM = int(argv[4])
            lF = int(argv[5])
            uF = int(argv[6])
            lJ = int(argv[7])
            uJ = int(argv[8])
            lA = int(argv[9])
            uA = int(argv[10])
            lS = int(argv[11])
            uS = int(argv[12])
            lC = int(argv[13])
            uC = int(argv[14])
            lT = int(argv[15])
            uT = int(argv[16])


    (C, score) = readData(data_in, k) # read the election
    C = np.array(C)

    W, S = R(C, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT) # compute the optimal committees with fairness constraints

    # translate the format of sensitive attributes from numbers to words
    cand = {}
    for i in range(len(C)):
        cand[i] = {}
        if C[i][0] == 0:
            cand[i][0] = "male"
        elif C[i][0] == 1:
            cand[i][0] = "female"

        if C[i][1] == 0:
            cand[i][1] = "junior"
        elif C[i][1] == 1:
            cand[i][1] = "middle-aged"
        elif C[i][1] == 2:
            cand[i][1] = "senior"

        if C[i][2] == 0:
            cand[i][2] = "city"
        elif C[i][2] == 1:
            cand[i][2] = "countryside"

    if 'allsolution' in str(R):
        printWinners_allsolution(W, S, cand, score)
    else:
        printWinners(W, S, cand, score)

    data_out.close()