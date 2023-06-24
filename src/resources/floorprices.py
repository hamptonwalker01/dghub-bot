from src.resources.floortheme import FloorTheme
from collections import Counter
from src.helpers.utils import price_to_str


class FloorPrices(object):
    def __init__(self, rush_price, med_price, large_price, token_price, carded_price):
        self.rush = rush_price
        self.med = med_price
        self.large = large_price
        self.tokens = token_price
        self.cards = carded_price
        pass

    def calc_large_price(self, tokens: bool, carded: bool):
        base = self.large
        if carded:
            return self.cards
        elif tokens:
            return base + self.tokens
        return base

    # returns price of med + large floors and price including rushes

    def get(self, counts: Counter, tokens: bool, carded: bool) -> tuple[str, str]:
        price, rush_price = 0, counts[FloorTheme.C1] * self.rush
        price += counts[FloorTheme.MED] * self.med  # med floor calculation
        price += (counts[FloorTheme.ABA] + counts[FloorTheme.OCC] +
                  counts[FloorTheme.WARP] + counts[FloorTheme.HW]) * self.calc_large_price(tokens, carded)
        return price_to_str(price), price_to_str(price + rush_price)


# Initialize price objects
# Main Account Floor Prices
BASE_PRICES = FloorPrices(1_500_000, 4_000_000, 8_000_000,
                          1_000_000, 25_000_000)
# Iron Account Floor Prices
IRON_PRICES = FloorPrices(2_000_000, 10_000_000, 25_000_000,
                          5_000_000, 80_000_000)
# DXP Prices (Mains only)
DXP_PRICES = FloorPrices(1_500_000, 4_000_000, 20_000_000,
                         1_000_000, 30_000_000)

# Keyed by (Iron, Dxp)
PRICES = {
    (True, True): IRON_PRICES,
    (True, False): IRON_PRICES,
    (False, True): DXP_PRICES,
    (False, False): BASE_PRICES
}
