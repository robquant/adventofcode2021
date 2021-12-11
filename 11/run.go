package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

func read_array(path string) [][]int {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	array := make([][]int, 0)
	scanner := bufio.NewScanner(file)
	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		line := scanner.Text()
		numbers := make([]int, 0)
		for _, r := range line {
			number, _ := strconv.ParseInt(string(r), 10, 8)
			numbers = append(numbers, int(number))
		}
		array = append(array, numbers)
	}
	return array
}

func inc(octo [][]int, row, col int) {
	if row >= 0 && col >= 0 && row < len(octo) && col < len(octo[0]) {
		if octo[row][col] > 0 {
			octo[row][col]++
		}
	}
}

func flash(octo [][]int) int {
	nrows := len(octo)
	ncols := len(octo[0])

	nflashes := 0
	for row := 0; row < nrows; row++ {
		for col := 0; col < ncols; col++ {
			if octo[row][col] > 9 {
				nflashes += 1
				octo[row][col] = 0
				inc(octo, row-1, col-1)
				inc(octo, row-1, col)
				inc(octo, row-1, col+1)
				inc(octo, row, col-1)
				inc(octo, row, col+1)
				inc(octo, row+1, col-1)
				inc(octo, row+1, col)
				inc(octo, row+1, col+1)
			}
		}
	}
	return nflashes
}

func step(octo [][]int) int {
	nrows := len(octo)
	ncols := len(octo[0])

	for row := 0; row < nrows; row++ {
		for col := 0; col < ncols; col++ {
			octo[row][col] += 1
		}
	}
	total_flashes := 0
	nflashes := flash(octo)
	for ; nflashes > 0; nflashes = flash(octo) {
		total_flashes += nflashes
	}
	return total_flashes
}

func main() {

	array := read_array("input.txt")
	total_flashes := 0
	start := time.Now()
	for i := 0; i < 100; i++ {
		total_flashes += step(array)
	}
	fmt.Printf("Flash: %d\n", total_flashes)
	fmt.Printf("Runtime: %v\n", time.Since(start))
}
