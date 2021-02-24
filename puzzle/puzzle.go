package main

import (
    "bufio"
    "fmt"
    "io"
    "io/ioutil"
    "strconv"
    "strings"
    "sort"
    "os"
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
func CrunchVariation(initial_value, position int, values []int, ret_val *int, mut *sync.Mutex, wg *sync.WaitGroup) {
    // must decrement counter of all running go routines, otherwise go will deadlock
    defer wg.Done()
    // there will be three possible paths at most, due to deduplicating and rules for
    high_pos := position+3
    if high_pos > len(values){
        high_pos = len(values)
    }
    next_vals := values[position:high_pos]
    // find positions for next iteration, 0 - 3 paths leading from 'vertex' are possible
    var next_pos []int
    for i, v := range next_vals {
        if diff := v - initial_value; 1 <= diff && diff <= 3{
            next_pos = append(next_pos, position+1+i)
        }
    }
    // no other path means we found unique variation
    // this is a leaf value, mark found combination and exit
    // sync writing with mutex to avoid race conditions
    if len(next_pos) <= 0 {
        mut.Lock()
        *ret_val += 1
        mut.Unlock()
        return
    }
    // launch go routines over new vertexes
    // their children will spawn their own go routines
    // after few recursion cycles, in the end there will be single go routine for each leaf vertex
    // this might be very resource intensive, but these routines are fairly small and quick
    for i, u := range next_pos {
        wg.Add(1)
		go func(pos, val int) {
			CrunchVariation(pos, val, values, ret_val, mut, wg)
		}(next_vals[i], u)
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
    // create variable for return value
    var ret_val int
    // create mutex for syncing writes to return value
    var mu = sync.Mutex{}
    // need a reliable way to wait for all go routines to finish, use WaitGroup for it
    var wg sync.WaitGroup
    // add to counter of running go routines
    wg.Add(1)
    // run recursive go routine, that walk (more like runs :) through all variations and counts them
    // pass address of return value, so function can modify it outside of own scope
    go CrunchVariation(0, 0, ints, &ret_val, &mu, &wg)
    // until all of go routines are finished, the result will not be complete
    wg.Wait()
    // show what numbers were crunched and the result
    fmt.Printf("List(len=%v): %v\n", len(ints), ints)
    fmt.Println("Final result is:", ret_val)
}
