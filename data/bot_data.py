TEST_SERVERS = [597564088972869633, 1122248392635064390, 719547175763443803]

COLOURS = {
    'default': 0x7d45a8,
    'ed': 0xc1210f,
    'error': 0XED4337,
    'prefloor': 0xDC7412,
    'Frozen': 0x99DBF5,
    'Abandoned': 0xE8AA42,
    'Furnished': 0xEF9A53,
    'Occult': 0x674188,
    'Warped': 0xB70404,
    'Regular': 0x3498DB,
    'Premium': 0x3F8434
}

LINKS = {
    "Logo": "https://i.imgur.com/JeT2OC1.png",
    "Premium": "https://i.imgur.com/WaEdzy4.png",
    "Regular": "https://i.imgur.com/Z7U81Rl.png",
    "Tokens": "https://i.imgur.com/rTM6Ft5.png",
}

EMOJIS = {
    "pc": {
        "Cards": {
            "DGH_Token": "<:DGH_Token:692021706893819925>",
            "XP_cards": "<:XP_cards:858372407592222760>",
        },
        "Iron": {
            "outfit": "<:outfit:719732079360999464>",
            "torstol_sticks": "<:torstolsticks:814897581343113216>",
            "inspire_love": "<:inspire_love:814916964610211920>",
        },
        "Premium": {
            "DGH_DXPW": "<:DGH_DXPW:698433263617966140>",
            "knowledge_bomb": "<:knowledge_bomb:977301191400783933>",
            "yak_track": "<:yak_track:977301191325274203>",
            "pulsecore": "<:pulsecore:814897581355696168>",
            "raf": "<:raf:814900337356963910>",
            # "premierartefact": "<:premierartefact:814897581225410590>",
            "vex": "<:vex:815757341756358717>",
            "sceptre_of_enchantment": "<:sceptre_of_enchantment:977301191077806082>",
            "coin_of_enchantment": "<:coin_of_enchantment:977301191136522292>",
        }
    },
    "about": {
        "bot": "<:bot:735442459991212043>",
        "online": "<:status_online:719731694168702996>",
        "offline": "<:status_offline:719731682294366319>",
    }
}

BUFF_MAP = {
    "XP_cards": {"name": "2.5x XP Cards",
                 "value": f"+150% XP"},  # no premium
    "DGH_Token": {"name": "Double Tokens",
                  "value": f"+100% Tokens"},  # no premium
    "DGH_DXPW": {"name": "DXPW",
                 "value": f"2x XP (multiplicative)"},  # no iron
    "knowledge_bomb": {"name": "Knowledge Bomb",
                       "value": f"+50% XP"},  # no iron
    "pulsecore": {"name": "Pulse Cores",
                  "value": f"+10% XP"},  # no iron
    "vex": {"name": "Clan Avatar",
            "value": f"+3-6% XP"},  # no iron
    "raf": {"name": "RAF Scroll",
            "value": f"+50% XP"},  # no iron
    "sceptre_of_enchantment": {"name": "Sceptre",
                               "value": f"+2/4% XP"},  # no iron
    "coin_of_enchantment": {"name": "Coin",
                            "value": f"+1/2% XP"},
    "yak_track": {"name": "Yak Track",
                  "value": f"+0%-20%"},  # no iron
    "outfit": {"name": "Outfit",
               "value": f"+7% XP and Tokens"},
    "torstol_sticks": {"name": "Torstol Sticks",
                       "value": f"+2% XP"},
    "inspire_love": {"name": "Inspire Love",
                     "value": f"+2% XP"},
}
FLOOR_THEMES = {}
