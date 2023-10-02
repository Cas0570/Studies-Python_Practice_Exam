PAWN_COUNT = 4
MIN_PLAYERS = 2
MAX_PLAYERS = 4
COLORS = ["red", "green", "yellow", "black"]
BOARD_SIZE = 40


def main():
    print('*** Mens Erger Je Niet ***')

    players = read_players()

    print('** Players **')
    # TODO: show player numbers and colors

    # TODO: play the game! Don't forget to split up your code into some
    # functions that make sense.

    # TODO: Game finished? Show who's won!


def read_players():
    """Ask the user how many players want to participate, and what colors they want to play. Returns the list of players."""

    # TODO: implement!

    # Each player could be a dictionary similar to this:
    # {
    #     "color": "red",
    #     "start_position": 10,
    #     "active_pawn_positions": [], # no pawns are on the board yet
    #     "available_pawn_count": 4, # all pawns still need a 6 to be thrown to start
    #     "home_pawn_count": 0, # no pawns are home yet
    # }
    # Midway in the game, the dictionary could look like this.
    # {
    #     "color": "red",
    #     "start_position": 10,
    #     "active_pawn_positions": [10, 3], # position 10 is red's start square, position 3 is 7 squares before red's finish
    #     "available_pawn_count": 1, # one pawn still needs a 6 to start
    #     "home_pawn_count": 1, # one pawn is already home safe
    # }
    # Of course, you're also free to organize the game state in some other way.
    return []


main()