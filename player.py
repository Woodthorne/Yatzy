from slots import (
    Slot, Ones, Twos, Threes, Fours, Fives, Sixes, Bonus, Pair, Pairs,
    Triple, Quadruple, StraightSmall, StraightLarge, House, Chance, Yatzy
)


class ScoreTable:
    def __init__(self) -> None:
        self._ones = Ones()
        self._twos = Twos()
        self._threes = Threes()
        self._fours = Fours()
        self._fives = Fives()
        self._sixes = Sixes()
        self._bonus = Bonus()

        self._pair = Pair()
        self._pairs = Pairs()
        self._triple = Triple()
        self._quadruple = Quadruple()
        self._straight = StraightSmall()
        self._Straight = StraightLarge()
        self._house = House()
        self._chance = Chance()
        self._yatzy = Yatzy()

    def get_slots(self) -> list[Slot]:
        return [
            self._ones,
            self._twos,
            self._threes,
            self._fours,
            self._fives,
            self._sixes,
            self._bonus,
            self._pair,
            self._pairs,
            self._triple,
            self._quadruple,
            self._straight,
            self._Straight,
            self._house,
            self._chance,
            self._yatzy,
        ]

    def verify_bonus(self) -> None:
        upper_scores = [slot.score for slot in self.get_slots() if slot.is_upper()]
        self._bonus.verify(upper_scores)
    
    def total_score(self) -> int:
        score = 0
        for slot in self.get_slots():
            score += slot.score
        return score


class Player:
    def __init__(self, name: str) -> None:
        self._name = name
        self.table = ScoreTable()

    @property
    def name(self) -> str:
        return self._name

    def total_score(self) -> int:
        return self.table.total_score()
    
    def is_done(self) -> bool:
        for slot in self.table.get_slots():
            if slot.is_scorable():
                return False
        return True
    