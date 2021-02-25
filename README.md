# Data Engineering puzzle

This is implementation of Data Engineering puzzle. For more information about the task/puzzle, go to https://github.com/nufrix/data-engineering-puzzle.

## How to run this solution
### 1. Go install Go
Expecting you already have Go installed on your system. If not, what are you waiting for?

Go to https://golang.org/doc/install and follow steps for download and installation.

### 2. Go build Go
Create executable for your system by running:

For MacOS and Linux
```
go build -o solve_puzzle puzzle/puzzle.go
```
For Windows

Switch to unix-like system, then go back to step 1. Go install Go.

Or you may try running
```
go build -o solve_puzzle.exe puzzle\puzzle.go
```
(Run at your own risk! Only gods know what will happen, might be good, might be catastrophic...)

### 3. Go run Go
If all went well, there should be an executable `solve_puzzle`(or `solve_puzzle.exe` for Windows users...). Run it as any other executable:

`./solve_puzzle`

OR

`./solve_puzzle.exe` (not sure how to run executables from cmd in windows, this is just a guess...)

You may want to specify input file as first argument.

`./solve_puzzle path/to/my/puzzle/input.txt`

Input file defaults to `./puzzle/puzzle_input.txt` (you know, the bigger one).

### 4. (Optional) Go make yourself some tea
You might want something to drink while you wait.

Just kidding, it does not take that long :)


## Expected result
Output to stdout shows length of input (after removing duplicate values), a list of all values (sorted of course, we not animals) and number of all possible variations.
```
List(len=31): [1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 33 34 35 38 39 42 45 46 47 48 49]
Final result is: 19208
Sample variation: [[0 1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 33 34 35 38 39 42 45 46 47 48 49] [0 1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 33 34 35 38 39 42 45 46 47 49] [0 1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 35 38 39 42 45 46 47 48 49]]
```

## How do you time this?
You may use any tool for timing executables. Unix command `time` might be handy.

`time ./solve_puzzle puzzle/puzzle_input.txt`

Example output (times might vary based on resources available):

```
List(len=31): [1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 33 34 35 38 39 42 45 46 47 48 49]
Final result is: 19208
Sample variation: [[0 1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 33 34 35 38 39 42 45 46 47 48 49] [0 1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 33 34 35 38 39 42 45 46 47 49] [0 1 2 3 4 7 8 9 10 11 14 17 18 19 20 23 24 25 28 31 32 35 38 39 42 45 46 47 48 49]]

real	0m0.037s    <- this number is what we are looking for
user	0m0.074s  X <- NOT THIS, this is CPU time combined from all CPU cores
sys     0m0.017s  X <- NOR THIS, this is time not spent by program, but system calls

```
