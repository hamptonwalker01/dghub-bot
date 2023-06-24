from bs4 import BeautifulSoup
import requests
from src.resources import FloorSize, FloorStats, FloorSizeMap
# webscrape the xp table from the rs wiki


def get_xp_table() -> dict[int]:
    page = requests.get("http://runescape.wiki/w/Experience/Table")
    soup = BeautifulSoup(page.text, "html.parser")
    xp_table = {}
    tables = soup.find_all('table')[0:2]
    for idx, table in enumerate(tables):
        parsed = table.find_all(
            'td')[:-1] if idx == 0 else table.find_all('td')
        for idx, i in enumerate(parsed[::3]):
            level = int(i.text)
            offset = 3*idx + 1
            xp_table[level] = int(parsed[offset].text.replace(',', ''))
    return {k: xp_table[k] for k in range(1, 121)}


XP_TABLE = get_xp_table()


def level_to_xp(lvl: str) -> int:
    try:
        level = int(lvl)
        if level not in XP_TABLE:
            return None
        return XP_TABLE[level]
    except ValueError:
        return None


def xp_to_level(exp: int) -> int:
    for key, value in XP_TABLE.items():
        if exp > value:
            continue
        if exp == value:
            return key
        return key - 1
    return 120


def determine_floor_mod(floor_size: FloorSize) -> float:
    floor_mods = {
        FloorSize.RUSH: 0,
        FloorSize.MED: 1.1,
        FloorSize.LARGE: 1.33
    }
    return floor_mods.get(floor_size, 0)


# stolen from James calc, no idea how this works
def base_floor_xp(pn, fn, floor_size: FloorSize) -> int:
    # Magic numbers yay?
    if floor_size == FloorSize.RUSH:
        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
    elif floor_size == FloorSize.MED:
        m1 = 0.0012
        m2 = -0.0203
        m3 = 0.8909
        m4 = 3.5366
        c1 = 0.3833
        c2 = -8.9034
        c3 = 272.45
        c4 = 838.82
    elif floor_size == FloorSize.LARGE:
        m1 = 0.0015
        m2 = 0.0026
        m3 = 1.2126
        m4 = 8.8089
        c1 = 0.3807
        c2 = 3.4423
        c3 = 263.03
        c4 = 2015

    m = m1 * pn**3 + m2 * pn**2 + m3 * pn + m4
    c = c1 * pn**3 + c2 * pn**2 + c3 * pn + c4
    y = m * fn + c
    return y

# Calculate XP/Token multiplier based off of user-inputted boosts


def calc_mult(floor_size: FloorSize, subs: bool, token_cards: bool,
              xp_cards: bool, iron: bool, dxp: bool, *args):
    args = args[0] or None
    dxp = dxp and not iron
    outfit_xp = 7 if args and "Outfit" in args else 0
    outfit_tokens = outfit_xp
    card_xp, card_tokens = 0, 0

    if subs:
        if floor_size != FloorSize.RUSH:
            card_xp = 150
            card_tokens = 100

            outfit_xp *= 2.5
            outfit_tokens *= 2

    elif floor_size == FloorSize.LARGE:
        if xp_cards:
            card_xp = 150
            outfit_xp *= 2.5

        if token_cards:
            card_tokens = 100
            outfit_tokens *= 2

    mult = 0
    mult += (dxp + 1) * card_xp
    mult += outfit_xp
    if args:
        mult += 2 if "Torstol Sticks" in args else 0
        mult += 10 if "Pulse Cores" in args else 0
        mult += 6 if "Clan Avatar" in args else 0
        mult += 10 if "RAF Scroll" in args else 0
        mult += 2 if "Inspire Love" in args else 0
        mult += 20 if "Yak Track" in args and not dxp else 0
        mult += 50 if "Knowledge Bomb" in args and not dxp else 0
        mult += 4 if "Sceptre" in args else 0
        mult += 2 if "Coin" in args else 0

    fin = round(mult / 100 + (1 + dxp), 3)
    token_mult = round(1 + (outfit_tokens + card_tokens) / 100, 3)
    return fin, token_mult


def gainz_from_floor(
    floor_number: int,
    prestige: int,
    bonus_xp: int,
    floor_size: FloorSize,
    subs: bool,
    token_cards: bool,
    xp_cards: bool,
    iron: bool,
    dxp: bool,
    *args: any
) -> int:
    if floor_number > prestige:
        prestige = floor_number

    floor_xp = base_floor_xp(floor_number, floor_number, floor_size)
    prestige_xp = base_floor_xp(prestige, floor_number, floor_size)
    xp_mult, token_mult = calc_mult(
        floor_size, subs, token_cards, xp_cards, iron,  dxp, args[0])

    mod = determine_floor_mod(floor_size)
    base_xp = round((floor_xp + prestige_xp) / 2) * mod
    total_xp = base_xp * xp_mult
    total_tokens = base_xp * token_mult / 10

    if bonus_xp > 0:
        total_xp += base_xp
        bonus_xp -= base_xp if bonus_xp >= base_xp else bonus_xp

    return total_xp, total_tokens, bonus_xp


def get_current_floor(level: int):
    if level < 23:
        return 1
    elif level < 35:
        return 12
    elif level < 59:
        return 18
    elif level < 65:
        return 27
    elif level < 85:
        return 30
    else:
        return ((level + 1) // 2) - 12


def calculate(map: FloorSizeMap,
              start: int,
              end: int,
              bonus: int,
              subs: bool,
              token_cards: bool,
              xp_cards: bool,
              iron: bool,
              dxp: bool,
              *args):
    bonus_xp = bonus
    stats = FloorStats(start, iron, dxp, xp_cards, token_cards, subs)
    lvl = xp_to_level(start)
    prestige = (lvl + 1) // 2
    current_floor = get_current_floor(lvl)
    current_xp, current_tokens = start, 0
    while current_xp < end:
        check = (lvl + 1) // 2
        if current_floor > check:
            prestige = check
            current_floor = 1
        floor_size = map.get_floor_size(lvl, current_floor, subs)
        xp_gainz, token_gainz, bonus_xp = gainz_from_floor(
            current_floor, prestige, bonus_xp, floor_size, subs, token_cards, xp_cards, iron, dxp, args[0])
        current_xp += xp_gainz
        current_tokens += token_gainz
        if lvl < 120:
            lvl = xp_to_level(current_xp)
        stats.update(map.determine_floor_theme(current_floor, floor_size))
        current_floor += 1
    stats.end_tokens = round(current_tokens)
    stats.end_xp = round(current_xp)
    return stats
