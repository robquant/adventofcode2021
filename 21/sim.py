from collections import defaultdict

# Frequency table of sum of three rolls of the Dirac Dice
sum_freq_three_rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7 : 6, 8: 3, 9: 1}

def step(states):
    new_states = defaultdict(int)
    for state, count in states.items():
        pos, points = state
        for sum_, freq in sum_freq_three_rolls.items():
            new_pos = pos + sum_
            if new_pos > 10:
                new_pos -= 10
            new_points = points + new_pos
            new_states[(new_pos, new_points)] += count * freq
    return new_states

def count_wins(states):
    wins = 0
    for state, count in states.items():
        pos, points = state
        if points >= 21:
            wins += count
    return wins

def remove_win_universes(states):
    new_states = defaultdict(int)
    for state, count in states.items():
        _, points = state
        if points < 21:
            new_states[state] = count
    return new_states

states_player1 = defaultdict(int)
states_player1[(1,0)] = 1
states_player2 = defaultidct(int)
states_player2[(2,0)] = 1

wins_player1 = 0
wins_player2 = 0

while sum(states_player2.values()) > 0:
    states_player1 = step(states_player1)
    wins = count_wins(states_player1)
    wins_player1 += wins * sum(states_player2.values())
    states_player1 = remove_win_universes(states_player1)
    states_player2 = step(states_player2)
    wins = count_wins(states_player2)
    wins_player2 += wins * sum(states_player1.values())
    states_player2 = remove_win_universes(states_player2)

if wins_player1 > wins_player2:    
    print(f"Player 1 won in {wins_player1} universes")
else:
    print(f"Player 2 won in {wins_player2} universes")
