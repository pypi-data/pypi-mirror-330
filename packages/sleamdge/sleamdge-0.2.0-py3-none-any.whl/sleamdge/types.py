from enum import IntEnum


class ParentType(IntEnum):
    GROUP = 1
    CLAN = 2


class Parent:
    __slots__ = "type", "id"

    def __init__(self, type_: ParentType, parent_id: int):
        self.type = type_
        self.id = parent_id


class ChannelId:
    __slots__ = "parent", "channel_id"

    def __init__(self, parent: Parent, channel_id: int):
        self.parent = parent
        self.channel_id = channel_id

    def __repr__(self):
        return f"{self.parent.type.value}-{self.parent.id}-{self.channel_id}"

    def __hash__(self):
        return hash(str(self))

    @classmethod
    def from_str(cls, string):
        parent_type_int, parent_id, channel_id = (int(x) for x in string.split("-"))
        parent = Parent(ParentType(parent_type_int), parent_id)
        return cls(parent, channel_id)
