from src.resources.floortheme import FloorTheme
from collections import Counter


class FloorTimes():
    def __init__(self, rush, med, large):
        self.rush = rush
        self.med = med
        self.large = large

    def get(self, floors: Counter):
        total, rushes = 0, 0
        for key, value in floors.items():
            if key == FloorTheme.C1:
                rushes += value * self.rush
            elif key == FloorTheme.MED:
                total += value * self.med
            else:
                total += value * self.large
        return total, total + rushes


EXPECTED_TIMES = FloorTimes(1.5, 6, 10)
