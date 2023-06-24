from discord import Embed
from datetime import datetime
from data.bot_data import COLOURS


def str_to_int(s: str) -> int:
    l = s.lower()  # lowercase to standardize (also Jagex password reference)
    offset = 1
    # ignore inputs over 16 characters cause who is trying to buy trillions of tokens
    if len(s) > 16:
        return None
    # search for k/m and "multiply" appropriately + dealing with decimals
    l = l.replace(",", '')
    k_flag, m_flag, p_flag = l.find('k'), l.find('m'), l.find('.')
    if k_flag != -1 and m_flag != -1:  # if both k & m are present in string this is not a valid input
        return None
    elif k_flag > 0:  # multiply by 1000
        l = l.replace('k', '000')
    elif m_flag > 0:  # multiply by 1000000
        l = l.replace('m', '000000')
    if p_flag > 0:  # if user provided a decimal
        offset = 10 ** (max(m_flag, k_flag) - (p_flag + 1))
        l = l.replace('.', '')

    try:  # return integer with k/m replaced
        r = int(l)
        if r < 0:
            return None
        return r // offset
    except:  # user provided invalid input
        return None


# removing trailing 0's at the end of a string
def remove_decimal(s: str) -> str:
    p = s.find('.')
    if p == -1:
        return s
    if s[-2:] == ".0":
        return s[:-2]
    idx = len(s) - 1
    while idx > p:
        if s[idx] != "0":
            break
        s[idx] = ''
        idx -= 1
    return s

# adds commas to an int we just casted to a string


def int_to_str(s) -> str:
    _s = str(s)
    p_idx = _s.find('.')
    if p_idx == -1 and len(_s) > 3:
        p_idx = len(_s)
    while p_idx > 3:
        _s = _s[:p_idx - 3] + ',' + _s[p_idx - 3:]
        p_idx -= 3
    return _s

# Converting a given price to a human readable format


def price_to_str(p: int) -> str:
    ks = p / 1_000
    if ks < 1_000:
        k = remove_decimal(str(ks))
        k = int_to_str(k)
        return f"{k}K"
    mils = p / 1_000_000
    b_flag = True if mils >= 10_000 else False
    b = remove_decimal(
        str(mils / 1_000)) if b_flag else remove_decimal(str(p / 1_000_000))

    b = int_to_str(b)

    b += "B" if b_flag else "M"
    return b


def minutes_to_text(minutes) -> str:
    hours, mins = minutes // 60, minutes % 60
    h_format = f"{int(hours)} hours" if hours != 1 else "1 hour"
    m_format = f"{int(mins)} minutes" if mins != 1 else "1 minute"
    if hours > 0:
        return h_format if mins == 0 else h_format + " and " + m_format
    return m_format


def custom_error(exception, msg):
    embed = Embed(
        title=f"ERROR",
        colour=COLOURS['error'],
        timestamp=datetime.now()
    )
    embed.add_field(
        name=exception,
        value=msg,
        inline=False
    )
    return embed
