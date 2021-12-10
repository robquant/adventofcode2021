package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	file, err := os.Open("input.txt")
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

	rows := len(array)
	cols := len(array[0])
	result := 0
	for x := range array {
		for y, v := range array[x] {
			if x > 0 && v >= array[x-1][y] {
				continue
			}
			if x < rows-1 && v >= array[x+1][y] {
				continue
			}
			if y > 0 && v >= array[x][y-1] {
				continue
			}
			if y < cols-1 && v >= array[x][y+1] {
				continue
			}
			result += v + 1
		}
	}

	fmt.Println(result)
}
