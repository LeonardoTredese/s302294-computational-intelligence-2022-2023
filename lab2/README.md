Lab 2 - Genetic Algorithms
==========================

The problem is described [here](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab1_set-covering.ipynb)

I adopted Strategy 1, with tournaments for parent selection and acceptance with penalty for infeasible solutions.
I used 2 types of mutations and 2 types of crossovers.

Population size is set to 20, offspring size is set to 20, mutation rate is set to 0.8 and tournament
size is set to 15, maximum number of generations is set to 1000.

The results are the following

```
For problem of size 5:
     Found a valid solution
     with weight 5
     in 3 seconds
For problem of size 10:
     Found a valid solution
     with weight 10
     in 3 seconds
For problem of size 20:
     Found a valid solution
     with weight 24
     in 3 seconds
For problem of size 100:
     Found a valid solution
     with weight 204
     in 4 seconds
For problem of size 500:
     Found a valid solution
     with weight 1,516
     in 7 seconds
For problem of size 1000:
     Found a valid solution
     with weight 3,748
     in 14 seconds
For problem of size 10000:
     Found a valid solution
     with weight 58,058
     in 200 seconds
```
Collaborations
--------------

I have collaborated with:

- s291871
- s280117
