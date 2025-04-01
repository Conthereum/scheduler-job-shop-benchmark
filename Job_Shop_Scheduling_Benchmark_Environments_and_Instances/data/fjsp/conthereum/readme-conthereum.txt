---------------------------
FJS file format input data:
totalJob totalMachine maximumOperationPerMachine
[each line for each job:] operationCountInJob operationOptions [per operationOptions:] machinId [starting from 1] duration

Note: input time for each transaction is defined by nano second instead of millisecond because the numbers are integers
and if it was millisecond we could not define 6.3 millisecond - there are two seperate files of the same data in milli
second to compare their performance.



Makespan: 315000  -> the time that 100 jobs are done in parallel in 3 machines

--------------------------
            GA
--------------------------
for 100 non conflicting transactions that take between 5 to 10 millisecond to execute which take 777 ms to execute in a serial way, running on my PC:
1- using OR-Tool code:  (makespan): 675 ms - first feasible answer (walltime) - in 25.01 s
2- using GA+FJSP code: makespan: 315.000 ms - walltime: 1.51 s

in the best optimal expectation, it can be optimal to 777/3 = 259
--------------------------
by increasing the input to 200 non-conflicting transaction (2 times of the previous dataset):
Makespan: 531000
WallTime (s): 18.20144820213318
--------------------------
        Dispatching
--------------------------
Bugs:
(?) number_total_machines in dispatching_rules.toml seems redundant with data in fjs definition

----------------------
for each machine_assignment_rule, there is an implementation in rules.py in which selectes the next machin SPT: select a
 machin in which that specific operation takes the least to execute on it / EER: select a machin which has the earliest
 end time and in all tests SPT return the best result. in our case all operations take the same time in any machin and
 can bypass it



