from game_logic import YatzyGame
from interface import Interface


if __name__ == '__main__':
    game = YatzyGame()
    interface = Interface(game = game)
    interface.main_menu()