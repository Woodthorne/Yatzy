import random
import string
from typing import Any, Generator

from die import Die
from player import Player

class Turn:
    def __init__(self, turn_num: int, player: Player) -> None:
        self.turn_num = turn_num
        self.player = player
        self.dice: dict[str, Die] = {char: Die() for char in string.ascii_lowercase[:5]}
        self.scored = False
        self._die_rolls = 0

    @property
    def die_rolls(self) -> int:
        return self._die_rolls
    
    def get_dice(self, ordered: bool = False) -> list[Die]:
        dice = [die for die in self.dice.values()]
        if ordered:
            dice.sort(key = lambda die: die.pips)
        return dice

    def get_dice_pips(self, ordered: bool = False) -> list[int]:
        return [die.pips for die in self.get_dice(ordered)]

    def get_die(self, key: str) -> Die:
        if key in self.dice.keys():
            return self.dice[key]
        return None
    
    def roll_dice(self) -> None:
        for die in self.dice.values():
            die.roll()
        self._die_rolls += 1


class YatzyGame:
    def __init__(self) -> None:
        self._players: dict[str, Player] = {}
        self._turn_order: list[Player] = []

    def add_player(self, player_name) -> None:
        self._players[player_name] = Player(player_name)

    def get_player_from_order(self) -> Generator[Player, Any, None]:
        for player in self._turn_order:
            yield player
        for player in self.get_player_from_order():
            yield player

    def get_players(self, ordered: bool = True) -> list[Player]:
        players = [player for player in self._players.values()]
        if ordered:
            players.sort(key = lambda player: player.total_score())
        return players

    def has_players(self) -> bool:
        return self.player_count() > 0
    
    def player_names(self) -> Generator[str, Any, None]:
        for player in self._players.values():
            yield player.name

    def player_count(self) -> int:
        return len(self._players.items())
    
    def remove_player(self, player_name: str) -> None:
        del self._players[player_name]

    def reset(self) -> None:
        self.__init__()

    def set_turn_order(self) -> None:
        for player_name in self.player_names():
            self._turn_order.append(self._players[player_name])
        
        random.shuffle(self._turn_order)
    
    def turns(self) -> Generator[Turn, Any, None]:
        turn_num = 0
        for player in self.get_player_from_order():
            if player.is_done():
                return
            else:
                turn_num += 1
                yield Turn(
                    turn_num = turn_num,
                    player = player
                )
