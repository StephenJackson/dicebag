import random
import re

class DiceBag(object):
    def __init__(self, default_sides, default_min_hit=None):
        self.default_sides = default_sides
        self.default_min_hit = default_min_hit
        self.expression_dict_keys = ["base", "dice_num", "action", "sides", "mod", "percent", "dc"]
        self.default_regex = "(\d*[+])?(\d*)([a-zA-Z]*)(\d*)([+-]\d+)?([.]\d+)?([dD][cC]\d+)?"

    #Basic rolling function. dice.roll(int) I think is more clear than random.randint(1, x).
    #This method defaults to self.default_sides.
    def roll(self, sides=None):
        """ [sides = int]. Inclusive max return int. defaults if no arg given."""
        if not sides:
            sides = self.default_sides
        if sides <= 0:
            return None
        return random.randint(1, sides)

    #For exploding dice. TODO: add support for range rather than just max result.
    def explode(self, sides=None):
        if not sides:
            sides = self.default_sides
        #prevent infinite recursion
        if sides <= 1:
            return None
        result = self.roll(sides)
        if result == sides:
            result += self.explode(sides)
        return result

    #Regex magic. This should cover any dice rolling system besides a dicepool hit system.
    #roller interfaces for those should replace the default regex and expression dict keys.
    def rollexpression(self, stringin, appmethod, appexpression=None, flags=None):
        """ 
        args: stringin = string, appmethod = AppInterface method, [appexpression = special regex, flags = flags for special regex]
        takes in string and applies regex to find dice roll params. returns dict of values num_dice, dice_action, sides, mod, dc 
        """
        if not appexpression:
            m = re.match(self.default_regex, stringin)
        else:
            m = re.match(appexpression, stringin, flags)
        if m.group():
            m_iter = [m.group(x) for x in range(1,8)]
            appmethod(dict(zip(self.expression_dict_keys, m_iter)))
        else:
            print "~Sorry, I did not understand you."

    #similar to roll, but for roll hit systems. It can be used alone but the standard case is to roll alot of dice.
    #max included for edge cases where the max dice size is not a hit
    #TODO: stop infinite recursion case where min or sides <= 1
    def _hit(self, min_, sides=None, exp=False, max_=None):
        """ min_ = int, [sides = int], [exp = bool], [max_ = int] returns int """
        result = roll(sides)
        if not max_:
            max_ = sides
        if result >= min_ and result <= max_:
            hits = 1
            if exp and result == sides:
                hits += self.hit(sides, min_, exp, max_)
            return hits

    #Interfaces for roll hit dicepool systems should use this.
    def roll_hits(self, times, min_=None, sides=None, exp=False, max_=None):
        """ times, min_=None, sides=None, exp=False, max_=None, returns int """
        result = 0
        if not sides:
            sides = self.default_sides
        if not min_ and self.default_min_hit:
            min_ = self.default_min_hit
        for x in range(times):
            result += self.hit(min_, sides, exp, max_)

    #For when you just need to roll ALOT of dice.
    def roll_many(self, times, sides=None, explode=False):
        """ times = int, [sides = int], [explode = bool]. returns list """
        if sides == None:
            sides = self.default_sides
        if explode:
            return [self.explode(sides) for x in range(times)]
        return [self.roll(sides) for x in range(times)]

    #easy mass modding a list of rolls.
    #TODO: add lambda support for mod
    def rolls_with_mod(self, rolls, mod):
        """ rolls = list of ints, mod = int, returns list """
        return [x + mod for x in rolls]

    #probably not needed but nice for readability.
    def total_bonus(self, rolls, bonus):
        """ rolls = list or int, bonus = int, returns int  """
        return sum(rolls) + bonus

    #similar to bonus, does comparisons and returns list
    #TODO: add lambda support for comparisons
    def dc_cmp(self, rolls, dc):
        """ rolls = int or list, dc = int, returns list """
        return [x - dc for x in rolls]

    #Percentages come up in some systems. This will take a value and a float and return an int
    def percent(self, x, percent_float):
        """ x = int or float, percent_float = float """
        if not perfloat < 0.0:
            return int(x * percent_float)
