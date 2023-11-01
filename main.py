# External modules.
from board_printer import *
import random
import os

# Global variables.
PAWN_COUNT = 4
MIN_PLAYERS = 2
MAX_PLAYERS = 4
COLORS = ["red", "green", "yellow", "black"]
BOARD_SIZE = 40

# The main function that calls the needed functions every turn until a winner is found.
def main():
    print('*** Mens Erger Je Niet ***')

    output_method = choose_output_method()

    if not os.path.exists("game-state.txt"):
        players = read_players()

        print('\n** Players **')
        for player in players:
            print(f" Player #{players.index(player)} plays with the color: {player['color'].capitalize()} ")

        print_type(players, output_method)

        current_player = players[-1]["color"] # Set to the last player so that the turn is given to player 1.

    else:
        if not os.path.getsize('game-state.txt') == 0:
            players = []

            with open("game-state.txt", 'r') as file:
                lines = file.readlines()
            
            for index, line in enumerate(lines):
                if index is not 0:
                    color, pawns_available, pawns_home, pawns_active = parse_line(line)
                    player = {
                        "color": color,
                        "start_position": 10 * index,
                        "active_pawn_positions": pawns_active,
                        "available_pawn_count": pawns_available,
                        "home_pawn_count": pawns_home,
                    }
                    players.append(player)
                else:
                    header_line = line.strip().split('=')

            current_player = header_line[1]

            print_type(players, output_method)
        else:
            print("File is empty!")
            exit()

    # Loop every turn.
    while True:
        current_player = change_turn(players, current_player)

        print(f"\nPlayer {current_player}:")
        input("  Press enter to roll the dice...")

        rolled_number = roll_dice()

        current_player_index = get_player_index(players, current_player)

        act_on_dice_value(rolled_number, players, current_player_index)
        
        print_type(players, output_method)

        save_game(players, current_player)

        has_current_player_won(players, current_player_index)

# Check the game-state.txt file and return the right values.
def parse_line(line):
    pawns_available = 0
    pawns_home = 0
    pawns_active = []

    line = line.strip()
    parts = line.split('/')
    color, pawns = parts[0], parts[1:]
    for pawn in pawns:
        if pawn == "a":
            pawns_available += 1
        elif pawn == "h":
            pawns_home += 1
        elif pawn.isdigit():
            pawns_active.append(int(pawn))

    return color, pawns_available, pawns_home, pawns_active

# Ask for the amount/color of the players and give them the right values. (Partly provided by LMS)
def read_players():
    players = []
    
    while True:
        player_count = input("\nWith how many players would you like to play [2-4]: ")
        if player_count.isdigit() and MIN_PLAYERS <= int(player_count) <= MAX_PLAYERS:
            player_count = int(player_count)
            break
        else:
            print("Invalid number!")
    
    available_colors = COLORS.copy()

    for player_num in range(1, player_count + 1):
        while True:
            selected_color = input(f"Choose a color for player #{player_num} [{', '.join(available_colors)}]: ")
            if selected_color.lower() in available_colors:
                player = {
                    "color": selected_color,
                    "start_position": 10 * (player_num - 1),
                    "active_pawn_positions": [],
                    "available_pawn_count": PAWN_COUNT,
                    "home_pawn_count": 0,
                }
                players.append(player)
                available_colors.remove(selected_color)
                break
            else:
                print("Invalid color!")

    return players

# Print the current state of the game.
def print_game_state(players):
    all_active_positions = []

    print("\nPlayers:")
    for player in players:
        print(f"   {players.index(player)}: {player['color']} (starting square: {player['start_position']}, pawns available: {player['available_pawn_count']}, pawns home: {player['home_pawn_count']})")
    print("Board:")
    for player in players:
        all_active_positions.extend(player["active_pawn_positions"])
    
    if not all_active_positions:
        print("   No pawn on the board.")
        
    else:
        sorted_positions = sorted(all_active_positions)
        for position in sorted_positions:
            for player in players:
                if position in player["active_pawn_positions"]:
                    formatted_position = f"{position:4}" if position >= 10 else f"{position:4}"
                    print(f"{formatted_position}: {player['color']}")

# Change turn for the players.
def change_turn(players, current_player=None):
    if current_player is None:
        current_player = players[0]['color']
    
    current_player_index = None
    for index, player in enumerate(players):
        if player['color'] == current_player:
            current_player_index = index
            break
    
    if current_player_index is not None:
        next_player_index = (current_player_index + 1) % len(players)
        next_player = players[next_player_index]['color']
        return next_player

# Generate random 1-6.
def roll_dice():
    rolled_number = random.randint(1, 6)
    print(f"  You rolled: {rolled_number}!")
    return rolled_number

# Get the index number of the current player.
def get_player_index(players, current_player):
    for i, player in  enumerate(players):
        if player["color"] == current_player:
            index = i
            break

    return index

# Checks what number is rolled and what to do next. (Place pawn, Move pawn, Remove Pawn, Add home pawn, etc.)
def act_on_dice_value(rolled_number, players, current_player_index):
    current_player = players[current_player_index]

    if rolled_number == 6 and current_player["available_pawn_count"] > 0:
        if current_player["start_position"] in current_player["active_pawn_positions"]:
            selected_pawn = current_player["start_position"]
            new_position = calculate_new_position(selected_pawn, rolled_number)
            check_pawn_on_square(selected_pawn, new_position, players)
            move_pawn(players, current_player_index, selected_pawn, new_position)
        else:
            for player in players:
                if current_player["start_position"] in player["active_pawn_positions"]:
                    player["active_pawn_positions"].remove(current_player["start_position"])
                    player["available_pawn_count"] += 1
                    print(f"  Another player's pawn was on square {current_player['start_position']}, it is sent back to available pawns.")
            print("  Placing a pawn on the starting square!")
            current_player["available_pawn_count"] -= 1
            current_player["active_pawn_positions"].append(current_player["start_position"])

    elif current_player["active_pawn_positions"]:
        if len(current_player["active_pawn_positions"]) == 1:
            selected_pawn = current_player["active_pawn_positions"][0]
        else:
            while True:
                selected_pawn = input(f"  The pawn at which square would you like to move? ({', '.join(map(str, current_player['active_pawn_positions']))}) ")
                if selected_pawn.isdigit() and int(selected_pawn) in current_player["active_pawn_positions"]:
                    selected_pawn = int(selected_pawn)
                    break

        new_position = calculate_new_position(selected_pawn, rolled_number)

        check_pawn_on_square(selected_pawn, new_position, players)

        if new_position == current_player["start_position"]:
            current_player["active_pawn_positions"].remove(selected_pawn)
            current_player["home_pawn_count"] += 1
            print("  Pawn has arrived home!")
        else:
            move_pawn(players, current_player_index, selected_pawn, new_position)

    else:
        print("  No movable pawns.")

# Calculate the new pawn position on the board.
def calculate_new_position(selected_pawn, rolled_number):
    new_position = (selected_pawn + rolled_number) % BOARD_SIZE
    print(f"  Pawn moving from {selected_pawn} to {new_position}.")

    return new_position

# Checks if a pawn is on the new-position square.
def check_pawn_on_square(selected_pawn, new_position, players):
    for player in players:
        if new_position in player["active_pawn_positions"]:
            player["active_pawn_positions"].remove(new_position)
            player["available_pawn_count"] += 1
            print(f"  Another player's pawn was on square {new_position}, it is sent back to available pawns.")

# Move the pawn to its new position.
def move_pawn(players, current_player_index, selected_pawn, new_position):
    current_player = players[current_player_index]
    current_player["active_pawn_positions"].remove(selected_pawn)
    current_player["active_pawn_positions"].append(new_position)

# Checks if a player has won.
def has_current_player_won(players, current_player_index):
    for player in players:
        if player["home_pawn_count"] == 4:
            print(f"""
All the pawns of player #{current_player_index} ({player['color'].capitalize()}) are in their homes.
Player #{current_player_index} ({player['color'].capitalize()}) wins!""")
            if os.path.exists("game-state.txt"):
                os.remove("game-state.txt")
            exit()

# Save the game state to the right file.
def save_game(players, current_player):
    with open("game-state.txt", 'w') as file:
        file.write(f"last_turn={current_player}\n")
        for player in players:
            color = player["color"]
            active_pawns = player["active_pawn_positions"]
            available_pawn_count = player["available_pawn_count"]
            home_pawn_count = player["home_pawn_count"]

            pawns = ['a' for pawn in range(available_pawn_count)] + ['h' for pawn in range(home_pawn_count)]
            active_pawns_string = [str(pawn) for pawn in active_pawns]

            file.write(f"{color}/{'/'.join(pawns)}/{'/'.join(active_pawns_string)}\n")

# Ask the user what output method to use.
def choose_output_method():
    print("\nWhich game state output would you like?")
    print(" 1. Simple (text based output)")
    print(" 2. Advanced (visual based output)")
    while True:
        output_method = input("Please choose a option: ")
        if output_method.isdigit() and 1 <= int(output_method) <= 2:
            break

    return output_method

# Print the correct output method
def print_type(players, output_method):
    if output_method == "1": # Simple
        print_game_state(players)
    elif output_method == "2": # Advanced
        print_board(players)

main()