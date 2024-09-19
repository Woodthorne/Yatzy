class Slot:
    def __init__(self) -> None:
        self._score = None

    @property
    def score(self) -> int:
        if self.is_scorable():
            return 0
        else:
            return self._score
    
    def set_score(self, dice_values: list[int]) -> None:
        self._score = self.calculate_score(dice_values)

    def calculate_score(self, dice_values: list[int]) -> int|None:
        # Logic for calculating possible score
        if self.is_scorable():
            return 0
        return None
    
    def is_scorable(self) -> bool:
        if self._score == None:
            return True
        return False
    
    def is_upper(self) -> bool:
        return issubclass(self.__class__, Upper)
    
    def __str__(self) -> str:
        return self.__class__.__name__


class Upper(Slot):
    def calculate_score(self, dice_values: list[int], target: int) -> bool:
        if self.is_scorable():
            return sum(die for die in dice_values if die == target)
        return None


class Matching(Slot):
    def calculate_score(self, dice_values: list[int], matches: int) -> bool:
        if self.is_scorable():
            sorted_dice = sorted(dice_values, reverse = True)
            for index in range(matches - 1, len(sorted_dice)):
                checking_dice = [sorted_dice[index - shift] for shift in range(matches)]
                valid = True
                for die in checking_dice:
                    if checking_dice[0] != die:
                        valid = False
                        break
                if valid:
                    return sum(checking_dice)
            return 0
        return None


class Straight(Slot):
    def calculate_score(self, dice_values: list[int], target_dice: list) -> bool:
        if self.is_scorable():
            sorted_dice = sorted(dice_values)
            if sorted_dice == target_dice:
                return sum(dice_values)
            return 0
        return None


class Ones(Upper):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target = 1)
    
    def __str__(self) -> str:
        return 'Ettor'


class Twos(Upper):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target = 2)
    
    def __str__(self) -> str:
        return 'Tvåor'


class Threes(Upper):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target = 3)
    
    def __str__(self) -> str:
        return 'Treor'


class Fours(Upper):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target = 4)
    
    def __str__(self) -> str:
        return 'Fyror'


class Fives(Upper):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target = 5)
    
    def __str__(self) -> str:
        return 'Femmor'


class Sixes(Upper):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target = 6)
    
    def __str__(self) -> str:
        return 'Sexor'


class Bonus(Slot):
    @property
    def score(self) -> int:
        if self._score == None:
            return 0
        else:
            return self._score

    def verify(self, upper_points: list[int]) -> None:
        if self._score == None:
            total_upper = sum(upper_points)
            if total_upper >= 63:
                self._score = 50
    
    def is_scorable(self) -> bool:
        return False

    def __str__(self) -> str:
        return 'Bonus'


class Pair(Matching):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, matches = 2)
    
    def __str__(self) -> str:
        return 'Par'


class Pairs(Slot):
    def calculate_score(self, dice_values: list[int]) -> bool:
        if self.is_scorable():
            sorted_dice = sorted(dice_values, reverse = True)
            scored = None
            score_1 = None
            score_2 = None
            for index in range(1, len(sorted_dice)):
                die_1 = sorted_dice[index]
                die_2 = sorted_dice[index - 1]
                if die_1 == die_2:
                    if not scored:
                        score_1 = die_1 + die_2
                        scored = [index, index - 1]
                    elif index not in scored and index - 1 not in scored:
                        score_2 = die_1 + die_2
            if score_1 and score_2:
                return score_1 + score_2
            return 0
        return None

    def __str__(self) -> str:
        return 'Två par'


class Triple(Matching):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, matches = 3)
    
    def __str__(self) -> str:
        return 'Tretal'


class Quadruple(Matching):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, matches = 4)
    
    def __str__(self) -> str:
        return 'Fyrtal'


class StraightSmall(Straight):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target_dice = [1, 2, 3, 4, 5])
    
    def __str__(self) -> str:
        return 'Liten stege'


class StraightLarge(Straight):
    def calculate_score(self, dice_values: list[int]) -> bool:
        return super().calculate_score(dice_values, target_dice = [2, 3, 4, 5, 6])
    
    def __str__(self) -> str:
        return 'Stor stege'


class House(Slot):
    def calculate_score(self, dice_values: list[int]) -> bool:
        if self.is_scorable():
            sorted_dice = sorted(dice_values, reverse = True)
            biggest = sorted_dice[0]
            smallest = sorted_dice[1]

            big_count = 0
            small_count = 0
            for index in range(len(sorted_dice)):
                if sorted_dice[index] == biggest:
                    big_count += 1
                if sorted_dice[len(sorted_dice) - 1 - index] == smallest:
                    small_count += 1
            
            if {big_count, small_count} == {2, 3}:
                return sum(dice_values)
            return 0
        return None
    
    def __str__(self) -> str:
        return 'Kåk'


class Chance(Slot):
    def calculate_score(self, dice_values: list[int]) -> bool:
        if self.is_scorable():
            return sum(dice_values)
        return None
    
    def __str__(self) -> str:
        return 'Chans'


class Yatzy(Matching):
    def calculate_score(self, dice_values: list[int]) -> bool:
        if super().calculate_score(dice_values, matches = 5):
            return 50
        return None
    
    def __str__(self) -> str:
        return 'Yatzy'

