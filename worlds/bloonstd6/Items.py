from typing import Dict, List, Optional
from BaseClasses import Item, ItemClassification
from worlds.bloonstd6.Locations import BloonsLocations
from .Utils import Shared


class BTD6MedalItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(
            name,
            ItemClassification.progression_skip_balancing,
            code,
            player,
        )


class BTD6MapUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6MonkeyUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)

class BTD6HeroUnlock(Item):
    game: str = "Bloons TD6"
    
    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)

class BTD6KnowledgeUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6ProgressiveKnowledge(Item):
    game: str = "Bloons TD6"

    def __init__(self, code: Optional[int], player: int):
        super().__init__("Progressive Knowledge", ItemClassification.useful, code, player)


class BTD6ProgressivePrices(Item):
    game: str = "Bloons TD6"

    def __init__(self, code: Optional[int], player: int):
        super().__init__("Progressive Prices", ItemClassification.useful, code, player)


class BTD6CategoryUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6TrapItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.trap, code, player)


class BTD6FillerItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.filler, code, player)


class BloonsItems:
    MEDAL_NAME: str = "Medal"
    MEDAL_CODE: int = 1

    MONEY_NAME: str = "Monkey Money"
    MONEY_CODE: int = 2

    PROGRESSIVE_KNOWLEDGE_NAME: str = "Progressive Knowledge"
    PROGRESSIVE_KNOWLEDGE_CODE: int = 999

    PROGRESSIVE_PRICES_NAME: str = "Progressive Prices"
    PROGRESSIVE_PRICES_CODE: int = 1000

    CATEGORY_PRIMARY_NAME: str = "Primary Monkeys"
    CATEGORY_PRIMARY_CODE: int = 1001
    CATEGORY_MILITARY_NAME: str = "Military Monkeys"
    CATEGORY_MILITARY_CODE: int = 1002
    CATEGORY_MAGIC_NAME: str = "Magic Monkeys"
    CATEGORY_MAGIC_CODE: int = 1003
    CATEGORY_SUPPORT_NAME: str = "Support Monkeys"
    CATEGORY_SUPPORT_CODE: int = 1004

    MODIFIED_BLOONS_NAME: str = "Modified Bloons"
    MODIFIED_BLOONS_CODE: int = 1005

    FREEZE_TRAP_NAME: str = "Freeze Trap"
    FREEZE_TRAP_CODE: int = 1006

    BEE_TRAP_NAME: str = "Bee Trap"
    BEE_TRAP_CODE: int = 1007

    SPEED_UP_TRAP_NAME: str = "Speed Up Trap"
    SPEED_UP_TRAP_CODE: int = 1008

    LITERATURE_TRAP_NAME: str = "Literature Trap"
    LITERATURE_TRAP_CODE: int = 1009

    MONKEY_BOOST_NAME: str = "Monkey Boost"
    MONKEY_BOOST_CODE: int = 1010

    MONKEY_STORM_NAME: str = "Monkey Storm"
    MONKEY_STORM_CODE: int = 1011

    CASH_DROP_NAME: str = "Cash Drop"
    CASH_DROP_CODE: int = 1012

    category_names: List[str] = [
        "Primary Monkeys",
        "Military Monkeys",
        "Magic Monkeys",
        "Support Monkeys",
    ]

    category_towers: Dict[str, List[str]] = {
        "Primary Monkeys": ["DartMonkey", "BoomerangMonkey", "BombShooter", "TackShooter", "IceMonkey", "GlueGunner", "Desperado"],
        "Military Monkeys": ["SniperMonkey", "MonkeySub", "MonkeyBuccaneer", "MonkeyAce", "HeliPilot", "MortarMonkey", "DartlingGunner"],
        "Magic Monkeys": ["WizardMonkey", "SuperMonkey", "NinjaMonkey", "Alchemist", "Druid", "Mermonkey"],
        "Support Monkeys": ["BananaFarm", "SpikeFactory", "MonkeyVillage", "EngineerMonkey", "BeastHandler"],
    }

    item_offset = 3

    items: Dict[str, int] = {}
    auto_item_groups: Dict[str, set] = {}

    monkeyIDs: List[str] = [
        "DartMonkey",
        "BoomerangMonkey",
        "BombShooter",
        "TackShooter",
        "IceMonkey",
        "GlueGunner",
        "SniperMonkey",
        "MonkeySub",
        "MonkeyBuccaneer",
        "MonkeyAce",
        "HeliPilot",
        "MortarMonkey",
        "DartlingGunner",
        "WizardMonkey",
        "SuperMonkey",
        "NinjaMonkey",
        "Alchemist",
        "Druid",
        "Mermonkey",
        "BananaFarm",
        "SpikeFactory",
        "MonkeyVillage",
        "EngineerMonkey",
        "BeastHandler",
        "Desperado",
    ]

    def __init__(self) -> None:
        mapdata = BloonsLocations()
        maplist = mapdata.get_maps()

        self.items[self.MEDAL_NAME] = self.MEDAL_CODE
        self.items[self.MONEY_NAME] = self.MONEY_CODE
        self.items[self.PROGRESSIVE_KNOWLEDGE_NAME] = self.PROGRESSIVE_KNOWLEDGE_CODE
        self.items[self.PROGRESSIVE_PRICES_NAME] = self.PROGRESSIVE_PRICES_CODE
        self.items[self.CATEGORY_PRIMARY_NAME] = self.CATEGORY_PRIMARY_CODE
        self.items[self.CATEGORY_MILITARY_NAME] = self.CATEGORY_MILITARY_CODE
        self.items[self.CATEGORY_MAGIC_NAME] = self.CATEGORY_MAGIC_CODE
        self.items[self.CATEGORY_SUPPORT_NAME] = self.CATEGORY_SUPPORT_CODE
        self.items[self.MODIFIED_BLOONS_NAME] = self.MODIFIED_BLOONS_CODE
        self.items[self.FREEZE_TRAP_NAME] = self.FREEZE_TRAP_CODE
        self.items[self.BEE_TRAP_NAME] = self.BEE_TRAP_CODE
        self.items[self.SPEED_UP_TRAP_NAME] = self.SPEED_UP_TRAP_CODE
        self.items[self.LITERATURE_TRAP_NAME] = self.LITERATURE_TRAP_CODE
        self.items[self.MONKEY_BOOST_NAME] = self.MONKEY_BOOST_CODE
        self.items[self.MONKEY_STORM_NAME] = self.MONKEY_STORM_CODE
        self.items[self.CASH_DROP_NAME] = self.CASH_DROP_CODE

        index = self.item_offset
        for name in maplist:
            self.items[f"{name}-MUnlock"] = index
            index += 1
        for name in self.monkeyIDs:
            self.items[f"{name}-TUnlock"] = index
            index += 1
        for name in Shared.heroIDs:
            self.items[f"{name}-HUnlock"] = index
            index += 1
        for name in Shared.knowledgeIDs:
            self.items[f"{name}-KUnlock"] = index
            index += 1

        self.auto_item_groups["maps"] = set(
            names for names in self.items.keys() if names.endswith("-MUnlock")
        )
        self.auto_item_groups["towers"] = set(
            names for names in self.items.keys() if names.endswith("-TUnlock")
        )
        self.auto_item_groups["knowledge"] = set(
            name for name in self.items.keys() if name.endswith("-KUnlock")
        ) | {self.PROGRESSIVE_KNOWLEDGE_NAME}

