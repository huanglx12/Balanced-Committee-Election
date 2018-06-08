# Balanced committee election


## 1. Balanced committee election demo

Balanced committee election corresponds to a scenario where we want to elect a committee from a candidate set that is balanced according to important features including gender, age and locality. For more details, have a look at Section 2 of our paper (https://arxiv.org/pdf/1710.10057).


### 1.1. Running a single experiment using the default settings

To run the code, you first need to install a package CPLEX (https://www.ibm.com/products/ilog-cplex-optimization-studio). 
The main program is winner.py, which takes an election as input, formulates voting as an integer linear program, and computes optimal balanced committees. To test whether the code works, try:

  python winner.py <demo.in >demo.out

where "demo.in" is a file containing the information of an election and "demo.out" is an output file that records the resulting optimal balanced committee. 
  While running "winner.py", the code will generate an additional file that contains the formulation of the corresponding integer linear program (optimization.lp).


### 1.2. Generating an unconstrained optimal committee 

Program "winner.py" can compute an (unconstrained) committee that achieves the most votes by running:

  python winner.py <demo.in >demo.out bloc k

The key "bloc" is for using the unconstrained rule for committee selection. 

The number "k" represents the desired number of winners. 

The "demo.in" file has the following format:
  1. A single line with a number m (the number of candidates).
  2. m lines with descriptions of the candidates. Each line contains three items: gender, age and locality. Here "gender" takes 2 valued 0/1 which corresponds to male/female correspondingly, "age" takes 3 valued 0/1/2 which corresponds to junior/middle-aged/senior correspondingly, and "locality" takes 2 valued 0/1 which corresponds to city/countryside correspondingly. 
  3. A single line with m numbers where the i-th number is the number of votes achieved by candidate i.

For example, the following file defines four candidates:
  4
  0 0 1
  1 1 0
  0 2 0
  1 1 0
  10 2 20 5

The generated "demo.out" file has the following format:
  1. A single line with k numbers which represents the selected optimal committee.
  2. A single line with the total votes of the selected optimal committee.
  3. k lines with descriptions of the selected candidates. Each line is of form: candidate_id: gender, age, locality, #votes.

For example, if "demo.in" is the prior example containing four candidates, running "python winner.py <demo.in >demo.out bloc 2" produces the following contents:
  Committee: 1 3 
  Total votes of the selected optimal committee: 30
  Candidate 1: male, junior, countryside, votes = 10
  Candidate 3: male, senior, city, votes = 20
  Male: 2
  Female: 0
  Junior: 1
  Middle-aged: 0
  Senior: 1
  City: 1
  Countryside: 1

   

### 1.3. Generating a balanced optimal committee 

Program "winner.py" can compute an optimal committee that achieves the most votes and satisfies specified requirements for three features gender, age and locality simulataneously by running

  python winner.py <demo.in >demo.out bloc_pro k lM uM lF uF lJ uJ lA uA lS uS lC uC lT uT

The key "bloc_pro" represents constrained voting with balanced requirements in gender, age and locality. 

The key "demo.in", "demo.out" and "k" are the same as described in Section 1.2. The remaining input represents the following:
  1. The fairness constraints for gender: the number of selected male candidates is at least "lM" and at most "uM", and the number of selected female candidates is at least "lF" and at most "uF".
  2. The fairness constraints for age: the number of selected junior candidates is at least "lJ" and at most "uJ", the number of selected middle-aged candidates is at least "lA" and at most "uA", and the number of selected senior candidates is at least "lS" and at most "uS".
  3. The fairness constraints for locality: the number of selected candidates living in the city is at least "lC" and at most "uC", and the number of selected candidates living in the countryside is at least "lT" and at most "uT".


### 1.4. Generating all balanced optimal committees

Sometimes, there may have more than one optimal balanced committees of size k. Program "winner.py" can compute all optimal committees that achieve the most votes and satisfies specified requirements for three features gender, age and locality simulataneously by running

  python winner.py <demo.in >demo.out bloc_pro_allsolution k lM uM lF uF lJ uJ lA uA lS uS lC uC lT uT

All input keys are exactly the same as described in Section 1.2 except "demo.out". The generated "demo.out" file has the following format:
  1. A single line with the number T of optimal balanced committees.  
  2. A single line with the total votes received by optimal balanced committees. 
  3. T optimal balanced committees, each with the same form as described in Section 1.3.








 