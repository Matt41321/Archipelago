import math
import random
from BaseClasses import Item, Region
from Utils import visualize_regions
from worlds.AutoWorld import World

from typing import Any, ClassVar, Dict, List, Type
from Options import PerGameCommonOptions
from worlds.generic.Rules import add_rule, set_rule

from .Options import BloonsTD6Options, Difficulty
from .Locations import BTD6Hero, BTD6Knowledge, BTD6Map, BTD6Medal, BloonsLocations
from .Items import (
    BTD6CategoryUnlock,
    BTD6FillerItem,
    BTD6HeroUnlock,
    BTD6KnowledgeUnlock,
    BTD6ProgressiveKnowledge,
    BTD6ProgressivePrices,
    BTD6MapUnlock,
    BTD6MedalItem,
    BTD6MonkeyUnlock,
    BTD6TrapItem,
    BloonsItems,
)
from .Utils import Shared


class BTD6World(World):
    """
    Bloons TD6 is a tower defense game about Monkeys trying to defend themselves against the Balloon onslaught.
    Play a random assortment of maps to collect medals until you can complete the goal map.
    """

    # World Options
    game = "Bloons TD6"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = BloonsTD6Options
    options: BloonsTD6Options

    bloonsMapData = BloonsLocations()
    bloonsItemData = BloonsItems()

    item_name_to_id = {name: code for name, code in bloonsItemData.items.items()}
    location_name_to_id = {name: code for name, code in bloonsMapData.locations.items()}

    item_name_groups = bloonsItemData.auto_item_groups
    location_name_groups = bloonsMapData.auto_location_groups

    def generate_early(self) -> None:
        ## Initialize per-player instances of variables:
        self.starting_maps: List[str] = []
        self.included_maps: List[str] = []

        self.starting_monkeys: List[str] = []
        self.remaining_monkeys: List[str] = []

        starting_hero: str = ""
        self.available_heroes: List[str] = Shared.heroIDs.copy()

        self.random.shuffle(self.available_heroes)

        starting_hero = self.available_heroes.pop(0)
        self.multiworld.push_precollected(self.create_item(starting_hero))

        ## Handle selection of maps for locations
        available_maps: List[str] = self.bloonsMapData.get_maps(
            self.options.min_map_diff.value, self.options.max_map_diff.value
        )
        self.random.shuffle(available_maps)

        # Select Victory Map
        # Boss/Elite Boss events only work on Beginner or Intermediate maps
        if self.options.goal.value >= 1:
            boss_eligible_maps = self.bloonsMapData.get_maps(
                0, min(self.options.max_map_diff.value, 1)
            )
            self.random.shuffle(boss_eligible_maps)
            self.victory_map_name = boss_eligible_maps[0]
            if self.victory_map_name in available_maps:
                available_maps.remove(self.victory_map_name)
        else:
            self.victory_map_name = available_maps.pop()

        # Select and initialize starting maps
        for _ in range(self.options.starting_map_count.value):
            self.starting_maps.append(available_maps.pop())

        for map in self.starting_maps:
            self.multiworld.push_precollected(self.create_item(map))

        # Select unlockable maps for item checks
        for _ in range(self.options.total_maps.value):
            if len(available_maps) == 0:
                break
            self.included_maps.append(available_maps.pop())

        ## Handle start of game initialization for monkey towers
        self.remaining_categories: List[str] = []

        # Towers that can deal damage (used to guarantee at least one attacker when randomizing)
        damage_towers = {
            "DartMonkey", "BoomerangMonkey", "BombShooter", "TackShooter",
            "Desperado", "IceMonkey", "SniperMonkey", "MonkeySub",
            "MonkeyBuccaneer", "WizardMonkey", "NinjaMonkey", "Druid",
            "Mermonkey", "EngineerMonkey", "BeastHandler",
        }

        if self.options.category_lock.value:
            # Category Lock: start with one random category, other 3 are items
            categories = BloonsItems.category_names.copy()
            self.random.shuffle(categories)
            starting_category = categories.pop(0)

            # Precollect all towers in the starting category
            for tower in BloonsItems.category_towers[starting_category]:
                self.multiworld.push_precollected(self.create_item(tower))
                self.starting_monkeys.append(tower)

            # Remaining categories become items
            self.remaining_categories = categories
            # No individual monkey items when category lock is on
        else:
            available_towers: List[str] = self.bloonsItemData.monkeyIDs.copy()

            # Sets starting monkey to Dart Monkey or randomizes it based on options
            if not self.options.starting_monkey.value:
                self.starting_monkeys.append(available_towers.pop(0))
                self.random.shuffle(available_towers)
            else:
                self.random.shuffle(available_towers)
                # Ensure first starting monkey can deal damage
                damage_pool = [t for t in available_towers if t in damage_towers]
                first_monkey = self.random.choice(damage_pool)
                available_towers.remove(first_monkey)
                self.starting_monkeys.append(first_monkey)

            # Adds additional starting monkeys based on options
            for _ in range(self.options.num_start_monkey.value - 1):
                self.starting_monkeys.append(available_towers.pop())

            for monkey in self.starting_monkeys:
                self.multiworld.push_precollected(self.create_item(monkey))

            # Put the rest of the monkeys into storage for item generation
            self.remaining_monkeys.extend(available_towers)

    def create_item(self, name: str) -> Item:
        if name == self.bloonsItemData.MEDAL_NAME:
            return BTD6MedalItem(name, self.bloonsItemData.MEDAL_CODE, self.player)

        if name == self.bloonsItemData.MONEY_NAME:
            return BTD6FillerItem(name, self.bloonsItemData.MONEY_CODE, self.player)

        if name == self.bloonsItemData.MONKEY_BOOST_NAME:
            return BTD6FillerItem(name, self.bloonsItemData.MONKEY_BOOST_CODE, self.player)

        if name == self.bloonsItemData.MONKEY_STORM_NAME:
            return BTD6FillerItem(name, self.bloonsItemData.MONKEY_STORM_CODE, self.player)

        if name == self.bloonsItemData.CASH_DROP_NAME:
            return BTD6FillerItem(name, self.bloonsItemData.CASH_DROP_CODE, self.player)

        if name == self.bloonsItemData.PROGRESSIVE_KNOWLEDGE_NAME:
            return BTD6ProgressiveKnowledge(self.bloonsItemData.PROGRESSIVE_KNOWLEDGE_CODE, self.player)

        if name == self.bloonsItemData.PROGRESSIVE_PRICES_NAME:
            return BTD6ProgressivePrices(self.bloonsItemData.PROGRESSIVE_PRICES_CODE, self.player)

        if name in BloonsItems.category_towers:
            return BTD6CategoryUnlock(name, self.bloonsItemData.items[name], self.player)

        if name == self.bloonsItemData.MODIFIED_BLOONS_NAME:
            return BTD6TrapItem(name, self.bloonsItemData.MODIFIED_BLOONS_CODE, self.player)

        if name == self.bloonsItemData.FREEZE_TRAP_NAME:
            return BTD6TrapItem(name, self.bloonsItemData.FREEZE_TRAP_CODE, self.player)

        if name == self.bloonsItemData.BEE_TRAP_NAME:
            return BTD6TrapItem(name, self.bloonsItemData.BEE_TRAP_CODE, self.player)

        if name == self.bloonsItemData.SPEED_UP_TRAP_NAME:
            return BTD6TrapItem(name, self.bloonsItemData.SPEED_UP_TRAP_CODE, self.player)

        if name == self.bloonsItemData.LITERATURE_TRAP_NAME:
            return BTD6TrapItem(name, self.bloonsItemData.LITERATURE_TRAP_CODE, self.player)

        map = self.bloonsItemData.items.get(f"{name}-MUnlock")
        monkey = self.bloonsItemData.items.get(f"{name}-TUnlock")
        knowledge = self.bloonsItemData.items.get(f"{name}-KUnlock")
        hero = self.bloonsItemData.items.get(f"{name}-HUnlock")
        if map:
            return BTD6MapUnlock(f"{name}-MUnlock", map, self.player)
        if hero:
            return BTD6HeroUnlock(f"{name}-HUnlock", hero, self.player)
        if knowledge:
            return BTD6KnowledgeUnlock(f"{name}-KUnlock", knowledge, self.player)
        return BTD6MonkeyUnlock(f"{name}-TUnlock", monkey, self.player)
        # Remember to add Monkey Money later for future Hero Checks.

    def create_items(self) -> None:
        map_keys = self.included_maps.copy()
        all_map_keys: List[str] = map_keys.copy()
        all_map_keys.extend(self.starting_maps.copy())

        item_count = 0

        for name in map_keys:
            self.multiworld.itempool.append(self.create_item(name))
            item_count += 1

        for _ in range(self.options.total_medals.value):
            self.multiworld.itempool.append(self.create_item(BloonsItems.MEDAL_NAME))
            item_count += 1

        if self.options.category_lock.value:
            for cat in self.remaining_categories:
                self.multiworld.itempool.append(self.create_item(cat))
                item_count += 1
        else:
            for monkey in self.remaining_monkeys:
                self.multiworld.itempool.append(self.create_item(monkey))
                item_count += 1

        for hero in self.available_heroes:
            self.multiworld.itempool.append(self.create_item(hero))
            item_count += 1

        if self.options.progressive_prices.value:
            for _ in range(3):
                self.multiworld.itempool.append(self.create_item(BloonsItems.PROGRESSIVE_PRICES_NAME))
                item_count += 1

        if self.options.progressive_knowledge.value:
            # Progressive mode: 7 items unlock knowledge layer by layer
            for _ in range(7):
                self.multiworld.itempool.append(self.create_item(BloonsItems.PROGRESSIVE_KNOWLEDGE_NAME))
                item_count += 1
        else:
            # Original mode: one item per knowledge node
            for knowledge in Shared.knowledgeIDs:
                self.multiworld.itempool.append(self.create_item(knowledge))
                item_count += 1

        filler_items = (
            len(self.multiworld.get_unfilled_locations(self.player)) - item_count
        )

        # Split filler between traps and Monkey Money based on trap percentage
        trap_count = 0
        if self.options.trap_percentage.value > 0 and filler_items > 0:
            trap_count = max(0, int(filler_items * (self.options.trap_percentage.value / 100)))

        money_count = filler_items - trap_count

        # Distribute traps by weight across trap types
        trap_names = [
            BloonsItems.MODIFIED_BLOONS_NAME,
            BloonsItems.FREEZE_TRAP_NAME,
            BloonsItems.BEE_TRAP_NAME,
            BloonsItems.SPEED_UP_TRAP_NAME,
            BloonsItems.LITERATURE_TRAP_NAME,
        ]
        trap_weights = [
            max(0, self.options.modified_bloons_weight.value),
            max(0, self.options.freeze_weight.value),
            max(0, self.options.bee_weight.value),
            max(0, self.options.speed_up_weight.value),
            max(0, self.options.literature_weight.value),
        ]
        if sum(trap_weights) == 0:
            trap_weights = [1, 1, 1, 1, 1]  # equal distribution if all weights are zero
        for _ in range(trap_count):
            chosen = random.choices(trap_names, weights=trap_weights, k=1)[0]
            self.multiworld.itempool.append(self.create_item(chosen))
        # Split non-trap filler evenly between Monkey Boost, Monkey Storm, and Cash Boost
        filler_cycle = [
            BloonsItems.MONKEY_BOOST_NAME,
            BloonsItems.MONKEY_STORM_NAME,
            BloonsItems.CASH_DROP_NAME,
        ]
        for i in range(money_count):
            self.multiworld.itempool.append(self.create_item(filler_cycle[i % 3]))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        map_select_region = Region("Map Select", self.player, self.multiworld)
        xp_region = Region("XP Progression", self.player, self.multiworld)
        hero_select_region = Region("Hero Select", self.player, self.multiworld)
        self.multiworld.regions += [
            menu_region,
            map_select_region,
            xp_region,
            hero_select_region,
        ]
        menu_region.connect(map_select_region)
        menu_region.connect(xp_region)
        menu_region.connect(hero_select_region)

        all_maps_copy = self.starting_maps.copy()
        incl_maps_copy = self.included_maps.copy()

        self.random.shuffle(incl_maps_copy)
        all_maps_copy.extend(incl_maps_copy)

        # region Map Locations
        for i in range(len(all_maps_copy)):
            name: str
            name = all_maps_copy[i]

            region = Region(name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            map_select_region.connect(
                region,
                name,
                lambda state, place=name + "-MUnlock": state.has(place, self.player),
            )
            region.add_locations(
                {
                    name + "-Unlock": self.bloonsMapData.locations[name + "-Unlock"],
                },
                BTD6Map,
            )

            # Handle Mode Based Checks
            region.add_locations(
                {
                    name + "-Easy": self.bloonsMapData.locations[name + "-Easy"],
                    name + "-Medium": self.bloonsMapData.locations[name + "-Medium"],
                    name + "-Hard": self.bloonsMapData.locations[name + "-Hard"],
                    name
                    + "-Impoppable": self.bloonsMapData.locations[name + "-Impoppable"],
                },
                BTD6Medal,
            )
            if self.options.rando_difficulty.value >= Difficulty.option_Advanced:
                region.add_locations(
                    {name + "-Chimps": self.bloonsMapData.locations[name + "-Chimps"]},
                    BTD6Medal,
                )
            if self.options.rando_difficulty.value == Difficulty.option_Expert:
                region.add_locations(
                    {
                        name
                        + "-PrimaryOnly": self.bloonsMapData.locations[
                            name + "-PrimaryOnly"
                        ],
                        name
                        + "-Deflation": self.bloonsMapData.locations[
                            name + "-Deflation"
                        ],
                        name
                        + "-MilitaryOnly": self.bloonsMapData.locations[
                            name + "-MilitaryOnly"
                        ],
                        name
                        + "-Apopalypse": self.bloonsMapData.locations[
                            name + "-Apopalypse"
                        ],
                        name
                        + "-Reverse": self.bloonsMapData.locations[name + "-Reverse"],
                        name
                        + "-MagicOnly": self.bloonsMapData.locations[
                            name + "-MagicOnly"
                        ],
                        name
                        + "-DoubleMoabHealth": self.bloonsMapData.locations[
                            name + "-DoubleMoabHealth"
                        ],
                        name
                        + "-HalfCash": self.bloonsMapData.locations[name + "-HalfCash"],
                        name
                        + "-AlternateBloonsRounds": self.bloonsMapData.locations[
                            name + "-AlternateBloonsRounds"
                        ],
                    },
                    BTD6Medal,
                )
                if self.options.category_lock.value:
                    add_rule(
                        self.multiworld.get_location(f"{name}-PrimaryOnly", self.player),
                        rule=lambda state: state.has("Primary Monkeys", self.player),
                    )
                    add_rule(
                        self.multiworld.get_location(f"{name}-MilitaryOnly", self.player),
                        rule=lambda state: state.has("Military Monkeys", self.player),
                    )
                    add_rule(
                        self.multiworld.get_location(f"{name}-MagicOnly", self.player),
                        rule=lambda state: state.has("Magic Monkeys", self.player),
                    )
                else:
                    add_rule(
                        self.multiworld.get_location(f"{name}-PrimaryOnly", self.player),
                        rule=lambda state: state.has_from_list(
                            {
                                "DartMonkey-TUnlock",
                                "BoomerangMonkey-TUnlock",
                                "BombShooter-TUnlock",
                                "TackShooter-TUnlock",
                                "IceMonkey-TUnlock",
                                "GlueGunner-TUnlock",
                                "Desperado-TUnlock"
                            },
                            self.player,
                            2,
                        ),
                    )
                    add_rule(
                        self.multiworld.get_location(f"{name}-MilitaryOnly", self.player),
                        rule=lambda state: state.has_from_list(
                            {
                                "SniperMonkey-TUnlock",
                                "MonkeySub-TUnlock",
                                "MonkeyBuccaneer-TUnlock",
                                "MonkeyAce-TUnlock",
                                "HeliPilot-TUnlock",
                                "MortarMonkey-TUnlock",
                                "DartlingGunner-TUnlock",
                            },
                            self.player,
                            2,
                        ),
                    )
                    add_rule(
                        self.multiworld.get_location(f"{name}-MagicOnly", self.player),
                        rule=lambda state: state.has_from_list(
                            {
                                "WizardMonkey-TUnlock",
                                "SuperMonkey-TUnlock",
                                "NinjaMonkey-TUnlock",
                                "Alchemist-TUnlock",
                                "Druid-TUnlock",
                                "Mermonkey-TUnlock",
                            },
                            self.player,
                            2,
                        ),
                    )

            # Handle Round Sanity Checks for this map
            if self.options.round_sanity.value > 0:
                interval = self.options.round_sanity.value
                r = interval
                while r <= 100:
                    loc_name = f"{name}-Round {r}"
                    region.add_locations(
                        {loc_name: self.bloonsMapData.locations[loc_name]}
                    )
                    r += interval
        # endregion

        # region Hero Locations
        for hero in Shared.heroIDs:
            region = Region(hero, self.player, self.multiworld)
            region.add_locations({hero: self.bloonsMapData.locations[hero]}, BTD6Hero)
            hero_select_region.connect(
                region, rule=lambda state: state.has(hero + "-HUnlock", self.player)
            )
            self.multiworld.regions.append(region)
        # endregion

        # region Level Locations
        # Levels are split into 7 XP-sphere sub-regions so the AP solver spreads items
        # across the full level range rather than dumping everything into sphere 1.
        #
        # Cumulative XP thresholds (raw XP):
        #   Sphere 1 : <  1 000 000
        #   Sphere 2 :  1 000 000 –  5 000 000
        #   Sphere 3 :  5 000 000 – 15 000 000
        #   Sphere 4 : 15 000 000 – 30 000 000
        #   Sphere 5 :  30 000 000 – 60 000 000
        #   Sphere 6 :  60 000 000 – 120 000 000
        #   Sphere 7 : 120 000 000 – 180 000 000

        XP_THRESHOLDS = [0, 1_000_000, 5_000_000, 15_000_000, 30_000_000, 60_000_000, 120_000_000]
  
        SPHERE_MEDAL_PCTS = [0, 35, 50, 63, 75, 85, 93]

        total_medals = self.options.total_medals.value

        xp_sphere_regions = []
        for s in range(7):
            sr = Region(f"XP Sphere {s + 1}", self.player, self.multiworld)
            self.multiworld.regions.append(sr)
            xp_sphere_regions.append(sr)
            n = max(0, int(total_medals * SPHERE_MEDAL_PCTS[s] / 100))
            if n == 0:
                xp_region.connect(sr)
            else:
                xp_region.connect(
                    sr,
                    rule=lambda state, medals=n: state.has(BloonsItems.MEDAL_NAME, self.player, medals),
                )

        for i in range(self.options.max_level.value - 1):
            level = i + 2
            name  = f"Level {level}"

            if self.options.xp_curve.value:
                cum_xp = 0.3556 * (level ** 4)
            else:
                cum_xp = (level - 1) * self.options.static_req.value

            sphere = 1
            for threshold in XP_THRESHOLDS[1:]:
                if cum_xp >= threshold:
                    sphere += 1
                else:
                    break

            xp_sphere_regions[sphere - 1].add_locations({name: self.bloonsMapData.locations[name]})
        # endregion

        # region Pop Tier Locations
        if self.options.pop_tier_checks.value:
            pop_tier_region = Region("Pop Tiers", self.player, self.multiworld)
            self.multiworld.regions.append(pop_tier_region)
            menu_region.connect(pop_tier_region)
            for monkey in self.bloonsItemData.monkeyIDs:
                if f"{monkey}-Tier3" not in self.bloonsMapData.locations:
                    continue
                pop_tier_region.add_locations({
                    f"{monkey}-Tier3": self.bloonsMapData.locations[f"{monkey}-Tier3"],
                    f"{monkey}-Tier4": self.bloonsMapData.locations[f"{monkey}-Tier4"],
                    f"{monkey}-Tier5": self.bloonsMapData.locations[f"{monkey}-Tier5"],
                })
                # Require the monkey to be unlocked before its tier locations are
                # accessible — this prevents the solver from placing that monkey's
                # own TUnlock item behind its own pop tier check (circular dependency).
                for tier in ("Tier3", "Tier4", "Tier5"):
                    add_rule(
                        self.multiworld.get_location(f"{monkey}-{tier}", self.player),
                        rule=lambda state, m=monkey: state.has(f"{m}-TUnlock", self.player),
                    )
        # endregion

        # region Knowledge Locations
        if not self.options.progressive_knowledge.value:
            # Original mode: individual knowledge nodes as locations gated by their own items
            knowledge_region = Region("Knowledge Tree", self.player, self.multiworld)
            self.multiworld.regions.append(knowledge_region)
            menu_region.connect(knowledge_region)

            primary_region = Region("Primary Knowledge", self.player, self.multiworld)
            military_region = Region("Military Knowledge", self.player, self.multiworld)
            magic_region = Region("Magic Knowledge", self.player, self.multiworld)
            support_region = Region("Support Knowledge", self.player, self.multiworld)
            heroes_region = Region("Hero Knowledge", self.player, self.multiworld)
            powers_region = Region("Powers Region", self.player, self.multiworld)

            self.multiworld.regions += [
                primary_region, military_region, magic_region,
                support_region, heroes_region, powers_region,
            ]

            knowledge_region.connect(primary_region)
            knowledge_region.connect(military_region)
            knowledge_region.connect(magic_region)
            knowledge_region.connect(support_region)
            knowledge_region.connect(heroes_region)
            knowledge_region.connect(powers_region)

            knowledge_regions: List[Region] = []
            for kname in Shared.knowledgeIDs:
                region = Region(kname, self.player, self.multiworld)
                region.add_locations(
                    {kname + "-Tree": self.bloonsMapData.locations[f"{kname}-Tree"]},
                    BTD6Knowledge,
                )
                knowledge_regions.append(region)

            self.multiworld.regions += knowledge_regions

            def knowledge_connection(parent_region: Region | int, knowledge_id: int):
                if type(parent_region) is int:
                    region = knowledge_regions[parent_region]
                else:
                    region = parent_region
                region.connect(
                    knowledge_regions[knowledge_id],
                    rule=lambda state, place=Shared.knowledgeIDs[knowledge_id] + "-KUnlock": state.has(place, self.player),
                )

            # Primary Layer 1
            knowledge_connection(primary_region, 0)
            knowledge_connection(primary_region, 1)
            knowledge_connection(primary_region, 2)
            # Primary Layer 2
            knowledge_connection(0, 4)
            knowledge_connection(4, 3)
            knowledge_connection(0, 5)
            knowledge_connection(1, 6)
            knowledge_connection(1, 7)
            knowledge_connection(2, 8)
            # Primary Layer 3
            knowledge_connection(3, 9)
            knowledge_connection(4, 10)
            knowledge_connection(5, 11)
            knowledge_connection(6, 12)
            knowledge_connection(7, 13)
            knowledge_connection(13, 16)
            knowledge_connection(8, 14)
            knowledge_connection(8, 15)
            # Primary Layer 4
            knowledge_connection(10, 17)
            knowledge_connection(11, 18)
            knowledge_connection(13, 19)
            knowledge_connection(14, 20)
            knowledge_connection(18, 21)
            knowledge_connection(19, 21)
            # Primary Layer 5
            knowledge_connection(17, 22)
            knowledge_connection(17, 23)
            knowledge_connection(18, 24)
            knowledge_connection(12, 25)
            knowledge_connection(19, 26)
            knowledge_connection(26, 28)
            knowledge_connection(20, 27)
            # Primary Layer 6
            knowledge_connection(24, 29)
            knowledge_connection(27, 30)
            knowledge_connection(29, 31)
            knowledge_connection(30, 31)
            # Military Layer 1
            knowledge_connection(military_region, 32)
            knowledge_connection(military_region, 33)
            knowledge_connection(military_region, 34)
            knowledge_connection(military_region, 35)
            # Military Layer 2
            knowledge_connection(32, 36)
            knowledge_connection(33, 37)
            knowledge_connection(34, 38)
            # Military Layer 3
            knowledge_connection(military_region, 39)
            knowledge_connection(32, 40)
            knowledge_connection(36, 41)
            knowledge_connection(37, 42)
            knowledge_connection(33, 43)
            knowledge_connection(38, 44)
            knowledge_connection(35, 45)
            # Military Layer 4
            knowledge_connection(40, 46)
            knowledge_connection(41, 47)
            knowledge_connection(42, 48)
            knowledge_connection(39, 49)
            knowledge_connection(45, 50)
            # Military Layer 5
            knowledge_connection(46, 56)
            knowledge_connection(47, 56)
            knowledge_connection(48, 52)
            knowledge_connection(52, 55)
            knowledge_connection(43, 51)
            knowledge_connection(49, 54)
            knowledge_connection(44, 53)
            # Military Layer 6
            knowledge_connection(56, 57)
            knowledge_connection(47, 58)
            knowledge_connection(51, 59)
            knowledge_connection(59, 60)
            knowledge_connection(52, 60)
            # Military Layer 7
            knowledge_connection(57, 61)
            knowledge_connection(53, 61)
            # Magic Layer 1
            knowledge_connection(magic_region, 62)
            knowledge_connection(magic_region, 64)
            knowledge_connection(magic_region, 63)
            # Magic Layer 2
            knowledge_connection(62, 65)
            knowledge_connection(62, 66)
            knowledge_connection(64, 67)
            knowledge_connection(63, 68)
            knowledge_connection(68, 69)
            # Magic Layer 3
            knowledge_connection(65, 70)
            knowledge_connection(66, 71)
            knowledge_connection(67, 72)
            knowledge_connection(68, 73)
            knowledge_connection(67, 78)
            knowledge_connection(63, 78)
            # Magic Layer 4
            knowledge_connection(71, 74)
            knowledge_connection(72, 77)
            knowledge_connection(73, 76)
            knowledge_connection(78, 75)
            # Magic Layer 5
            knowledge_connection(77, 81)
            knowledge_connection(74, 80)
            knowledge_connection(70, 79)
            # Magic Layer 6
            knowledge_connection(79, 83)
            knowledge_connection(81, 83)
            knowledge_connection(75, 82)
            # Support Layer 1
            knowledge_connection(support_region, 84)
            knowledge_connection(support_region, 85)
            # Support Layer 2
            knowledge_connection(84, 86)
            knowledge_connection(84, 87)
            knowledge_connection(85, 88)
            # Support Layer 3
            knowledge_connection(86, 90)
            knowledge_connection(87, 91)
            knowledge_connection(85, 92)
            knowledge_connection(support_region, 89)
            # Support Layer 4
            knowledge_connection(90, 94)
            knowledge_connection(91, 95)
            knowledge_connection(92, 97)
            knowledge_connection(88, 93)
            knowledge_connection(89, 96)
            # Support Layer 5
            knowledge_connection(94, 98)
            knowledge_connection(95, 103)
            knowledge_connection(97, 102)
            knowledge_connection(93, 99)
            knowledge_connection(96, 100)
            knowledge_connection(96, 101)
            # Support Layer 6
            knowledge_connection(98, 104)
            knowledge_connection(100, 105)
            # Heroes Layer 1
            knowledge_connection(heroes_region, 106)
            knowledge_connection(heroes_region, 107)
            knowledge_connection(heroes_region, 108)
            # Heroes Layer 2
            knowledge_connection(106, 109)
            knowledge_connection(107, 110)
            # Heroes Layer 3
            knowledge_connection(109, 111)
            knowledge_connection(110, 112)
            knowledge_connection(108, 113)
            # Heroes Layer 4
            knowledge_connection(111, 114)
            knowledge_connection(112, 114)
            # Heroes Layer 5
            knowledge_connection(114, 115)
            knowledge_connection(113, 116)
            # Heroes Layer 6
            knowledge_connection(115, 117)
            knowledge_connection(116, 118)
            # Powers Layer 1
            knowledge_connection(powers_region, 119)
            knowledge_connection(powers_region, 120)
            knowledge_connection(powers_region, 121)
            # Powers Layer 2
            knowledge_connection(119, 122)
            knowledge_connection(120, 123)
            knowledge_connection(121, 124)
            # Powers Layer 3
            knowledge_connection(122, 125)
            knowledge_connection(123, 126)
            knowledge_connection(124, 132)
            knowledge_connection(126, 132)
            # Powers Layer 4
            knowledge_connection(125, 129)
            knowledge_connection(126, 127)
            knowledge_connection(132, 128)
            # Powers Layer 5
            knowledge_connection(128, 130)
            knowledge_connection(128, 131)
            # Powers Layer 6
            knowledge_connection(130, 133)
        else:
            # Progressive mode: knowledge is applied automatically in-game when
            # "Progressive Knowledge" items are received. No Tree locations exist —
            # there's nothing to click or check.
            pass
        # endregion

        # visualize_regions(
        #     self.multiworld.get_region("Menu", self.player),
        #     "output/regionmap.puml",
        # )

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            BloonsItems.MEDAL_NAME,
            self.player,
            int(round(self.options.total_medals.value * (self.options.medalreq.value / 100))),
        )

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "victoryLocation": self.victory_map_name,
            "medalsNeeded": int(round(self.options.total_medals.value * (self.options.medalreq.value / 100))),
            "xpCurve": bool(self.options.xp_curve.value),
            "staticXPReq": int(self.options.static_req.value),
            "maxLevel": int(self.options.max_level.value),
            "difficulty": int(self.options.rando_difficulty.value),
            "popTierChecks": bool(self.options.pop_tier_checks.value),
            "tier3PopRequirement": int(self.options.tier3_pop_requirement.value),
            "tier4PopRequirement": int(self.options.tier4_pop_requirement.value),
            "tier5PopRequirement": int(self.options.tier5_pop_requirement.value),
            "progressiveKnowledge": bool(self.options.progressive_knowledge.value),
            "roundSanity": int(self.options.round_sanity.value),
            "progressivePrices": bool(self.options.progressive_prices.value),
            "categoryLock": bool(self.options.category_lock.value),
            "goal": int(self.options.goal.value),
        }
