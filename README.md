# Data Engineering puzzle

This puzzle was selected from Advent of Code 2020 for my colleagues at MallGroup.

## Task
You have list of numbers (found in the file `puzzle_input.txt`). Find out how many possible combinations can be generated from this list, when the following rules are fulfilled:
* Each sequence starts with 0
* The difference between each item in valid combination must be between 1 and 3, e.g. sequence `0, 2, 5, 6, 8` is valid, `0, 2, 6, 8` is *not* valid
* Each number from given list of numbers can be used a maximum of once in each combination.
* The sequence ends when no other item in given list of numbers can not be used
* The sequence must be in ascending order

## Example
List of numbers `1, 2, 3, 5`:

### Valid combinations:
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
