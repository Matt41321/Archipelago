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
        super().__init__("Progressive Prices", ItemClassification.progression, code, player)


class BTD6ProgressiveStartingCash(Item):
    game: str = "Bloons TD6"

    def __init__(self, code: Optional[int], player: int):
        super().__init__("Progressive Starting Cash", ItemClassification.useful, code, player)


class BTD6CategoryUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6TrapItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.trap, code, player)


class BTD6PathUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


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

    PROGRESSIVE_STARTING_CASH_NAME: str = "Progressive Starting Cash"
    PROGRESSIVE_STARTING_CASH_CODE: int = 1028

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

    RESOLUTION_TRAP_NAME: str = "144p Trap"
    RESOLUTION_TRAP_CODE: int = 1013

    FLOOD_TRAP_NAME: str = "Flood Trap"
    FLOOD_TRAP_CODE: int = 1014

    SWAP_TRAP_NAME: str = "Swap Trap"
    SWAP_TRAP_CODE: int = 1015

    SHUFFLE_TRAP_NAME: str = "Shuffle Trap"
    SHUFFLE_TRAP_CODE: int = 1016

    ZOOM_TRAP_NAME: str = "Zoom Trap"
    ZOOM_TRAP_CODE: int = 1017

    SCREEN_FLIP_TRAP_NAME: str = "Screen Flip Trap"
    SCREEN_FLIP_TRAP_CODE: int = 1018

    CHAOS_TRAP_NAME: str = "Chaos Control Trap"
    CHAOS_TRAP_CODE: int = 1020

    MATH_QUIZ_TRAP_NAME: str = "Math Quiz Trap"
    MATH_QUIZ_TRAP_CODE: int = 1021

    TRIVIA_TRAP_NAME: str = "Trivia Trap"
    TRIVIA_TRAP_CODE: int = 1022

    POKEMON_TRIVIA_TRAP_NAME: str = "Pokemon Trivia Trap"
    POKEMON_TRIVIA_TRAP_CODE: int = 1023

    NUMBER_SEQUENCE_TRAP_NAME: str = "Number Sequence Trap"
    NUMBER_SEQUENCE_TRAP_CODE: int = 1024

    INPUT_SEQUENCE_TRAP_NAME: str = "Input Sequence Trap"
    INPUT_SEQUENCE_TRAP_CODE: int = 1025

    YAP_TRAP_NAME: str = "Yap Trap"
    YAP_TRAP_CODE: int = 1026

    # Dict of trap name -> item code, used for weighted selection
    trap_items: Dict[str, int] = {
        "Modified Bloons": 1005,
        "Freeze Trap": 1006,
        "Bee Trap": 1007,
        "Speed Up Trap": 1008,
        "Literature Trap": 1009,
        "144p Trap": 1013,
        "Flood Trap": 1014,
        "Swap Trap": 1015,
        "Shuffle Trap": 1016,
        "Zoom Trap": 1017,
        "Screen Flip Trap": 1018,
        "Chaos Control Trap": 1020,
        "Math Quiz Trap": 1021,
        "Trivia Trap": 1022,
        "Pokemon Trivia Trap": 1023,
        "Number Sequence Trap": 1024,
        "Input Sequence Trap": 1025,
        "Yap Trap": 1026,
    }

    MONKEY_BOOST_NAME: str = "Monkey Boost"
    MONKEY_BOOST_CODE: int = 1010

    MONKEY_STORM_NAME: str = "Monkey Storm"
    MONKEY_STORM_CODE: int = 1011

    CASH_DROP_NAME: str = "Cash Drop"
    CASH_DROP_CODE: int = 1012

    THRIVE_NAME: str = "Thrive"
    THRIVE_CODE: int = 1027

    category_names: List[str] = [
        "Primary Monkeys",
        "Military Monkeys",
        "Magic Monkeys",
        "Support Monkeys",
    ]

    category_towers: Dict[str, List[str]] = {
        "Primary Monkeys": ["DartMonkey", "BoomerangMonkey", "BombShooter", "TackShooter", "IceMonkey", "GlueGunner", "Desperado"],
        "Military Monkeys": ["SniperMonkey", "MonkeySub", "MonkeyBuccaneer", "MonkeyAce", "HeliPilot", "MortarMonkey", "DartlingGunner"],
        "Magic Monkeys": ["WizardMonkey", "SuperMonkey", "NinjaMonkey", "Alchemist", "Druid", "Mermonkey", "Skywarden"],
        "Support Monkeys": ["BananaFarm", "SpikeFactory", "MonkeyVillage", "EngineerMonkey", "BeastHandler"],
    }

    # Reverse lookup used by the logic rules in category lock mode, where a monkey is
    # represented by its category item instead of its own "-TUnlock" item.
    monkey_to_category: Dict[str, str] = {
        monkey: category
        for category, monkeys in category_towers.items()
        for monkey in monkeys
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
        "Skywarden",
    ]

    display_name_to_id: Dict[str, str] = {
        "Dart Monkey": "DartMonkey",
        "Boomerang Monkey": "BoomerangMonkey",
        "Bomb Shooter": "BombShooter",
        "Tack Shooter": "TackShooter",
        "Ice Monkey": "IceMonkey",
        "Glue Gunner": "GlueGunner",
        "Sniper Monkey": "SniperMonkey",
        "Monkey Sub": "MonkeySub",
        "Monkey Buccaneer": "MonkeyBuccaneer",
        "Monkey Ace": "MonkeyAce",
        "Heli Pilot": "HeliPilot",
        "Mortar Monkey": "MortarMonkey",
        "Dartling Gunner": "DartlingGunner",
        "Wizard Monkey": "WizardMonkey",
        "Super Monkey": "SuperMonkey",
        "Ninja Monkey": "NinjaMonkey",
        "Alchemist": "Alchemist",
        "Druid": "Druid",
        "Mermonkey": "Mermonkey",
        "Banana Farm": "BananaFarm",
        "Spike Factory": "SpikeFactory",
        "Monkey Village": "MonkeyVillage",
        "Engineer Monkey": "EngineerMonkey",
        "Beast Handler": "BeastHandler",
        "Desperado": "Desperado",
        "Skywarden": "Skywarden",
    }

    id_to_display_name: Dict[str, str] = {v: k for k, v in display_name_to_id.items()}

    _normalized_lookup: Dict[str, str] = {
        k.lower().replace(" ", ""): v
        for k, v in display_name_to_id.items()
    }

    @classmethod
    def resolve_monkey_name(cls, name: str) -> str | None:
        if name in cls.display_name_to_id:
            return cls.display_name_to_id[name]
        normalized = name.lower().replace(" ", "")
        return cls._normalized_lookup.get(normalized)

    def __init__(self) -> None:
        mapdata = BloonsLocations()
        maplist = mapdata.get_maps()

        self.items[self.MEDAL_NAME] = self.MEDAL_CODE
        self.items[self.MONEY_NAME] = self.MONEY_CODE
        self.items[self.PROGRESSIVE_KNOWLEDGE_NAME] = self.PROGRESSIVE_KNOWLEDGE_CODE
        self.items[self.PROGRESSIVE_PRICES_NAME] = self.PROGRESSIVE_PRICES_CODE
        self.items[self.PROGRESSIVE_STARTING_CASH_NAME] = self.PROGRESSIVE_STARTING_CASH_CODE
        self.items[self.CATEGORY_PRIMARY_NAME] = self.CATEGORY_PRIMARY_CODE
        self.items[self.CATEGORY_MILITARY_NAME] = self.CATEGORY_MILITARY_CODE
        self.items[self.CATEGORY_MAGIC_NAME] = self.CATEGORY_MAGIC_CODE
        self.items[self.CATEGORY_SUPPORT_NAME] = self.CATEGORY_SUPPORT_CODE
        for trap_name, trap_code in self.trap_items.items():
            self.items[trap_name] = trap_code
        self.items[self.MONKEY_BOOST_NAME] = self.MONKEY_BOOST_CODE
        self.items[self.MONKEY_STORM_NAME] = self.MONKEY_STORM_CODE
        self.items[self.CASH_DROP_NAME] = self.CASH_DROP_CODE
        self.items[self.THRIVE_NAME] = self.THRIVE_CODE

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
        for monkey in self.monkeyIDs:
            for path in Shared.pathNames:
                self.items[f"{monkey}-{path}"] = index
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
        self.auto_item_groups["paths"] = set(
            name for name in self.items.keys()
            if name.endswith("-TopPath") or name.endswith("-MiddlePath") or name.endswith("-BottomPath")
        )

