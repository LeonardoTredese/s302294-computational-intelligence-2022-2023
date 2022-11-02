Lab 1 - Graph Search
====================

The problem is described [here](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab1_set-covering.ipynb)

In this solution I use a graph search with both Dijkstra and A star algorithms.

The output of the program looks like this:

```
Starting search for N: 5 with A_star:
	Found a solution with cost 5
	visited 151 states
Starting search for N: 5 with dijkstra:
	Found a solution with cost 5
	visited 367 states
Starting search for N: 10 with A_star:
	Found a solution with cost 10
	visited 2,197 states
Starting search for N: 10 with dijkstra:
	Found a solution with cost 10
	visited 337,561 states
Starting search for N: 20 with A_star:
	Found a solution with cost 23
	visited 33,691 states
Starting search for N: 20 with dijkstra:
	Found a solution with cost 23
	visited 545,985 states
```

Known Issues
------------

- Running both Dijkstra and A star for problem size greater than 100
  takes way to long. I never wayted for it to find the actual solution.

Collaborations
--------------

I have collaborated with:

- s291871
- s280117

Yanking
-------

I have yanked lines of code from the professors
[8 puzzle example](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab1_set-covering.ipynb)
