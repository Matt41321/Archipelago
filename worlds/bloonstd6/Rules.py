from __future__ import annotations

from typing import Callable, TYPE_CHECKING
from worlds.generic.Rules import add_rule

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

# All 25 towers — used for n_towers counting.
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
})

# Heroes with camo detection.
CAMO_HEROES: frozenset = frozenset({"Etienne-HUnlock", "Quincy-HUnlock", "Silas-HUnlock", "Ezili-HUnlock", "Sauda-HUnlock", "Geraldo-HUnlock"})

# Heroes that provide income.
ECONOMY_HEROES: frozenset = frozenset({"Benjamin-HUnlock", "Geraldo-HUnlock"})

# Minimum towers required per map tier and mode.
TOWER_REQUIREMENTS: dict = {
    "beginner":     {"Easy": 1, "Medium": 1, "Hard": 3, "Impoppable": 4, "Chimps": 4},
    "intermediate": {"Easy": 1, "Medium": 2, "Hard": 3, "Impoppable": 5, "Chimps": 5},
    "advanced":     {"Easy": 2, "Medium": 3, "Hard": 4, "Impoppable": 7, "Chimps": 7},
    "expert":       {"Easy": 4, "Medium": 4, "Hard": 6, "Impoppable": 10, "Chimps": 10},
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


def has_damage(state, player: int, category_lock: bool) -> bool:
    if category_lock:
        return state.has_from_list(_ANY_CATEGORY, player, 1)
    return state.has_from_list(DAMAGE_TOWERS, player, 1)


def has_camo_detection(state, player: int, category_lock: bool) -> bool:
    if category_lock:
        return state.has_from_list(_ANY_CATEGORY, player, 1)
    return (
        state.has_from_list(CAMO_CAPABLE_TOWERS, player, 1)
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


def n_towers(state, player: int, k: int, category_lock: bool) -> bool:
    if category_lock:
        return True
    return state.has_from_list(ALL_TOWERS, player, k)


def _rule_easy(state, p: int, cl: bool, towers: int) -> bool:
    return (
        has_damage(state, p, cl)
        and has_camo_detection(state, p, cl)
        and n_towers(state, p, towers, cl)
    )


def _rule_medium(state, p: int, cl: bool, towers: int) -> bool:
    return (
        has_damage(state, p, cl)
        and has_camo_detection(state, p, cl)
        and n_towers(state, p, towers, cl)
    )


def _rule_hard(state, p: int, cl: bool, towers: int) -> bool:
    return (
        has_damage(state, p, cl)
        and has_camo_detection(state, p, cl)
        and n_towers(state, p, towers, cl)
    )


def _rule_impoppable(state, p: int, cl: bool, towers: int) -> bool:
    return (
        has_damage(state, p, cl)
        and has_camo_detection(state, p, cl)
        and has_ddt_counter(state, p, cl)
        and n_towers(state, p, towers, cl)
    )


def _rule_chimps(state, p: int, cl: bool, towers: int) -> bool:
    return (
        has_damage(state, p, cl)
        and has_camo_detection(state, p, cl)
        and has_ddt_counter(state, p, cl)
        and n_towers(state, p, towers, cl)
    )


def _rule_deflation(state, p: int, cl: bool, towers: int) -> bool:
    # No DDTs in Deflation.
    return (
        has_damage(state, p, cl)
        and has_camo_detection(state, p, cl)
        and n_towers(state, p, towers, cl)
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

# Round thresholds mapped to mode difficulty for tower-count lookup.
_ROUND_TIER_RULES = [
    (40,  "Easy"),
    (60,  "Medium"),
    (80,  "Hard"),
    (100, "Impoppable"),
]


def _make_rule(mode: str, tier: str, player: int, category_lock: bool) -> Callable | None:
    fn = _MODE_RULE_FN.get(mode)
    if fn is None:
        return None
    base_mode = _ALT_MODE_BASE.get(mode, mode)
    towers = TOWER_REQUIREMENTS[tier][base_mode]
    return lambda state, p=player, cl=category_lock, t=towers: fn(state, p, cl, t)


def _apply_to_all_active_modes(world: "BTD6World", map_name: str, rule: Callable) -> None:
    """Add rule to every active mode location for this map."""
    from .Options import Difficulty
    player = world.player
    difficulty = world.options.rando_difficulty.value

    for mode in ("Easy", "Medium", "Hard", "Impoppable"):
        add_rule(world.multiworld.get_location(f"{map_name}-{mode}", player), rule)

    if difficulty >= Difficulty.option_Advanced:
        add_rule(world.multiworld.get_location(f"{map_name}-Chimps", player), rule)

    if difficulty == Difficulty.option_Expert:
        for mode in ("Deflation", "Apopalypse", "Reverse",
                     "DoubleMoabHealth", "HalfCash", "AlternateBloonsRounds"):
            add_rule(world.multiworld.get_location(f"{map_name}-{mode}", player), rule)


def set_map_rules(world: "BTD6World", map_name: str) -> None:
    from .Options import Difficulty

    player = world.player
    category_lock = bool(world.options.category_lock.value)
    difficulty = world.options.rando_difficulty.value
    tier = _get_map_tier(world, map_name)

    for mode in ("Easy", "Medium", "Hard", "Impoppable"):
        rule = _make_rule(mode, tier, player, category_lock)
        add_rule(
            world.multiworld.get_location(f"{map_name}-{mode}", player),
            rule,
        )

    if difficulty >= Difficulty.option_Advanced:
        rule = _make_rule("Chimps", tier, player, category_lock)
        add_rule(
            world.multiworld.get_location(f"{map_name}-Chimps", player),
            rule,
        )

    # Expert alt modes
    if difficulty == Difficulty.option_Expert:
        for mode in ("Deflation", "Apopalypse", "Reverse",
                     "DoubleMoabHealth", "HalfCash", "AlternateBloonsRounds"):
            rule = _make_rule(mode, tier, player, category_lock)
            add_rule(
                world.multiworld.get_location(f"{map_name}-{mode}", player),
                rule,
            )

    if map_name in _WATER_REQUIRED_MAPS:
        water_rule = lambda state, p=player, cl=category_lock: has_water_tower(state, p, cl)
        _apply_to_all_active_modes(world, map_name, water_rule)

    if difficulty >= Difficulty.option_Advanced and map_name in _EXPERT_CHIMPS_STARTS:
        strategies = _EXPERT_CHIMPS_STARTS[map_name]
        start_rule = lambda state, p=player, cl=category_lock, s=strategies: has_chimps_start(state, p, cl, s)
        add_rule(
            world.multiworld.get_location(f"{map_name}-Chimps", player),
            start_rule,
        )

    if (
        tier in ("advanced", "expert")
        and difficulty >= Difficulty.option_Advanced
        and world.options.progressive_prices.value
    ):
        prices_rule = lambda state, p=player: state.has("Progressive Prices", p, 1)
        add_rule(
            world.multiworld.get_location(f"{map_name}-Chimps", player),
            prices_rule,
        )


def set_round_rule(world: "BTD6World", map_name: str, round_n: int) -> None:
    player = world.player
    category_lock = bool(world.options.category_lock.value)
    tier = _get_map_tier(world, map_name)

    mode = "Impoppable"
    for threshold, tier_mode in _ROUND_TIER_RULES:
        if round_n <= threshold:
            mode = tier_mode
            break

    towers = TOWER_REQUIREMENTS[tier][mode]
    fn = _MODE_RULE_FN[mode]
    rule = lambda state, p=player, cl=category_lock, t=towers: fn(state, p, cl, t)
    loc = world.multiworld.get_location(f"{map_name}-Round {round_n}", player)
    add_rule(loc, rule)

    if map_name in _WATER_REQUIRED_MAPS:
        water_rule = lambda state, p=player, cl=category_lock: has_water_tower(state, p, cl)
        add_rule(loc, water_rule)
