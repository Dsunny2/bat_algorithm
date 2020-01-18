## Available Scripts

In the project directory, you can run the testfile.py **experiment** function:

### `Input`

**1.**   **filename** 

**Format:** string

**Data description:** filename of standardized data from TSPLIB (http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) Files ending in .tsp are the original test data set, and files ending in .opt.tour are the optimal solutions that already exist. You only need to put the test data set.

**Input example:**  bays29.tsp berlin52.tsp

**Suggestion:** if you just want to test, please choose small scale data set (below 100 points) because it will take a lot of time to calculate.

**2.**   **bat_size**

**format:** int

**Data description:** the number of bats. The larger the number of bats, the larger the range of random search, and the less likely it is to fall into a local optimal solution.

**Input example:** 5 15 25

**Suggestion:** You can start with small number like 5, if the result is unsatisfying, try bigger number.

**3.**   **iterations**

**Format:** int

**Data description:** the number of iterations. The larger the number of iterations, the closer to the optimal solution.

**Input example:** 100 150 300

**Suggestion:** You can start with small number like 100, if the result is unsatisfying, try bigger number.

### `Output`

**1.**   **best path & best distance**

They are the best path and best distance based on the bat size and the number of iterations you set.

**2.**   **best path existed & best distance existed**

They are the best path and best distance found by others, which is the optimal solution now known.

**3.**   **The graph in results folder**

The blue lines stand for the optimal solution and the red lines stand for our experiment results. There are some specific information about this experiment in the upper right corner.


