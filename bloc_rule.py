import numpy as np
import sys

sys.path.append('/afs/akt.tu-berlin.de/service/cplex/cplex/python/x86-64_sles10_4.1') # the path of CPLEX package
import cplex
from cplex.exceptions import CplexError


# generate the optimization problem for unconstrained voting:
# Each binary variable xi represents a candidate Ci. xi = 1 means that we select candidate Ci as a winner.
def write_cplex_format_bloc(scoring, k, out):
    m = len(scoring)
    f = open(out, 'w')

    # generate the objective function: the total score of the selected committee
    s = "Maximize\nobj:"

    pos = 0
    first = True
    for i in range(m):
        if not first:
            s += " +"
        first = False
        s += " " + str(scoring[i]) + " x" + str(i)

        pos += 1

    # generate the cardinality constraint: the number of selected winners is k.
    f.write(s + "\n")
    f.write("Subject To\n")
    subj_k = "c1:"
    first = True
    for i in range(m):
        if not first:
            subj_k += " +"
        first = False
        subj_k += " " + "x" + str(i)

    f.write(subj_k + ' = ' + str(k) + '\n')

    # list all binary variables
    f.write("Binary\n")
    for i in range(m):
        f.write("x" + str(i) + "\n")

    f.write("End\n")
    f.close()

# generate the optimization problem for fair voting:
# Each binary variable xi represents a candidate Ci. xi = 1 means that we select candidate Ci as a winner.
# xi should satisfy the cardinality constraint sum_i xi = k and all fairness constraints according to sensitive attributes.
def write_cplex_format_bloc_pro(candidate, scoring, k, out, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT):
    m = len(scoring)
    f = open(out, 'w')


    # generate the objective function: the total score of the selected committee
    s = "Maximize\nobj:"

    pos = 0
    first = True
    for i in range(m):
        if not first:
            s += " +"
        first = False
        s += " " + str(scoring[i]) + " x" + str(i)

        pos += 1

    f.write(s + "\n")
    f.write("Subject To\n")

    # generate the cardinality constraint: the number of selected winners is k.
    subj_k = "c1:"
    first = True
    for i in range(m):
        if not first:
            subj_k += " +"
        first = False
        subj_k += " " + "x" + str(i)

    f.write(subj_k + ' = ' + str(k) + '\n')

    # generate the fairness constraint for gender: the number of selected male candidates is at least lM and at most uM.
    subj_lM = "c2:"
    subj_uM = "c3:"
    first = True
    for i in range(m):
        if int(candidate[i][0]) == 0:
            if not first:
                subj_lM += " +"
                subj_uM += " +"
            first = False
            subj_lM += " " + "x" + str(i)
            subj_uM += " " + "x" + str(i)

    f.write(subj_lM + ' >= ' + str(lM) + '\n')
    f.write(subj_uM + ' <= ' + str(uM) + '\n')

    # generate the fairness constraint for gender: the number of selected female candidates is at least lF and at most uF.
    subj_lF = "c4:"
    subj_uF = "c5:"
    first = True
    for i in range(m):
        if int(candidate[i][0]) == 1:
            if not first:
                subj_lF += " +"
                subj_uF += " +"
            first = False
            subj_lF += " " + "x" + str(i)
            subj_uF += " " + "x" + str(i)

    f.write(subj_lF + ' >= ' + str(lF) + '\n')
    f.write(subj_uF + ' <= ' + str(uF) + '\n')

    # generate the fairness constraint for age: the number of selected junior candidates is at least lJ and at most uJ.
    subj_lJ = "c6:"
    subj_uJ = "c7:"
    first = True
    for i in range(m):
        if int(candidate[i][1]) == 0:
            if not first:
                subj_lJ += " +"
                subj_uJ += " +"
            first = False
            subj_lJ += " " + "x" + str(i)
            subj_uJ += " " + "x" + str(i)

    f.write(subj_lJ + ' >= ' + str(lJ) + '\n')
    f.write(subj_uJ + ' <= ' + str(uJ) + '\n')

    # generate the fairness constraint for age: the number of selected middle-aged candidates is at least lA and at most uA.
    subj_lA = "c8:"
    subj_uA = "c9:"
    first = True
    for i in range(m):
        if int(candidate[i][1]) == 1:
            if not first:
                subj_lA += " +"
                subj_uA += " +"
            first = False
            subj_lA += " " + "x" + str(i)
            subj_uA += " " + "x" + str(i)

    f.write(subj_lA + ' >= ' + str(lA) + '\n')
    f.write(subj_uA + ' <= ' + str(uA) + '\n')

    # generate the fairness constraint for age: the number of selected senior candidates is at least lS and at most uS.
    subj_lS = "c10:"
    subj_uS = "c11:"
    first = True
    for i in range(m):
        if int(candidate[i][1]) == 2:
            if not first:
                subj_lS += " +"
                subj_uS += " +"
            first = False
            subj_lS += " " + "x" + str(i)
            subj_uS += " " + "x" + str(i)

    f.write(subj_lS + ' >= ' + str(lS) + '\n')
    f.write(subj_uS + ' <= ' + str(uS) + '\n')

    # generate the fairness constraint for locality: the number of selected candidates living in the city is at least lC and at most uC.
    subj_lC = "c12:"
    subj_uC = "c13:"
    first = True
    for i in range(m):
        if int(candidate[i][2]) == 0:
            if not first:
                subj_lC += " +"
                subj_uC += " +"
            first = False
            subj_lC += " " + "x" + str(i)
            subj_uC += " " + "x" + str(i)

    f.write(subj_lC + ' >= ' + str(lC) + '\n')
    f.write(subj_uC + ' <= ' + str(uC) + '\n')

    # generate the fairness constraint for locality: the number of selected candidates living in the countryside is at least lT and at most uT.
    subj_lT = "c14:"
    subj_uT = "c15:"
    first = True
    for i in range(m):
        if int(candidate[i][2]) == 1:
            if not first:
                subj_lT += " +"
                subj_uT += " +"
            first = False
            subj_lT += " " + "x" + str(i)
            subj_uT += " " + "x" + str(i)

    f.write(subj_lT + ' >= ' + str(lT) + '\n')
    f.write(subj_uT + ' <= ' + str(uT) + '\n')


    # list all binary variables
    f.write("Binary\n")
    for i in range(m):
        f.write("x" + str(i) + "\n")

    f.write("End\n")
    f.close()


# apply CPLEX to compute an unconstrained optimal committee and the unconstrained optimal score
def run_ilp_bloc(score, k):
    m = len(score)
    candidates = np.arange(0, m, 1)

    # generate the optimization problem for unconstrained voting
    tmp = "optimization" + ".lp"

    write_cplex_format_bloc(score, k, tmp)
    cpx = cplex.Cplex(tmp)

    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_results_stream(None)

    # apply CPLEX to solve the optimization problem
    try:
        cpx.solve()
    except CplexError, exc:
        print exc
        return

    x = np.array(cpx.solution.get_values()[-m:])  # the solution computed by CPLEX
    opt = cpx.solution.get_objective_value()  # compute the score of the unconstrained optimal committee

    # return an unconstrained optimal committee and the unconstrained optimal score
    return candidates[np.logical_and(x > 0.9, x < 1.1)], opt


# apply CPLEX to compute an optimal committee with fairness constraints and the optimal score
def run_ilp_bloc_pro(candidate, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT):
    m = len(score)
    candidates = np.arange(0, m, 1)

    # generate the optimization problem for fair voting
    tmp = "optimization" + ".lp"

    write_cplex_format_bloc_pro(candidate, score, k, tmp, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT)
    cpx = cplex.Cplex(tmp)

    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_results_stream(None)

    # apply CPLEX to solve the optimization problem
    try:
        cpx.solve()
    except CplexError, exc:
        print exc
        return

    x = np.array(cpx.solution.get_values()[-m:]) # the solution computed by CPLEX
    opt = cpx.solution.get_objective_value() # compute the score of the optimal committee with fairness constraints

    # return an optimal committee and the optimal score
    return candidates[np.logical_and(x > 0.9, x < 1.1)], opt

# apply CPLEX to compute all optimal committees with fairness constraints and the optimal score
def run_ilp_bloc_pro_allsolution(candidate, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT):
    m = len(score)
    candidates = []

    tmp = "optimization" + ".lp"

    # generate the optimization problem for fair voting
    write_cplex_format_bloc_pro(candidate, score, k, tmp, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT)
    cpx = cplex.Cplex(tmp)

    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_results_stream(None)

    # apply CPLEX to solve the optimization problem
    try:
        cpx.parameters.randomseed.set(1)
        cpx.solve()
    except CplexError, exc:
        print exc
        return

    opt = cpx.solution.get_objective_value() # compute the score of the optimal committee with fairness constraints

    cpx.parameters.mip.pool.absgap.set(0) # ensure to compute optimal committees
    cpx.parameters.mip.limits.populate.set(1000000) # output at most 100 optimal committees. The number 100 can be modified accordingly.
    cpx.parameters.mip.pool.intensity.set(4)
    cpx.populate_solution_pool()

    x = {} # solutions computed by CPLEX
    candidates = {}
    c = {} # record all optimal committees
    for i in range(cpx.solution.pool.get_num()):
        x[i] = np.array(cpx.solution.pool.get_values(i,)[-m:])
        candidates[i] = np.arange(0, m, 1)
        c[i] = candidates[i][np.logical_and(x[i] > 0.9, x[i] < 1.1)]

    print >>sys.stderr, "There are %d optimal committees" % (len(c))

    return c, opt


# compute an unconstrained optimal committee
def bloc( C, score, k , lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT):

  # compute an unconstrained optimal committee
  (winning_committee, total_satisfaction) = run_ilp_bloc(score, k)

  return list(winning_committee), total_satisfaction


# compute an optimal committee with fairness constraints
def bloc_pro( C, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT ):

  (winning_committee, total_satisfaction) = run_ilp_bloc_pro(C, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT)
  return list(winning_committee), total_satisfaction


# compute all optimal committees with fairness constraints
def bloc_pro_allsolution( C, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT ):

  (winning_committee, total_satisfaction) = run_ilp_bloc_pro_allsolution(C, score, k, lM, uM, lF, uF, lJ, uJ, lA, uA, lS, uS, lC, uC, lT, uT)
  return winning_committee, total_satisfaction