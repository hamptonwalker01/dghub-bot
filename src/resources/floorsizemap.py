from src.resources.floorsize import FloorSize
from src.resources.floortheme import FloorTheme


class FloorSizeMap():
    def __determine_floor_size(self, floor_number: int, level: int, subs: bool) -> FloorSize:
        """Determine the type of floor based on specific levels."""
        if level <= 34:
            return FloorSize.MED

        if subs:
            if level <= 48:
                if floor_number <= 15:
                    return FloorSize.RUSH
                else:
                    return FloorSize.MED
            elif level <= 69:
                if floor_number <= 24:
                    return FloorSize.RUSH
                else:
                    return FloorSize.LARGE
            else:
                if floor_number <= 35:
                    return FloorSize.RUSH
                else:
                    return FloorSize.LARGE
        else:
            if level <= 58:
                if floor_number <= 11:
                    return FloorSize.RUSH
                return FloorSize.MED
            elif level <= 69:
                if floor_number <= 24:
                    return FloorSize.RUSH
                elif floor_number <= 29:
                    return FloorSize.MED
                return FloorSize.LARGE
            else:
                if floor_number <= 29:
                    return FloorSize.RUSH
                return FloorSize.LARGE

    def determine_floor_theme(self, floor_number: int, floor_size: FloorSize) -> FloorTheme:
        if floor_size == FloorSize.RUSH:
            return FloorTheme.C1
        elif floor_size == FloorSize.MED:
            return FloorTheme.MED
        elif floor_size == FloorSize.LARGE:
            if floor_number <= 35:
                return FloorTheme.ABA
            elif floor_number <= 47:
                return FloorTheme.OCC
            elif floor_number <= 56:
                return FloorTheme.WARP
        return FloorTheme.HW

    def get_floor_size(self, level: int, floor: int, subs: bool):
        return self.__determine_floor_size(floor, level, subs)
