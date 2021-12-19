package main

import (
	"bufio"
	"bytes"
	"fmt"
	"math"
	"os"
	"strconv"
)

type SnailfishNumber struct {
	Left, Right interface{}
	Parent      *SnailfishNumber
}

type TokenType int

const (
	OPEN_PAR TokenType = iota
	CLOSE_PAR
	NUMBER
)

type Token struct {
	Type  TokenType
	Value int
}

func (s *SnailfishNumber) Magnitude() int {
	result := 0
	switch v := s.Left.(type) {
	case int:
		result += 3 * v
	case *SnailfishNumber:
		result += 3 * v.Magnitude()
	}
	switch v := s.Right.(type) {
	case int:
		result += 2 * v
	case *SnailfishNumber:
		result += 2 * v.Magnitude()
	}
	return result
}

func (s *SnailfishNumber) String() string {
	var b bytes.Buffer
	b.WriteString("[")
	switch v := s.Left.(type) {
	case int:
		fmt.Fprintf(&b, "%d", v)
	case *SnailfishNumber:
		fmt.Fprintf(&b, "%v", v)
	}
	b.WriteString(",")
	switch v := s.Right.(type) {
	case int:
		fmt.Fprintf(&b, "%d", v)
	case *SnailfishNumber:
		fmt.Fprintf(&b, "%v", v)
	}
	b.WriteString("]")
	return b.String()
}

func assert(val bool) {
	if !val {
		panic("Assert failed")
	}
}

func parseToTree(tokens []Token) *SnailfishNumber {
	number, _ := parseToSubTree(tokens, 0, nil)
	return number
}

func parseToSubTree(tokens []Token, start int, parent *SnailfishNumber) (*SnailfishNumber, int) {
	pos := start
	assert(tokens[pos].Type == OPEN_PAR)
	pos++
	var left, right interface{}
	var result SnailfishNumber

	// Only single digit numbers
	// left, err = strconv.Atoi(tokens[pos : pos+1])
	if tokens[pos].Type == NUMBER {
		left = tokens[pos].Value
	} else {
		left, pos = parseToSubTree(tokens, pos, &result)
	}
	// pos++
	// assert(tokens[pos] == ',')
	pos++
	if tokens[pos].Type == NUMBER {
		right = tokens[pos].Value
	} else {
		right, pos = parseToSubTree(tokens, pos, &result)
	}
	pos++
	assert(tokens[pos].Type == CLOSE_PAR)
	result.Left = left
	result.Right = right
	return &result, pos
}

func parseToTokens(input string) []Token {
	tokens := make([]Token, 0)
	for _, c := range input {
		switch c {
		case '[':
			{
				tokens = append(tokens, Token{OPEN_PAR, 0})
			}
		case ']':
			{
				tokens = append(tokens, Token{CLOSE_PAR, 0})
			}
		case ',':
			{
				continue
			}
		default:
			{
				// Number
				number, err := strconv.Atoi(string(c))
				if err != nil {
					panic(err)
				}
				tokens = append(tokens, Token{NUMBER, number})
			}
		}
	}
	return tokens
}

func explode(tokens []Token) ([]Token, bool) {
	depth := 0
	exploded := false
	for i := 0; i < len(tokens); i++ {
		token := tokens[i]
		if token.Type == OPEN_PAR {
			depth++
		} else if token.Type == CLOSE_PAR {
			depth--
		}
		if depth == 5 && token.Type == NUMBER {
			exploded = true
			assert(tokens[i+1].Type == NUMBER)
			for j := i - 2; j >= 0; j-- {
				if tokens[j].Type == NUMBER {
					tokens[j].Value += token.Value
					break
				}
			}
			i++
			token = tokens[i]
			for j := i + 2; j < len(tokens); j++ {
				if tokens[j].Type == NUMBER {
					tokens[j].Value += token.Value
					break
				}
			}
			copy(tokens[i-1:], tokens[i+2:])
			tokens[i-2] = Token{NUMBER, 0}
			tokens = tokens[:len(tokens)-3]
			return tokens, exploded
		}
	}
	return tokens, exploded
}

func split(tokens []Token) ([]Token, bool) {
	split := false
	for i := 0; i < len(tokens); i++ {
		token := tokens[i]
		if token.Type == NUMBER && token.Value >= 10 {
			new_tokens := append([]Token{}, tokens[:i]...)
			new_tokens = append(new_tokens, Token{OPEN_PAR, 0})
			left := int(math.Floor(float64(token.Value) / 2.0))
			right := int(math.Ceil(float64(token.Value) / 2.0))
			new_tokens = append(new_tokens, Token{NUMBER, left})
			new_tokens = append(new_tokens, Token{NUMBER, right})
			new_tokens = append(new_tokens, Token{CLOSE_PAR, 0})
			new_tokens = append(new_tokens, tokens[i+1:]...)
			split = true
			return new_tokens, split
		}
	}
	return tokens, split
}

func reduce(tokens []Token) []Token {
	var was_exploded, was_split bool
	for {
		if tokens, was_exploded = explode(tokens); was_exploded {
			continue
		}
		if tokens, was_split = split(tokens); was_split {
			continue
		}
		break
	}
	return tokens
}

func add(left, right []Token) []Token {
	result := []Token{{OPEN_PAR, 0}}
	result = append(result, left...)
	result = append(result, right...)
	result = append(result, Token{CLOSE_PAR, 0})
	return reduce(result)
}

func main() {
	// b := parseToTokens("[[[[[9,8],1],2],3],4]")
	// b, _ = explode(b)
	// tree, _ := parseToTree(b, 0, nil)
	// fmt.Printf("%v\n", tree)
	// c := parseToTokens(("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"))
	// c = reduce(c)
	// tree, _ = parseToTree(c, 0, nil)
	// fmt.Printf("%v\n", tree)

	file, _ := os.Open(os.Args[1])
	scanner := bufio.NewScanner(file)
	lines := make([][]Token, 0)
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, parseToTokens(line))
	}

	// Part 1
	var result []Token
	for _, tokens := range lines {
		if result == nil {
			result = tokens
			continue
		}
		result = add(result, tokens)
	}
	tree := parseToTree(result)
	fmt.Printf("Magnitude: %d\n", tree.Magnitude())

	// Part 2
	maxMag := 0
	for i := 0; i < len(lines); i++ {
		for j := i + 1; j < len(lines); j++ {
			mag := parseToTree(add(lines[i], lines[j])).Magnitude()
			if mag > maxMag {
				maxMag = mag
			}
			mag = parseToTree(add(lines[j], lines[i])).Magnitude()
			if mag > maxMag {
				maxMag = mag
			}
		}
	}
	fmt.Printf("Max pairwise Magnitude: %d\n", maxMag)
}
