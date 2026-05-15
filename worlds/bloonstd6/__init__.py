import math
import random
from BaseClasses import Item, Region
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World

from typing import Any, ClassVar, Dict, List, Type
from Options import PerGameCommonOptions
from worlds.generic.Rules import add_rule, set_rule

from .Options import BloonsTD6Options, btd6_option_groups
from .Rules import set_map_rules, set_round_rule, has_economy, STARTING_DAMAGE_TOWERS
from .Locations import BTD6Hero, BTD6Knowledge, BTD6Map, BTD6Medal, BloonsLocations
from .Items import (
    BTD6CategoryUnlock,
    BTD6FillerItem,
    BTD6HeroUnlock,
    BTD6KnowledgeUnlock,
    BTD6PathUnlock,
    BTD6ProgressiveKnowledge,
    BTD6ProgressivePrices,
    BTD6MapUnlock,
    BTD6MedalItem,
    BTD6MonkeyUnlock,
    BTD6TrapItem,
    BloonsItems,
)
from .Utils import Shared


class BTD6Web(WebWorld):
    option_groups = btd6_option_groups


class BTD6World(World):
    """
    Bloons TD6 is a tower defense game about Monkeys trying to defend themselves against the Balloon onslaught.
    Play a random assortment of maps to collect medals until you can complete the goal map.
    """

    # World Options
    game = "Bloons TD6"
    web = BTD6Web()
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = BloonsTD6Options
    options: BloonsTD6Options

    bloonsMapData = BloonsLocations()
    bloonsItemData = BloonsItems()

    item_name_to_id = {name: code for name, code in bloonsItemData.items.items()}
    location_name_to_id = {name: code for name, code in bloonsMapData.locations.items()}

    item_name_groups = bloonsItemData.auto_item_groups
    location_name_groups = bloonsMapData.auto_location_groups

    def _apply_map_filters(self, maps: List[str]) -> List[str]:
        """Apply whitelist and blacklist options to a map list.
        Blacklisted maps are removed. Whitelisted maps are moved to the end so they
        are popped first and guaranteed into the pool before random maps fill remaining slots."""
        blacklist_ids = {
            resolved for name in self.options.map_blacklist.value
            if (resolved := BloonsLocations.resolve_map_name(name)) is not None
        }
        whitelist_ids = {
            resolved for name in self.options.map_whitelist.value
            if (resolved := BloonsLocations.resolve_map_name(name)) is not None
        }
        if blacklist_ids:
            maps = [m for m in maps if m not in blacklist_ids]
        if whitelist_ids:
            guaranteed = [m for m in maps if m in whitelist_ids]
            rest = [m for m in maps if m not in whitelist_ids]
            maps = rest + guaranteed
        return maps

    def generate_early(self) -> None:
        ## Initialize per-player instances of variables:
        self.starting_maps: List[str] = []
        self.included_maps: List[str] = []

        self.starting_monkeys: List[str] = []
        self.remaining_monkeys: List[str] = []
        self.remaining_categories: List[str] = []

        self.starting_hero: str = ""
        self.available_heroes: List[str] = []

        passthrough = getattr(self.multiworld, "re_gen_passthrough", {}).get("Bloons TD6", {})
        if passthrough:
            self._load_from_passthrough(passthrough)
            return

        self.available_heroes = Shared.heroIDs.copy()
        self.random.shuffle(self.available_heroes)

        self.starting_hero = self.available_heroes.pop(0)
        self.multiworld.push_precollected(self.create_item(self.starting_hero))

        # Handle selection of maps for locations
        available_maps: List[str] = self.bloonsMapData.get_maps(
            self.options.min_map_diff.value, self.options.max_map_diff.value
        )
        self.random.shuffle(available_maps)
        available_maps = self._apply_map_filters(available_maps)

        # Select Victory Map
        # Boss/Elite Boss events only work on Beginner or Intermediate maps
        if self.options.goal.value >= 1:
            boss_eligible_maps = self.bloonsMapData.get_maps(
                0, min(self.options.max_map_diff.value, 1)
            )
            self.random.shuffle(boss_eligible_maps)
            boss_eligible_maps = self._apply_map_filters(boss_eligible_maps)
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

        # Towers that can deal damage and are affordable enough to start with.
        damage_towers = STARTING_DAMAGE_TOWERS

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

        # Hardness order for determining the goal mode (hardest first)
        _HARDNESS_ORDER = [
            "Chimps", "Impoppable", "HalfCash", "AlternateBloonsRounds", "DoubleMoabHealth", "MagicOnly", "Hard",
            "Apopalypse", "MilitaryOnly", "Reverse", "Medium",
            "Deflation", "PrimaryOnly", "Easy",
        ]
        # Sort pool for deterministic random.sample regardless of set iteration order
        pool = sorted(self.options.mode_pool.value) or ["Easy", "Medium", "Hard", "Impoppable"]
        max_n = min(int(self.options.modes_per_map.value), len(pool))
        randomise_count = bool(self.options.random_mode_amount_per_map.value)
        self.map_modes: Dict[str, List[str]] = {}
        for map_name in self.starting_maps + self.included_maps:
            n = self.random.randint(1, max_n) if randomise_count else max_n
            self.map_modes[map_name] = self.random.sample(pool, n)
        self.goal_mode = next((m for m in _HARDNESS_ORDER if m in pool), "Easy")

    def _load_from_passthrough(self, passthrough: Dict[str, Any]) -> None:
        """Restore generate_early state from slot data (used by Universal Tracker)."""
        self.victory_map_name = passthrough["victoryLocation"]
        self.starting_maps = list(passthrough["startingMaps"])
        self.included_maps = list(passthrough["includedMaps"])
        self.starting_monkeys = list(passthrough["startingMonkeys"])
        self.starting_hero = passthrough["startingHero"]
        self.available_heroes = list(passthrough["availableHeroes"])
        self.remaining_categories = list(passthrough.get("remainingCategories", []))
        self.map_modes = {k: list(v) for k, v in passthrough.get("mapModes", {}).items()}
        self.goal_mode = passthrough.get("goalMode", "Impoppable")
        # Remaining monkeys = all towers not chosen as starters
        self.remaining_monkeys = [
            t for t in self.bloonsItemData.monkeyIDs
            if t not in self.starting_monkeys
        ]
        for map_name in self.starting_maps:
            self.multiworld.push_precollected(self.create_item(map_name))
        for monkey in self.starting_monkeys:
            self.multiworld.push_precollected(self.create_item(monkey))
        self.multiworld.push_precollected(self.create_item(self.starting_hero))

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return slot data for the Universal Tracker's re_gen_passthrough mechanism.

        The tracker calls this when connecting to a live game so it can regenerate
        the world with the exact same map/tower/hero choices as the server used,
        instead of re-randomising with a different seed.
        """
        return slot_data

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

        if name in BloonsItems.trap_items:
            return BTD6TrapItem(name, BloonsItems.trap_items[name], self.player)

        if name.endswith("-MUnlock") and name in self.bloonsItemData.items:
            return BTD6MapUnlock(name, self.bloonsItemData.items[name], self.player)
        if name.endswith("-TUnlock") and name in self.bloonsItemData.items:
            return BTD6MonkeyUnlock(name, self.bloonsItemData.items[name], self.player)
        if name.endswith("-HUnlock") and name in self.bloonsItemData.items:
            return BTD6HeroUnlock(name, self.bloonsItemData.items[name], self.player)
        if name.endswith("-KUnlock") and name in self.bloonsItemData.items:
            return BTD6KnowledgeUnlock(name, self.bloonsItemData.items[name], self.player)
        if (name.endswith("-TopPath") or name.endswith("-MiddlePath") or name.endswith("-BottomPath")) and name in self.bloonsItemData.items:
            return BTD6PathUnlock(name, self.bloonsItemData.items[name], self.player)

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

        if self.options.upgrade_sanity.value:
            for monkey in self.bloonsItemData.monkeyIDs:
                for path in Shared.pathNames:
                    self.multiworld.itempool.append(self.create_item(f"{monkey}-{path}"))
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
        weight_map = {
            name: max(0, self.options.trap_weights.value.get(name, 0))
            for name in BloonsItems.trap_items
        }
        trap_names = [n for n, w in weight_map.items() if w > 0]
        trap_weights = [weight_map[n] for n in trap_names]
        if not trap_names:
            trap_count = 0  # all weights zero — skip traps entirely
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

            # Handle Mode Based Checks — only add modes assigned to this map
            for mode in self.map_modes[name]:
                region.add_locations(
                    {f"{name}-{mode}": self.bloonsMapData.locations[f"{name}-{mode}"]},
                    BTD6Medal,
                )

            if "PrimaryOnly" in self.map_modes[name]:
                if self.options.category_lock.value:
                    add_rule(
                        self.multiworld.get_location(f"{name}-PrimaryOnly", self.player),
                        rule=lambda state: state.has("Primary Monkeys", self.player),
                    )
                else:
                    add_rule(
                        self.multiworld.get_location(f"{name}-PrimaryOnly", self.player),
                        rule=lambda state: state.has_from_list(
                            {
                                "DartMonkey-TUnlock", "BoomerangMonkey-TUnlock",
                                "BombShooter-TUnlock", "TackShooter-TUnlock",
                                "IceMonkey-TUnlock", "GlueGunner-TUnlock",
                                "Desperado-TUnlock",
                            },
                            self.player, 2,
                        ),
                    )
            if "MilitaryOnly" in self.map_modes[name]:
                if self.options.category_lock.value:
                    add_rule(
                        self.multiworld.get_location(f"{name}-MilitaryOnly", self.player),
                        rule=lambda state: state.has("Military Monkeys", self.player),
                    )
                else:
                    add_rule(
                        self.multiworld.get_location(f"{name}-MilitaryOnly", self.player),
                        rule=lambda state: state.has_from_list(
                            {
                                "SniperMonkey-TUnlock", "MonkeySub-TUnlock",
                                "MonkeyBuccaneer-TUnlock", "MonkeyAce-TUnlock",
                                "HeliPilot-TUnlock", "MortarMonkey-TUnlock",
                                "DartlingGunner-TUnlock",
                            },
                            self.player, 2,
                        ),
                    )
            if "MagicOnly" in self.map_modes[name]:
                if self.options.category_lock.value:
                    add_rule(
                        self.multiworld.get_location(f"{name}-MagicOnly", self.player),
                        rule=lambda state: state.has("Magic Monkeys", self.player),
                    )
                else:
                    add_rule(
                        self.multiworld.get_location(f"{name}-MagicOnly", self.player),
                        rule=lambda state: state.has_from_list(
                            {
                                "WizardMonkey-TUnlock", "SuperMonkey-TUnlock",
                                "NinjaMonkey-TUnlock", "Alchemist-TUnlock",
                                "Druid-TUnlock", "Mermonkey-TUnlock",
                            },
                            self.player, 2,
                        ),
                    )

            # Attach capability-based access rules to all medal locations
            set_map_rules(self, name)

            # Handle Round Sanity Checks for this map
            round_check_set: set[int] = set()
            if self.options.round_sanity.value > 0:
                interval = self.options.round_sanity.value
                r = interval
                while r <= 100:
                    round_check_set.add(r)
                    r += interval
            for r_str in self.options.custom_round_checks.value:
                try:
                    round_check_set.add(int(r_str))
                except ValueError:
                    pass
            for r in sorted(round_check_set):
                loc_name = f"{name}-Round {r}"
                region.add_locations(
                    {loc_name: self.bloonsMapData.locations[loc_name]}
                )
                set_round_rule(self, name, r)
        # endregion

        # region Hero Locations
        for hero in Shared.heroIDs:
            region = Region(hero, self.player, self.multiworld)
            region.add_locations({hero: self.bloonsMapData.locations[hero]}, BTD6Hero)
            hero_select_region.connect(
                region, rule=lambda state, h=hero: state.has(h + "-HUnlock", self.player)
            )
            self.multiworld.regions.append(region)
        # endregion

        # region Level Locations
        # Levels are split into 9 XP-sphere sub-regions so the AP solver spreads items
        # across the full level range rather than dumping everything into sphere 1.
        #
        # Cumulative XP thresholds (raw XP):
        #   Sphere 1 : <250 000
        #   Sphere 2 : 250 000 – 500 000
        #   Sphere 3 : 500 000 – 1 000 000
        #   Sphere 4 : 1 000 000 – 5 000 000
        #   Sphere 5 : 5 000 000 – 15 000 000
        #   Sphere 6 : 15 000 000 – 30 000 000
        #   Sphere 7 : 30 000 000 – 60 000 000
        #   Sphere 8 : 60 000 000 – 120 000 000
        #   Sphere 9 : 120 000 000+
        XP_THRESHOLDS = [0, 250_000, 500_000, 1_000_000, 5_000_000, 15_000_000, 30_000_000, 60_000_000, 120_000_000]

        SPHERE_MEDAL_PCTS = [0, 10, 20, 35, 50, 63, 75, 85, 93]

        total_medals = self.options.total_medals.value

        xp_sphere_regions = []
        for s in range(9):
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
            upgrade_sanity_on = bool(self.options.upgrade_sanity.value)
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
                # When upgrade_sanity is on, T4/T5 require at least one path item —
                # without a path the player can't buy T4/T5 upgrades to accumulate pops.
                if upgrade_sanity_on:
                    path_items = [f"{monkey}-TopPath", f"{monkey}-MiddlePath", f"{monkey}-BottomPath"]
                    for tier in ("Tier4", "Tier5"):
                        add_rule(
                            self.multiworld.get_location(f"{monkey}-{tier}", self.player),
                            rule=lambda state, pi=path_items: state.has_from_list(pi, self.player, 1),
                        )
        # endregion

        # region Knowledge Locations
        if not self.options.progressive_knowledge.value:
            knowledge_region = Region("Knowledge Tree", self.player, self.multiworld)
            self.multiworld.regions.append(knowledge_region)
            menu_region.connect(knowledge_region)

            for kname in Shared.knowledgeIDs:
                knowledge_region.add_locations(
                    {kname + "-Tree": self.bloonsMapData.locations[f"{kname}-Tree"]},
                    BTD6Knowledge,
                )
                add_rule(
                    self.multiworld.get_location(kname + "-Tree", self.player),
                    rule=lambda state, k=kname: state.has(k + "-KUnlock", self.player),
                )
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
        medals_needed = int(round(self.options.total_medals.value * (self.options.medalreq.value / 100)))
        category_lock = bool(self.options.category_lock.value)
        elite_boss = self.options.goal.value == 2
        if elite_boss:
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has(BloonsItems.MEDAL_NAME, self.player, medals_needed)
                and has_economy(state, self.player, category_lock)
            )
        else:
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has(BloonsItems.MEDAL_NAME, self.player, medals_needed)
            )

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "victoryLocation": self.victory_map_name,
            "medalsNeeded": int(round(self.options.total_medals.value * (self.options.medalreq.value / 100))),
            "xpCurve": bool(self.options.xp_curve.value),
            "staticXPReq": int(self.options.static_req.value),
            "maxLevel": int(self.options.max_level.value),
            "mapModes": {k: list(v) for k, v in self.map_modes.items()},
            "goalMode": self.goal_mode,
            "popTierChecks": bool(self.options.pop_tier_checks.value),
            "tier3PopRequirement": int(self.options.tier3_pop_requirement.value),
            "tier4PopRequirement": int(self.options.tier4_pop_requirement.value),
            "tier5PopRequirement": int(self.options.tier5_pop_requirement.value),
            "progressiveKnowledge": bool(self.options.progressive_knowledge.value),
            "roundSanity": int(self.options.round_sanity.value),
            "customRoundChecks": sorted(int(r) for r in self.options.custom_round_checks.value),
            "progressivePrices": bool(self.options.progressive_prices.value),
            "categoryLock": bool(self.options.category_lock.value),
            "upgradeSanity": bool(self.options.upgrade_sanity.value),
            "goal": int(self.options.goal.value),
            "deathLink": bool(self.options.death_link.value),
            # Fields used by the Universal Tracker to reconstruct the exact same world.
            "startingMaps": self.starting_maps,
            "includedMaps": self.included_maps,
            "startingMonkeys": self.starting_monkeys,
            "startingHero": self.starting_hero,
            "availableHeroes": self.available_heroes,
            "remainingCategories": self.remaining_categories,
        }
