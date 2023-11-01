BOARD_FILE = './mejn-board.txt'

with open(BOARD_FILE) as f:
    board_string = f.read()


def print_board(players):
    # For each square that is occupied by one of the player's pawns, store the
    # first character of the player's color in a dict, for easy reference.
    print()

    board = {}
    for player in players:
        for square in player['active_pawn_positions']:
            board[square] = player["color"][0]

    # Scan the file contents character by character
    pos = 0
    while pos < len(board_string):
        char = board_string[pos]

        if char == 'p':
            # A two-digit game board position.
            board_pos = int(board_string[pos+1:pos+3])
            print(f"[{board.get(board_pos, ' ')}]", end='')
            pos += 3

        elif char == 'a' or char == 'h':
            # Either *available* or *home* pawns. The next two characters are single-digit
            # values, representing the player number, and the threshold value, which is the
            # minimum *available* or *home* count for which we should show the player
            # color's first character within the ( ) brackets.

            player_num = int(board_string[pos+1])
            threshold = int(board_string[pos+2])

            if player_num >= len(players):
                # This player number is not participating, don't show anything.
                print("   ", end='')
            else:
                player = players[player_num]
                value = player['available_pawn_count'] if char == 'a' else player['home_pawn_count']
                output = player['color'][0] if value >= threshold else '_'
                print(f" {output} ", end='')
            pos += 3

        else:
            # A character without special meaning, just print it!
            print(char, end='')
            pos += 1