from collections import Counter
from src.helpers.utils import price_to_str, minutes_to_text, int_to_str, str_to_int
from math import ceil
from src.resources.floorprices import PRICES
from src.resources.floortimes import EXPECTED_TIMES
from src.resources.floortheme import FloorTheme


class FloorStats():
    def __init__(self, start_xp: int, iron: bool, dxp: bool, carded: bool, token_cards: bool, subs: bool):
        self.start_xp = start_xp
        self.start_tokens, self.end_xp, self.end_tokens = 0, 0, 0
        self.iron, self.dxp, self.carded, self.token_cards = iron, dxp, carded, token_cards
        self.subs = subs
        self.floors = Counter({
            FloorTheme.C1: 0,
            FloorTheme.MED: 0,
            FloorTheme.ABA: 0,
            FloorTheme.OCC: 0,
            FloorTheme.WARP: 0,
            FloorTheme.HW: 0
        })

    def update(self, theme: FloorTheme):
        self.floors.update({theme: 1})

    def get_subs_prices(self):
        return {
            "Affordable": {
                True: "405m",
                False: "240m"
            },
            "Premium": {
                True: "1,100m",
                False: "680m"
            }
        }

    def get_subs_cost(self):
        prices = self.get_subs_prices()
        affordable, premium = str_to_int(prices["Affordable"][self.dxp]),\
            str_to_int(prices["Premium"][self.dxp])
        floors = sum(self.get_num_floors())
        affordable_hours, premium_hours = ceil(floors / 9), ceil(floors / 12)
        affordable_cost = price_to_str(affordable * affordable_hours)
        premium_cost = price_to_str(premium * premium_hours)
        affordable_time = minutes_to_text(affordable_hours * 60)
        premium_time = minutes_to_text(premium_hours * 60)
        return [(affordable_cost, affordable_time), (premium_cost, premium_time)]

    def get_time_and_cost(self):
        if self.subs:
            return self.get_subs_cost()
        # price without/with rushes
        default_p, rush_p = PRICES[(self.iron, self.dxp)].get(
            self.floors, self.token_cards, self.carded)
        default_t, rush_t = EXPECTED_TIMES.get(self.floors)
        return [(default_p, minutes_to_text(default_t)), (rush_p, minutes_to_text(rush_t))]

    def get_total_xp(self):
        return int_to_str(self.end_xp - self.start_xp)

    def get_tokens(self):
        return int_to_str(self.end_tokens)

    def get_num_floors(self):
        return list(self.floors.values())[1:]
