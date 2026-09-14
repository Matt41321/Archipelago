from __future__ import annotations

from typing import Callable, TYPE_CHECKING
from worlds.generic.Rules import add_rule
from .Utils import Shared

if TYPE_CHECKING:
    from . import BTD6World

# Towers affordable at start that deal damage.
STARTING_DAMAGE_TOWERS: frozenset = frozenset({
    "DartMonkey",
    "BoomerangMonkey",
    "BombShooter",
    "TackShooter",
    "Desperado",
    "IceMonkey",
    "SniperMonkey",
    "MonkeySub",
    "MonkeyBuccaneer",
    "WizardMonkey",
    "NinjaMonkey",
    "Druid",
    "Mermonkey",
    "EngineerMonkey",
    "BeastHandler",
})

# All damage-dealing towers.
DAMAGE_TOWERS: frozenset = frozenset({
    "DartMonkey-TUnlock",
    "BoomerangMonkey-TUnlock",
    "BombShooter-TUnlock",
    "TackShooter-TUnlock",
    "Desperado-TUnlock",
    "IceMonkey-TUnlock",
    "SniperMonkey-TUnlock",
    "MonkeySub-TUnlock",
    "MonkeyBuccaneer-TUnlock",
    "MonkeyAce-TUnlock",
    "HeliPilot-TUnlock",
    "MortarMonkey-TUnlock",
    "DartlingGunner-TUnlock",
    "WizardMonkey-TUnlock",
    "SuperMonkey-TUnlock",
    "NinjaMonkey-TUnlock",
    "Druid-TUnlock",
    "Mermonkey-TUnlock",
    "SpikeFactory-TUnlock",
    "EngineerMonkey-TUnlock",
    "BeastHandler-TUnlock",
    "Skywarden-TUnlock",
})

# Towers that can detect/pop camo bloons.
CAMO_CAPABLE_TOWERS: frozenset = frozenset({
    "DartMonkey-TUnlock",
    "IceMonkey-TUnlock",
    "Desperado-TUnlock",
    "SniperMonkey-TUnlock",
    "MonkeySub-TUnlock",
    "MonkeyBuccaneer-TUnlock",
    "MonkeyAce-TUnlock",
    "HeliPilot-TUnlock",
    "MortarMonkey-TUnlock",
    "DartlingGunner-TUnlock",
    "WizardMonkey-TUnlock",
    "SuperMonkey-TUnlock",
    "NinjaMonkey-TUnlock",
    "Mermonkey-TUnlock",
    "SpikeFactory-TUnlock",
    "MonkeyVillage-TUnlock",
    "EngineerMonkey-TUnlock",
    "Skywarden-TUnlock"
})

# Towers that can deal with DDTs.
DDT_COUNTER_TOWERS: frozenset = frozenset({
    "IceMonkey-TUnlock",
    "GlueGunner-TUnlock",
    "Desperado-TUnlock",
    "SniperMonkey-TUnlock",
    "MonkeyBuccaneer-TUnlock",
    "MonkeyAce-TUnlock",
    "HeliPilot-TUnlock",
    "WizardMonkey-TUnlock",
    "SuperMonkey-TUnlock",
    "SpikeFactory-TUnlock",
    "MonkeyVillage-TUnlock",
})

# Income towers.
ECONOMY_TOWERS: frozenset = frozenset({"BananaFarm-TUnlock"})

# Water towers.
WATER_TOWERS: frozenset = frozenset({
    "MonkeySub-TUnlock",
    "MonkeyBuccaneer-TUnlock",
    "Mermonkey-TUnlock",
})

# All 26 towers — used for n_towers counting.
ALL_TOWERS: frozenset = frozenset({
    "DartMonkey-TUnlock",
    "BoomerangMonkey-TUnlock",
    "BombShooter-TUnlock",
    "TackShooter-TUnlock",
    "IceMonkey-TUnlock",
    "GlueGunner-TUnlock",
    "SniperMonkey-TUnlock",
    "MonkeySub-TUnlock",
    "MonkeyBuccaneer-TUnlock",
    "MonkeyAce-TUnlock",
    "HeliPilot-TUnlock",
    "MortarMonkey-TUnlock",
    "DartlingGunner-TUnlock",
    "WizardMonkey-TUnlock",
    "SuperMonkey-TUnlock",
    "NinjaMonkey-TUnlock",
    "Alchemist-TUnlock",
    "Druid-TUnlock",
    "Mermonkey-TUnlock",
    "BananaFarm-TUnlock",
    "SpikeFactory-TUnlock",
    "MonkeyVillage-TUnlock",
    "EngineerMonkey-TUnlock",
    "BeastHandler-TUnlock",
    "Desperado-TUnlock",
    "Skywarden-TUnlock"
})

LAND_TOWERS: frozenset = ALL_TOWERS - WATER_TOWERS

LAND_DAMAGE_TOWERS: frozenset = DAMAGE_TOWERS - WATER_TOWERS
LAND_CAMO_TOWERS: frozenset = CAMO_CAPABLE_TOWERS - WATER_TOWERS

CAMO_HEROES: frozenset = frozenset({"Etienne-HUnlock", "Quincy-HUnlock", "Silas-HUnlock", "Ezili-HUnlock", "Sauda-HUnlock", "Geraldo-HUnlock"})

ECONOMY_HEROES: frozenset = frozenset({"Benjamin-HUnlock", "Geraldo-HUnlock"})

# Minimum towers required per map tier and mode.
TOWER_REQUIREMENTS: dict = {
    "beginner":     {"Easy": 1, "Medium": 1, "Hard": 3, "Impoppable": 4, "Chimps": 4},
    "intermediate": {"Easy": 1, "Medium": 2, "Hard": 4, "Impoppable": 7, "Chimps": 7},
    "advanced":     {"Easy": 3, "Medium": 4, "Hard": 9, "Impoppable": 13, "Chimps": 13},
    "expert":       {"Easy": 5, "Medium": 7, "Hard": 13, "Impoppable": 16, "Chimps": 16},
}

ALL_PATHS: frozenset = frozenset(
    f"{monkey}-{path}" for monkey in Shared.monkeyIDs for path in Shared.pathNames
)

# Minimum upgrade-path items required per map tier and mode. When Upgrade Sanity is enabled.
PATH_REQUIREMENTS: dict = {
    "beginner":     {"Easy": 0, "Medium": 1, "Hard": 3,  "Impoppable": 6,  "Chimps": 6},
    "intermediate": {"Easy": 0, "Medium": 2, "Hard": 6,  "Impoppable": 14, "Chimps": 14},
    "advanced":     {"Easy": 3, "Medium": 6, "Hard": 12, "Impoppable": 20, "Chimps": 20},
    "expert":       {"Easy": 6, "Medium": 15, "Hard": 25, "Impoppable": 30, "Chimps": 30},
}

# Alt modes use tower counts from their base mode.
_ALT_MODE_BASE: dict = {
    "Deflation":             "Medium",
    "HalfCash":              "Hard",
    "Reverse":               "Hard",
    "Apopalypse":            "Hard",
    "DoubleMoabHealth":      "Impoppable",
    "AlternateBloonsRounds": "Impoppable",
}

# Maps that require a water tower.
_WATER_REQUIRED_MAPS: frozenset = frozenset({"Erosion", "FloodedValley", "PatsPond", "Peninsula"})

# Maps with no water at all, so they don't count towards required tower count.
_NO_WATER_MAPS: frozenset = frozenset({
    # Beginner
    "MonkeyMeadow", "TreeStump", "TownCentre", "OneTwoTree", "Scrapyard", "AlpineRun", "Hedge",
    # Intermediate
    "LostCrevasse", "CoveredGarden", "QuietStreet", "Encrypted", "Bazaar", "KartsNDarts",
    "MoonLanding", "Cracked",
    # Advanced
    "MushroomGrotto", "PartyParade", "SunsetGulch", "LastResort", "CastleRevenge",
    "MidnightMansion", "SunkenColumns", "XFactor", "Mesa", "Geared", "Spillway", "Cornfield",
    "Underground",
    # Expert
    "TrickyTracks", "GlacialTrail", "DarkDungeons", "Ravine", "Workshop",
})

# Valid CHIMPS starting strategies per expert map.
# Passes if the player has all items in any one strategy.
# Bypassed in category_lock mode.
_EXPERT_CHIMPS_STARTS: dict = {
    "TrickyTracks": [
        frozenset({"DartMonkey-TUnlock"}),
        frozenset({"Desperado-TUnlock"}),
    ],
    "GlacialTrail": [
        frozenset({"EngineerMonkey-TUnlock", "DartMonkey-TUnlock"}),
        frozenset({"DartMonkey-TUnlock", "NinjaMonkey-TUnlock"}),
        frozenset({"Sauda-HUnlock"}),
    ],
    "DarkDungeons": [
        frozenset({"DartMonkey-TUnlock"}),
    ],
    "Sanctuary": [
        frozenset({"Desperado-TUnlock"}),
        frozenset({"DartMonkey-TUnlock"}),
    ],
    "Ravine": [
        frozenset({"DartMonkey-TUnlock"}),
        frozenset({"Desperado-TUnlock"}),
    ],
    "FloodedValley": [
        frozenset({"Mermonkey-TUnlock"}),
        frozenset({"MonkeySub-TUnlock"}),
    ],
    "Infernal": [
        frozenset({"Quincy-HUnlock", "DartMonkey-TUnlock"}),
        frozenset({"BoomerangMonkey-TUnlock", "DartMonkey-TUnlock"}),
    ],
    "BloodyPuddles": [
        frozenset({"Desperado-TUnlock"}),
        frozenset({"DartMonkey-TUnlock", "MonkeySub-TUnlock"}),
    ],
    "Workshop": [
        frozenset({"DartMonkey-TUnlock"}),
    ],
    "Quad": [
        frozenset({"DartMonkey-TUnlock"}),
        frozenset({"Desperado-TUnlock"}),
    ],
    "DarkCastle": [
        frozenset({"DartMonkey-TUnlock", "MonkeySub-TUnlock"}),
    ],
    "MuddyPuddles": [
        frozenset({"MonkeyBuccaneer-TUnlock"}),
        frozenset({"Desperado-TUnlock"}),
    ],
    "#ouch": [
        frozenset({"Desperado-TUnlock"}),
        frozenset({"DartMonkey-TUnlock", "MonkeySub-TUnlock"}),
    ],
}

# The hardest, 100-round modes. Both get the CHIMPS-style access restrictions
# (valid expert starting strategy + a Progressive Prices item when enabled).
_CHIMPS_LIKE_MODES: tuple = ("Chimps", "Impoppable")

# Category fallbacks for category_lock mode.
_ANY_CATEGORY: frozenset = frozenset({
    "Primary Monkeys",
    "Military Monkeys",
    "Magic Monkeys",
    "Support Monkeys",
})

# Only Support Monkeys contains BananaFarm.
_ECONOMY_CATEGORY: frozenset = frozenset({"Support Monkeys"})

# Military and Magic categories have water towers.
_WATER_CATEGORIES: frozenset = frozenset({"Military Monkeys", "Magic Monkeys"})


def _get_map_tier(world: "BTD6World", map_name: str) -> str:
    for tier, names in world.bloonsMapData.map_names_by_difficulty.items():
        if map_name in names:
            return tier
    return "beginner"


def has_damage(state, player: int, category_lock: bool, no_water: bool = False) -> bool:
    if category_lock:
        return state.has_from_list(_ANY_CATEGORY, player, 1)
    pool = LAND_DAMAGE_TOWERS if no_water else DAMAGE_TOWERS
    return state.has_from_list(pool, player, 1)


def has_camo_detection(state, player: int, category_lock: bool, no_water: bool = False) -> bool:
    if category_lock:
        return state.has_from_list(_ANY_CATEGORY, player, 1)
    pool = LAND_CAMO_TOWERS if no_water else CAMO_CAPABLE_TOWERS
    return (
        state.has_from_list(pool, player, 1)
        or state.has_from_list(CAMO_HEROES, player, 1)
    )


def has_ddt_counter(state, player: int, category_lock: bool) -> bool:
    if category_lock:
        return state.has_from_list(_ANY_CATEGORY, player, 1)
    return state.has_from_list(DDT_COUNTER_TOWERS, player, 1)


def has_economy(state, player: int, category_lock: bool) -> bool:
    if category_lock:
        return state.has("Support Monkeys", player)
    return (
        state.has_from_list(ECONOMY_TOWERS, player, 1)
        or state.has_from_list(ECONOMY_HEROES, player, 1)
    )


def has_chimps_start(state, player: int, category_lock: bool, strategies) -> bool:
    if category_lock:
        return True
    return any(
        all(state.has(item, player) for item in strategy)
        for strategy in strategies
    )


def has_water_tower(state, player: int, category_lock: bool) -> bool:
    if category_lock:
        return state.has_from_list(_WATER_CATEGORIES, player, 1)
    return state.has_from_list(WATER_TOWERS, player, 1)


def n_towers(state, player: int, k: int, category_lock: bool, no_water: bool = False) -> bool:
    if category_lock:
        return True
    pool = LAND_TOWERS if no_water else ALL_TOWERS
    return state.has_from_list(pool, player, k)


def n_paths(state, player: int, k: int, upgrade_sanity: bool) -> bool:
    # A path only counts if its monkey is also unlocked.
    if not upgrade_sanity or k <= 0:
        return True
    usable = 0
    for monkey in Shared.monkeyIDs:
        if not state.has(f"{monkey}-TUnlock", player):
            continue
        for path in Shared.pathNames:
            if state.has(f"{monkey}-{path}", player):
                usable += 1
                if usable >= k:
                    return True
    return usable >= k


def _rule_easy(state, p: int, cl: bool, towers: int, no_water: bool, paths: int, upgrade_sanity: bool) -> bool:
    return (
        has_damage(state, p, cl, no_water)
        and has_camo_detection(state, p, cl, no_water)
        and n_towers(state, p, towers, cl, no_water)
        and n_paths(state, p, paths, upgrade_sanity)
    )


def _rule_medium(state, p: int, cl: bool, towers: int, no_water: bool, paths: int, upgrade_sanity: bool) -> bool:
    return (
        has_damage(state, p, cl, no_water)
        and has_camo_detection(state, p, cl, no_water)
        and n_towers(state, p, towers, cl, no_water)
        and n_paths(state, p, paths, upgrade_sanity)
    )


def _rule_hard(state, p: int, cl: bool, towers: int, no_water: bool, paths: int, upgrade_sanity: bool) -> bool:
    return (
        has_damage(state, p, cl, no_water)
        and has_camo_detection(state, p, cl, no_water)
        and n_towers(state, p, towers, cl, no_water)
        and n_paths(state, p, paths, upgrade_sanity)
    )


def _rule_impoppable(state, p: int, cl: bool, towers: int, no_water: bool, paths: int, upgrade_sanity: bool) -> bool:
    return (
        has_damage(state, p, cl, no_water)
        and has_camo_detection(state, p, cl, no_water)
        and has_ddt_counter(state, p, cl)
        and n_towers(state, p, towers, cl, no_water)
        and n_paths(state, p, paths, upgrade_sanity)
    )


def _rule_chimps(state, p: int, cl: bool, towers: int, no_water: bool, paths: int, upgrade_sanity: bool) -> bool:
    return (
        has_damage(state, p, cl, no_water)
        and has_camo_detection(state, p, cl, no_water)
        and has_ddt_counter(state, p, cl)
        and n_towers(state, p, towers, cl, no_water)
        and n_paths(state, p, paths, upgrade_sanity)
    )


def _rule_deflation(state, p: int, cl: bool, towers: int, no_water: bool, paths: int, upgrade_sanity: bool) -> bool:
    # No DDTs in Deflation.
    return (
        has_damage(state, p, cl, no_water)
        and has_camo_detection(state, p, cl, no_water)
        and n_towers(state, p, towers, cl, no_water)
        and n_paths(state, p, paths, upgrade_sanity)
    )


_MODE_RULE_FN = {
    "Easy":                  _rule_easy,
    "Medium":                _rule_medium,
    "Hard":                  _rule_hard,
    "Impoppable":            _rule_impoppable,
    "Chimps":                _rule_chimps,
    "Deflation":             _rule_deflation,
    "HalfCash":              _rule_hard,
    "DoubleMoabHealth":      _rule_impoppable,
    "AlternateBloonsRounds": _rule_impoppable,
    "Reverse":               _rule_hard,
    "Apopalypse":            _rule_hard,
}

PRIMARY_ONLY_TOWERS: frozenset = frozenset({
    "DartMonkey-TUnlock", "BoomerangMonkey-TUnlock", "BombShooter-TUnlock",
    "TackShooter-TUnlock", "IceMonkey-TUnlock", "GlueGunner-TUnlock", "Desperado-TUnlock",
})
MILITARY_ONLY_TOWERS: frozenset = frozenset({
    "SniperMonkey-TUnlock", "MonkeySub-TUnlock", "MonkeyBuccaneer-TUnlock",
    "MonkeyAce-TUnlock", "HeliPilot-TUnlock", "MortarMonkey-TUnlock", "DartlingGunner-TUnlock",
})
MAGIC_ONLY_TOWERS: frozenset = frozenset({
    "WizardMonkey-TUnlock", "SuperMonkey-TUnlock", "NinjaMonkey-TUnlock",
    "Alchemist-TUnlock", "Druid-TUnlock", "Mermonkey-TUnlock", "Skywarden-TUnlock",
})

_ONLY_MODE_DATA: dict = {
    "PrimaryOnly":  ("Primary Monkeys",  PRIMARY_ONLY_TOWERS),
    "MilitaryOnly": ("Military Monkeys", MILITARY_ONLY_TOWERS),
    "MagicOnly":    ("Magic Monkeys",    MAGIC_ONLY_TOWERS),
}

_MODE_DIFFICULTY: dict = {
    "Easy": "Easy", "PrimaryOnly": "Easy", "Deflation": "Easy",
    "Medium": "Medium", "MilitaryOnly": "Medium", "Reverse": "Medium", "Apopalypse": "Medium",
    "Hard": "Hard", "MagicOnly": "Hard", "DoubleMoabHealth": "Hard",
    "HalfCash": "Hard", "AlternateBloonsRounds": "Hard",
    "Impoppable": "Impoppable", "Chimps": "Chimps",
}

_DIFFICULTY_MAX_ROUND: dict = {
    "Easy": 40, "Medium": 60, "Hard": 80, "Impoppable": 100, "Chimps": 100,
}


def _mode_max_round(mode: str) -> int:
    return _DIFFICULTY_MAX_ROUND.get(_MODE_DIFFICULTY.get(mode, "Hard"), 80)


def max_reachable_round(world: "BTD6World", map_name: str) -> int:
    """Highest round playable on this map given its assigned modes (0 if none)."""
    modes = world.map_modes.get(map_name, [])
    if not modes:
        return 0
    return max(_mode_max_round(m) for m in modes)


def mode_access_rule(world: "BTD6World", map_name: str, mode: str) -> Callable:
    """Access rule for a single (map, mode), matching its medal-location logic."""
    player = world.player
    category_lock = bool(world.options.category_lock.value)
    if mode in _ONLY_MODE_DATA:
        category_item, towers = _ONLY_MODE_DATA[mode]
        if category_lock:
            return lambda state, p=player, c=category_item: state.has(c, p)
        return lambda state, p=player, ts=towers: state.has_from_list(ts, p, 2)
    tier = _get_map_tier(world, map_name)
    upgrade_sanity = bool(world.options.upgrade_sanity.value)
    rule = _make_rule(mode, tier, player, category_lock, map_name in _NO_WATER_MAPS, upgrade_sanity)
    if rule is None:
        return lambda state: True
    return rule


def _make_rule(
    mode: str, tier: str, player: int, category_lock: bool, no_water: bool, upgrade_sanity: bool
) -> Callable | None:
    fn = _MODE_RULE_FN.get(mode)
    if fn is None:
        return None
    base_mode = _ALT_MODE_BASE.get(mode, mode)
    towers = TOWER_REQUIREMENTS[tier][base_mode]
    paths = PATH_REQUIREMENTS[tier][base_mode]
    return lambda state, p=player, cl=category_lock, t=towers, nw=no_water, pa=paths, us=upgrade_sanity: (
        fn(state, p, cl, t, nw, pa, us)
    )


def _apply_to_all_active_modes(world: "BTD6World", map_name: str, rule: Callable) -> None:
    """Add rule to every active mode location for this map."""
    player = world.player
    for mode in world.map_modes.get(map_name, []):
        add_rule(world.multiworld.get_location(f"{map_name}-{mode}", player), rule)


def set_map_rules(world: "BTD6World", map_name: str) -> None:
    player = world.player
    category_lock = bool(world.options.category_lock.value)
    tier = _get_map_tier(world, map_name)
    map_modes = world.map_modes.get(map_name, [])
    no_water = map_name in _NO_WATER_MAPS
    upgrade_sanity = bool(world.options.upgrade_sanity.value)

    for mode in map_modes:
        rule = _make_rule(mode, tier, player, category_lock, no_water, upgrade_sanity)
        if rule is not None:
            add_rule(
                world.multiworld.get_location(f"{map_name}-{mode}", player),
                rule,
            )

    if map_name in _WATER_REQUIRED_MAPS:
        water_rule = lambda state, p=player, cl=category_lock: has_water_tower(state, p, cl)
        _apply_to_all_active_modes(world, map_name, water_rule)

    # CHIMPS and Impoppable share the same restrictions: an expert map's valid
    # starting strategy, plus (when progressive prices is on) at least one
    # Progressive Prices item.
    for mode in _CHIMPS_LIKE_MODES:
        if mode not in map_modes:
            continue
        loc = world.multiworld.get_location(f"{map_name}-{mode}", player)

        if map_name in _EXPERT_CHIMPS_STARTS:
            strategies = _EXPERT_CHIMPS_STARTS[map_name]
            add_rule(loc, lambda state, p=player, cl=category_lock, s=strategies: has_chimps_start(state, p, cl, s))

        if tier in ("advanced", "expert") and world.options.progressive_prices.value:
            add_rule(loc, lambda state, p=player: state.has("Progressive Prices", p, 1))


def set_round_rule(world: "BTD6World", map_name: str, round_n: int) -> None:
    player = world.player
    loc = world.multiworld.get_location(f"{map_name}-Round {round_n}", player)

    reaching_modes = [
        m for m in world.map_modes.get(map_name, [])
        if _mode_max_round(m) >= round_n
    ]
    if reaching_modes:
        sub_rules = [mode_access_rule(world, map_name, m) for m in reaching_modes]
        add_rule(loc, lambda state, rs=sub_rules: any(r(state) for r in rs))

    if map_name in _WATER_REQUIRED_MAPS:
        category_lock = bool(world.options.category_lock.value)
        water_rule = lambda state, p=player, cl=category_lock: has_water_tower(state, p, cl)
        add_rule(loc, water_rule)
