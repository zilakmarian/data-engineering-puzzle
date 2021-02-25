package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"os"

	"sort"
	"strconv"
	"strings"
	"sync"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func removeDuplicateValues(intSlice []int) []int {
	keys := make(map[int]bool)
	list := []int{}
	// If the key(values of the slice) is not equal
	// to the already present value in new slice (list)
	// then we append it. else we jump on another element.
	for _, entry := range intSlice {
		if _, value := keys[entry]; !value {
			keys[entry] = true
			list = append(list, entry)
		}
	}
	return list
}

// readInts reads whitespace-separated ints from r. If there's an error, it
// returns the ints successfully read so far as well as the error value.
func readInts(r io.Reader) ([]int, error) {
	scanner := bufio.NewScanner(r)
	scanner.Split(bufio.ScanWords)
	var result []int
	for scanner.Scan() {
		x, err := strconv.Atoi(scanner.Text())
		if err != nil {
			return result, err
		}
		result = append(result, x)
	}
	return result, scanner.Err()
}

// imagine values to be vertexes in directed graph
// try to find all combinations by racing to end of the graph
// once there (leaf vertex), increment value holding number of found leaves
// thus finding the number of all possible combinations
func CrunchVariation(path []int, initial_value, position int, values []int, mut *sync.Mutex, wg *sync.WaitGroup, final_result *[][]int) {
	// add new value to path of currently crunched variation
	if position < len(path) {
		path[position] = initial_value
	} else {
		path = append(path, initial_value)
	}
	// there will be three possible paths at most, due to deduplicating and rules for the task
	high_pos := position + 3
	if high_pos > len(values) {
		high_pos = len(values)
	}
	next_vals := values[position:high_pos]
	// find positions for next iteration, 0 - 3 paths leading from 'vertex' are possible
	var next_pos []int
	for i, v := range next_vals {
		if diff := v - initial_value; 1 <= diff && diff <= 3 {
			next_pos = append(next_pos, position+1+i)
		}
	}
	// no other path means we found unique variation
	// this is a leaf value, mark found combination and exit
	// sync writing with mutex to avoid race conditions
	if len(next_pos) <= 0 {
		mut.Lock()
		*final_result = append(*final_result, path)
		mut.Unlock()
		return
	}

	before := len(path)
	// walk first found path, then start spawning go routines
	// this is mostly to reduce number of all go routines running at the same time
	// thus limiting memory requirements
	// power of go routines is kind of wasted by doing this, but it is more reliable on memory conumption
	CrunchVariation(path, next_vals[0], next_pos[0], values, mut, wg, final_result)
	if len(path) != before {
		print("FML")
	}
	// launch go routines over new vertexes
	// their children might spawn their own go routines, if they find multiple paths
	if len(next_pos) > 1 {
		for i, u := range next_pos[1:] {
			// clone new path, that way no two go routines will share same resource
			new_path := make([]int, len(path))
			copy(new_path, path)

			wg.Add(1)
			// don't know any better way to recursively start another go routine with different arguments
			go func(f_path []int, val, pos int) {
				// must decrement counter of all additional running go routines, otherwise will deadlock
				defer wg.Done()
				CrunchVariation(f_path, val, pos, values, mut, wg, final_result)
			}(new_path, next_vals[i+1], u)
		}
	}

	return
}

func main() {
	// default path of input file is puzzle directory
	file_path := "./puzzle/puzzle_input.txt"
	// allow first argument to be path to another input file
	if len(os.Args) > 1 {
		file_path = os.Args[1]
	}
	// read the whole file
	dat, err := ioutil.ReadFile(file_path)
	check(err)
	// convert all values to ints
	ints, err := readInts(strings.NewReader(string(dat)))
	check(err)
	// no value can be used twice, remove redundant values
	ints = removeDuplicateValues(ints)
	// sort the rest of values
	sort.Ints(ints)
	// create variable fo
	// create mutex for syncing writes to return value
	var mu = sync.Mutex{}
	// need a reliable way to wait for all go routines to finish, use WaitGroup for it
	var wg sync.WaitGroup
	var initial_path []int
	var result_paths [][]int
	// run recursive go routine, that walks (more like runs :) through all variations and counts them
	// pass address of return value 'result_paths', so function can modify it outside of own scope
	CrunchVariation(initial_path, 0, 0, ints, &mu, &wg, &result_paths)
	// until all of go routines are finished, the result will not be complete
	wg.Wait()
	// show what numbers were crunched and the result
	fmt.Printf("List(len=%v): %v\n", len(ints), ints)
	fmt.Println("Final result is:", len(result_paths))
	if len(result_paths) > 0 {
		fmt.Println("Sample variation:", result_paths[:3])
	}

	// print out all results to out.txt
	// uncomment if you want to write results to file

	//f, err := os.Create("out.txt")
	//check(err)
	//defer f.Close()
	//for _, v := range result_paths {
	//	_, err = f.WriteString(fmt.Sprint(v))
	//	check(err)
	//	_, err = f.WriteString("\n")
	//	check(err)
	//}

}
