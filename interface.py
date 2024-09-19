import os
import string

from die import Die
from game_logic import Turn, YatzyGame
from slots import Upper, Slot

class Interface:
    def __init__(self, game: YatzyGame) -> None:
        self.game = game

    def main_menu(self) -> None:
        notification = None
        while True:
            self._print_rows(
                self._header('Huvudmeny'),
                notification,
                '1. Nytt spel',
                '0. Avsluta'
            )
            notification = ''
            opt = input('>>> ')
            if opt == '0':
                quit()
            elif opt == '1':
                self._new_game_menu()
            else:
                notification = 'Ogiltigt kommando'
    
    def _new_game_menu(self) -> None:
        notification = None
        while True:
            self._print_rows(
                self._header('Nytt spel'),
                notification,
                'Spelare:' if self.game.has_players() else None,
                *[f' - {name}' for name in self.game.player_names()],
                '1. Lägg till spelare' if self.game.player_count() != 5 else None,
                '2. Ta bort spelare' if self.game.player_count() != 0 else None,
                '3. Börja spelet' if 1 < self.game.player_count() < 6 else None,
                '0. Tillbaka till huvudmeny'
            )
            notification = None
            opt = input('>>> ')
            if opt == '0':
                self.game.reset()
                return
            elif opt == '1':
                self._add_player_menu()
            elif opt == '2' and self.game.has_players():
                self._remove_player_menu()
            elif opt == '3' and self.game.has_players():
                self._play_game()
                return
            else:
                notification = 'Ogiltigt kommando'

    def _add_player_menu(self) -> None:
        notification = None
        while True:
            self._print_rows(
                self._header(
                    'Nytt spel',
                    'Lägg till spelare'
                ),
                notification,
                'Skriv namn på spelare',
                '0. Avbryt'
            )
            notification = None
            opt = input('>>> ')
            if opt == '0':
                return
            else:
                if opt in self.game.player_names():
                    notification = 'Namn upptaget'
                    continue
                while True:
                    confirm = input(f'Använd spelarnamn {opt}? (j/n)').lower()
                    if confirm == 'j':
                        self.game.add_player(player_name = opt)
                        return
                    elif confirm == 'n':
                        break
                    else:
                        print('Ogiltigt kommando')

    def _remove_player_menu(self) -> None:
        notification = None
        while True:
            self._print_rows(
                self._header(
                    'Nytt spel',
                    'Ta bort spelare'
                ),
                notification,
                *[name for name in self.game.player_names()],
                'Skriv namn på spelaren du vill ta bort',
                '0. Avbryt'
            )
            notification = None
            opt = input('>>> ')
            if opt == '0':
                return
            elif opt in self.game.player_names():
                self.game.remove_player(player_name = opt)
            else:
                notification = 'Ingen spelare har det namnet'

    def _play_game(self) -> None:
        self.game.set_turn_order()
        for turn in self.game.turns():
            self._player_turn(turn)
        
        players = self.game.get_players(ordered = True)
        winner = players[-1]
        while True:
            self._print_rows(
                self._header('Spelslut'),
                f'{winner.name} har vunnit spelet med {winner.total_score()}',
                '### Slutranking ###',
                *[f'{index + 1} - {player.name}: {player.total_score()}' for index, player in enumerate(players)],
                '0: Tillbaka till huvudmenyn'
            )
            while True:
                opt = input('>>> ')
                if opt == '0':
                    return
                else:
                    print('Ogiltigt kommando')

    def _player_turn(self, turn: Turn) -> None:
        turn.roll_dice()
        notification = None
        while turn.die_rolls < 3:
            self._print_rows(
                self._header(
                    f'Tur {turn.turn_num}: {turn.player.name}',
                    f'Slag {turn.die_rolls}/3'
                ),
                'Välj tärning att låsa eller låsa upp innan nästa tärningsslag',
                *self._display_dice(turn.get_dice(), rolling = True),
                '1. Slå olåsta tärningarna',
                '0. Gå till poängsättning',
                notification
            )
            notification = None
            opt = input('>>> ').lower()
            if opt == '0':
                break
            elif opt == '1':
                turn.roll_dice()
            else:
                die = turn.get_die(opt)
                if die:
                    die.toggle_lock()
                else:
                    notification = 'Ogiltigt kommando'
        
        self._score_points(turn)

    def _score_points(self, turn: Turn) -> None:
        dice_values = turn.get_dice_pips(ordered = True)
        slot_list: list[str] = []
        slot_dict: dict[str, Slot] = {}
        for index, slot in enumerate(turn.player.table.get_slots()):
            opt = str(index + 1)
            if slot.is_scorable():
                slot_dict[opt] = slot
                slot_list.append(f'{opt}: {slot} ({slot.calculate_score(dice_values)})')
            else:
                slot_list.append(f'   {slot} {slot.score}')
        
        notification = None
        while not turn.scored:
            self._print_rows(
                self._header(
                    f'Tur {turn}: {turn.player.name}',
                    'Poängsättning'
                ),
                *self._display_dice(turn.get_dice(ordered = True)),
                *slot_list,
                notification
            )
            notification = None
            opt = input('>>> ')
            if opt in slot_dict.keys():
                chosen_slot = slot_dict[opt]
                chosen_slot.set_score(dice_values)
                turn.scored = not chosen_slot.is_scorable()
                if turn.scored and slot.is_upper():
                    turn.player.table.verify_bonus()
            else:
                notification = 'Ogiltigt kommando'
    
    def _print_rows(self, *rows: str) -> None:
        self._new_screen()
        for row in rows:
            if row != None:
                print(row)
    
    def _header(self, *messages: str) -> str:
        header = '### YATZY'
        for message in messages:
            header += f' - {message}'
        header += ' ###'
        return header
    
    def _display_dice(self, dice: list[Die], rolling = False):
        dice_rows = zip(*[die.display() for die in dice])
        dice_rows = ['  '.join(row) for row in dice_rows]
        dice_rows = [' ' + row for row in dice_rows]
        if rolling:
            dice_rows.insert(0, ''.join([f'    {char}    ' for char in string.ascii_lowercase[:len(dice)]]))
            dice_rows.append(''.join([f'  låst   ' if die.is_locked else '         ' for die in dice]))
        return dice_rows

    def _new_screen(self):
        '''
        Clears the screen, for windows and unix
        '''
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
