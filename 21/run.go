package main

import "fmt"

type Dice interface {
	Roll() int
}

type DeterministicDice struct {
	next  int
	count int
}

type Player struct {
	id     int
	pos    int
	points int
}

func (d *DeterministicDice) Roll() (ret int) {
	ret = d.next
	d.next = (d.next + 1) % 101
	d.count++
	if d.next == 0 {
		d.next = 1
	}
	return
}

func step(p *Player, d Dice) {
	for i := 0; i < 3; i++ {
		p.pos += d.Roll()
		for p.pos > 10 {
			p.pos -= 10
		}
	}
	p.points += p.pos
}

func main() {
	players := []*Player{{id: 1, pos: 1}, {id: 2, pos: 2}}
	dice := DeterministicDice{next: 1}
	won := false
	for {
		for _, player := range players {
			step(player, &dice)
			fmt.Printf("Player %d moves to %d, total %d\n", player.id, player.pos, player.points)
			if player.points >= 1000 {
				won = true
				break
			}
		}
		if won {
			break
		}
	}
	var total int
	for _, player := range players {
		if player.points < 1000 {
			fmt.Printf("Player %d lost with %d points after %d dice rolls\n", player.id, player.points, dice.count)
			total = player.points * dice.count
			break
		}
	}
	fmt.Printf("Total: %d", total)
}
