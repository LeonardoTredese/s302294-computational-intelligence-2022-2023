Lab 2 - Genetic Algorithms
==========================

The problem is described [here](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab1_set-covering.ipynb)

I adopted Strategy 1, with tournaments for parent selection and acceptance with penalty for infeasible solutions.
I used 2 types of mutations and 2 types of crossovers.

Population size is set to 100, offspring size is set to 20, mutation rate is set to 0.7 and tournament
size is set to 15.

The results are the following

```
For problem of size 5:
 Found a valid solution
 with weight 5
For problem of size 10:
 Found a valid solution
 with weight 10
For problem of size 20:
 Found a valid solution
 with weight 23
For problem of size 100:
 Found a valid solution
 with weight 208
For problem of size 500:
 Found a valid solution
 with weight 1,564
For problem of size 1000:
 Found a valid solution
 with weight 4,048
```
