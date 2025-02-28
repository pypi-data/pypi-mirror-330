import steam

EMOJIS = dict[str, str](
    [
        ("steamthumbsup", "👍"),
        ("steamthumbsdown", "👎"),
        ("steambored", "🥱"),
        ("steamfacepalm", "🤦"),
        ("steamhappy", "😄"),
        ("steammocking", "😝"),
        ("steamsalty", "🧂"),
        ("steamsad", "😔"),
        ("steamthis", "⬆"),
    ]
)
EMOJIS_INVERSE = {v: k for k, v in EMOJIS.items()}
EMOJIS_SET = set(EMOJIS.values())


def emojize(emoticon: steam.Emoticon) -> str:
    return EMOJIS.get(emoticon.name, "❔")


def demojize(emoji: str) -> str:
    return EMOJIS_INVERSE[emoji]
