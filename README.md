# Data Engineering puzzle

This puzzle was selected from Advent of Code 2020 for my colleagues at MallGroup.

## Task
You have list of numbers (found in the file `puzzle/puzzle_input.txt`). Find out all possible combinations that can be generated from this list, when the following rules are fulfilled:
* Each sequence starts with 0
* The difference between each item in valid combination must be between 1 and 3, e.g. sequence `0, 2, 5, 6, 8` is valid, `0, 2, 6, 8` is *not* valid
* Each number from given list of numbers can be used a maximum of once in each combination.
* The sequence ends when no other item in given list of numbers can not be used
* The sequence must be in ascending order

## Example
List of numbers `1, 2, 3, 5`:

### Valid combinations (examples):
* `0, 1, 2, 3, 5`
* `0, 1, 2, 5`
* `0, 2, 5`
* `0, 2, 3, 5`
* `0, 3, 5`

### Invalid combinations (examples):
* `0, 5` because the difference is 5
* `0, 1, 5` because the difference is 4
* `0, 2, 3` because not all possible items from given list were used (you have to add 5 at the end)
* `3, 5` because the sequence doesn't start with 0
* `0, 3, 2, 5` the sequence order is not ascending

## Testing data
If you want to test your algorithm, here are some testing data:
`[28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]`
and the amount if valid combinations that fulfill the rules above is `19208`. 

## Run reference application
Create your virtual environment:
```bash
python3.8 -m venv venv
```
activate it:
```bash
. venv/bin/activate
```
and run the program:
```bash
(venv) python3.8 main.py --input puzzle/puzzle_input_test.txt
```
and the expected output is:
```bash
Running with puzzle/puzzle_input_test.txt file.
2021-02-02 16:28:17,669 INFO     Puzzle input: [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49] 
2021-02-02 16:28:17,669 INFO     Computing starting variants.
2021-02-02 16:28:17,671 INFO     Creating threads for 7 starting variants
2021-02-02 16:28:17,675 INFO     Create and start thread 0 with variant [0, 1, 2, 4, 7].
2021-02-02 16:28:17,682 INFO     Create and start thread 1 with variant [0, 2, 3, 4, 7].
2021-02-02 16:28:17,688 INFO     Create and start thread 2 with variant [0, 3, 4, 7].
2021-02-02 16:28:17,695 INFO     Create and start thread 3 with variant [0, 1, 2, 3, 4, 7].
2021-02-02 16:28:17,752 INFO     Create and start thread 4 with variant [0, 1, 4, 7].
2021-02-02 16:28:17,773 INFO     Create and start thread 5 with variant [0, 1, 3, 4, 7].
2021-02-02 16:28:17,774 INFO     Create and start thread 6 with variant [0, 2, 4, 7].
2021-02-02 16:28:18,325 INFO     Found 10000 variants
2021-02-02 16:28:18,786 INFO     Result: 19208
```
If you want to run the reference application with production data:
```bash
(venv) python3.8 main.py --input puzzle/puzzle_input.txt
```

## Test reference application
Active you virtualenv:
```bash
. venv/bin/activate
```
move to `tests` directory:
```bash
(venv) cd tests/
```
and run tests:
```bash
(venv) pytest
```
and all tests should be OK (and green:) ).