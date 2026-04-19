from Options import Choice, Toggle, Range, DeathLink, OptionDict, OptionGroup, OptionSet, PerGameCommonOptions
from dataclasses import dataclass


class StartingMaps(Range):
    """The number of maps that will be automatically unlocked at the start."""

    range_start = 1
    range_end = 6
    default = 3
    display_name = "Starting Map Count"


class TotalMaps(Range):
    """
    The number of maps to be included (not including starting maps).
    This determines the number of \"Medal\" Items that are in the game in relation to your Randomizer Difficulty.
    """

    range_start = 10
    range_end = 85
    default = 15
    display_name = "Total Map Count"


class MinMapDiff(Range):
    """
    The Minimum Map Difficulty for selected maps (including starting and goal map)

    0 = Beginner
    1 = Intermediate
    2 = Advanced
    3 = Expert
    """

    range_start = 0
    range_end = 3
    default = 0
    display_name = "Minimum Map Difficulty"


class MaxMapDiff(Range):
    """
    The Maximum Map Difficulty for selected maps (including starting and goal map)

    0 = Beginner
    1 = Intermediate
    2 = Advanced
    3 = Expert
    """

    range_start = 0
    range_end = 3
    default = 3
    display_name = "Maximum Map Difficulty"


class Difficulty(Choice):
    """
    The difficulty of the randomizer.

    Basic: The Easy, Medium, Hard, and Impoppable Medals all send checks.
    Advanced: The Easy, Medium, Hard, Impoppable, and Chimps Medals all send checks.
    Expert: All Medals send checks.
    Note: Completing milestone rounds on higher difficulties will send checks related to the lower difficulties (i.e. completing round 60 on Impoppable will send the Medium check for that map)
    """

    display_name = "Difficulty"
    option_Basic = 4
    option_Advanced = 5
    option_Expert = 14
    default = 4


class TotalMedals(Range):
    """
    The total number of Medal items placed in the item pool.
    These are the collectables required to unlock the goal map.
    """

    display_name = "Total Medals"
    range_start = 20
    range_end = 100
    default = 60


class MedalRequirementPercentage(Range):
    """
    The Percentage of the Total Medals required for you to access the Goal Map

    For my own sanity and the randomizers this is hard bottomed at 50% so it can't be cheesed
    """

    display_name = "Medal Requirement Percentage"
    range_start = 50
    range_end = 100
    default = 60


class StartingMonkeys(Toggle):
    """
    Would you like to randomize all starting monkeys or include the Dart Monkey in the starting monkeys?
    Only relevant if Category Lock is disabled.

    True/On: All Starting Monkeys will be random.
    False/Off: The first starting monkey no matter how many you include will always be the Dart Monkey.
    """

    display_name = "Random Starting Monkeys"


class StartingMonkeyAmount(Range):
    """
    How many random starting Monkeys would you like?
    Only relevant if Category Lock is disabled.

    Min: 1
    Max: 25
    """

    range_start = 1
    range_end = 3
    default = 1
    display_name = "Starting Monkey Amount"


class XPCurve(Toggle):
    """
    The scaling of the XP requirements for Level Up checks.

    False/Static: A Configurable Amount of XP is Required to Level Up EACH time.
    True/Curved: Uses the default XP Curve from BTD6
    """

    display_name = "XP Curve Behaviour"


class StaticXPRequirement(Range):
    """
    Only relevant if "XP Curve Behaviour" is set to false.

    Min Req. 500 XP
    Max Req. 10,000 XP
    """

    display_name = "Static XP Requirement"
    range_start = 500
    range_end = 10000
    default = 5000


class MaxLevel(Range):
    """
    What do you want to be the maximum level of the randomizer?

    Levels start at 0, and you're required to go to at least 40
    """

    display_name = "Maximum Level"
    range_start = 0
    range_end = 150
    default = 40


class ProgressiveKnowledge(Toggle):
    """
    False/Off: Each individual Monkey Knowledge node is its own item in the multiworld pool.
               Receiving one unlocks that specific node in the Knowledge Tree (original behaviour).
    True/On:  All 134 individual knowledge items are replaced with 7 "Progressive Knowledge" items.
              Each one you receive unlocks the next full layer of the Knowledge Tree across all branches.
    """

    display_name = "Progressive Knowledge"


class PopTierChecks(Toggle):
    """
    False/Off: Monkey upgrade tiers are not locked behind pop counts.
    True/On:  Tier 3, 4, and 5 upgrades for each monkey are locked until that monkey
              has accumulated enough pops. Hitting each threshold sends a check.
              {Adds 72 checks}
    """

    display_name = "Pop Tier Checks"


class Tier3PopRequirement(Range):
    """
    Number of pops in a single game required with a monkey type to unlock its Tier 3 upgrades and send a check.
    Only relevant if Pop Tier Checks is enabled.
    """

    display_name = "Tier 3 Pop Requirement"
    range_start = 100
    range_end = 1000
    default = 200


class Tier4PopRequirement(Range):
    """
    Number of pops in a single game required with a monkey type to unlock its Tier 4 upgrades and send a check.
    Only relevant if Pop Tier Checks is enabled.
    """

    display_name = "Tier 4 Pop Requirement"
    range_start = 1000
    range_end = 10000
    default = 2000


class Tier5PopRequirement(Range):
    """
    Number of pops in a single game required with a monkey type to unlock its Tier 5 upgrades and send a check.
    Only relevant Pop Tier Checks is enabled.
    """

    display_name = "Tier 5 Pop Requirement"
    range_start = 5000
    range_end = 100000
    default = 10000


class RoundSanity(Range):
    """
    Adds location checks for completing rounds on any map.
    Set to 0 to disable. Otherwise, a check is sent every N rounds up to round 100.

    Examples:
    5 = checks at rounds 5, 10, 15, 20, ..., 100 (20 checks per map)
    20 = checks at rounds 20, 40, 60, 80, 100 (5 checks per map)
    60 = check at round 60 only (1 check per map)
    """

    display_name = "Round Sanity"
    range_start = 0
    range_end = 100
    default = 0


class ProgressivePrices(Toggle):
    """
    False/Off: Tower and upgrade costs behave normally based on the selected difficulty.
    True/On:  All tower and upgrade costs start at Impoppable pricing (1.20x).
              Receiving "Progressive Prices" items progressively decreases costs across all difficulties:
              Impoppable (1.20x) -> Hard (1.08x) -> Medium (1.00x) -> Easy (0.85x)
    """

    display_name = "Progressive Prices"


class CategoryLock(Toggle):
    """
    False/Off: Monkeys are unlocked individually as normal.
    True/On:  Monkeys are unlocked by category (Primary, Military, Magic, Support).
              You start with one random category and the other three are sent as items.
              When enabled, starting monkeys are always randomized (ignores Random Starting Monkeys option).
    """

    display_name = "Category Lock"


class Goal(Choice):
    """
    How you complete the randomizer. 
    Collecting enough of the "Medal" item will unlock a victory map (marked by the archipelago logo)

    Default: Beat the victory map on the highest available difficulty (Impoppable/Chimps)
    Boss: Defeat a random Boss Bloon event on the victory map.
    Elite Boss: Defeat a random Elite Boss Bloon event on the victory map. 
                Note: Boss Events are guaranteed to take place on Beginner or Intermediate maps.
    """

    display_name = "Goal"
    option_default = 0
    option_boss = 1
    option_elite_boss = 2
    default = 0


class TrapPercentage(Range):
    """
    Replace a percentage of filler items in the item pool with random traps.
    """

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeights(OptionDict):
    """
    Specify the weights determining how many copies of each trap item will be in your itempool.
    If you don't want a specific type of trap, you can set the weight for it to 0.
    If you set all trap weights to 0, you will get no traps, bypassing the "Trap Percentage" option.
    For information on what the traps do, check the wiki: https://archipelago.miraheze.org/wiki/Bloons_TD6
    """

    display_name = "Trap Weights"
    valid_keys = frozenset([
        "Modified Bloons", "Freeze Trap", "Bee Trap", "Speed Up Trap", "Literature Trap",
    ])
    default = {
        "Modified Bloons": 10,
        "Freeze Trap": 10,
        "Bee Trap": 10,
        "Speed Up Trap": 10,
        "Literature Trap": 10,
    }


_ALL_MAP_DISPLAY_NAMES = frozenset([
    "Monkey Meadow", "In The Loop", "Middle Of The Road", "Tinkerton", "Tree Stump",
    "Town Centre", "One Two Tree", "Scrapyard", "The Cabin", "Resort", "Skates",
    "Lotus Island", "Candy Falls", "Winter Park", "Carved", "Park Path", "Alpine Run",
    "Frozen Over", "Cubism", "Four Circles", "Hedge", "End Of The Road", "Logs",
    "Spa Pits", "Three Mines Around", "Luminous Cove", "Sulfur Springs", "Water Park",
    "Polyphemus", "Covered Garden", "Quarry", "Quiet Street", "Bloonarius Prime",
    "Balance", "Encrypted", "Bazaar", "Adora's Temple", "Spring Spring",
    "Karts N Darts", "Moon Landing", "Haunted", "Downstream", "Firing Range",
    "Cracked", "Streambed", "Chutes", "Rake", "Spice Islands", "Lost Crevasse",
    "Ancient Portal", "Castle Revenge", "Dark Path", "Erosion", "Midnight Mansion",
    "Sunken Columns", "X Factor", "Mesa", "Geared", "Spillway", "Cargo",
    "Pat's Pond", "Peninsula", "High Finance", "Another Brick", "Off The Coast",
    "Cornfield", "Underground", "Enchanted Glade", "Last Resort", "Party Parade",
    "Sunset Gulch", "Mushroom Grotto", "Glacial Trail", "Dark Dungeons", "Sanctuary",
    "Ravine", "Flooded Valley", "Infernal", "Bloody Puddles", "Workshop", "Quad",
    "Dark Castle", "Muddy Puddles", "#ouch", "Tricky Tracks",
])


class MapBlacklist(OptionSet):
    """
    Maps to never include in this randomizer, entered by display name.
    Example: ["Monkey Meadow", "#ouch", "Bloonarius Prime"]
    If a map appears in both the blacklist and whitelist, the blacklist wins.
    """

    display_name = "Map Blacklist"
    valid_keys = _ALL_MAP_DISPLAY_NAMES
    default = frozenset()


class MapWhitelist(OptionSet):
    """
    Maps that are guaranteed to be included in the pool (starting maps or unlockable maps),
    as long as they fall within the selected difficulty range and are not blacklisted.
    Other maps outside this list can still fill remaining slots. Entered by display name.
    Example: ["Monkey Meadow", "Bloonarius Prime", "Infernal"]
    """

    display_name = "Map Whitelist"
    valid_keys = _ALL_MAP_DISPLAY_NAMES
    default = frozenset()


@dataclass
class BloonsTD6Options(PerGameCommonOptions):
    goal: Goal
    total_medals: TotalMedals
    medalreq: MedalRequirementPercentage
    total_maps: TotalMaps
    starting_map_count: StartingMaps
    min_map_diff: MinMapDiff
    max_map_diff: MaxMapDiff
    map_blacklist: MapBlacklist
    map_whitelist: MapWhitelist
    rando_difficulty: Difficulty
    category_lock: CategoryLock
    starting_monkey: StartingMonkeys
    num_start_monkey: StartingMonkeyAmount
    xp_curve: XPCurve
    static_req: StaticXPRequirement
    max_level: MaxLevel
    progressive_knowledge: ProgressiveKnowledge
    progressive_prices: ProgressivePrices
    pop_tier_checks: PopTierChecks
    tier3_pop_requirement: Tier3PopRequirement
    tier4_pop_requirement: Tier4PopRequirement
    tier5_pop_requirement: Tier5PopRequirement
    round_sanity: RoundSanity
    death_link: DeathLink
    trap_percentage: TrapPercentage
    trap_weights: TrapWeights


btd6_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        TotalMedals,
        MedalRequirementPercentage,
    ]),
    OptionGroup("Map Options", [
        Difficulty,
        TotalMaps,
        StartingMaps,
        MinMapDiff,
        MaxMapDiff,
        MapBlacklist,
        MapWhitelist,
    ]),
    OptionGroup("Monkey Options", [
        CategoryLock,
        StartingMonkeys,
        StartingMonkeyAmount,
    ]),
    OptionGroup("Progression Options", [
        ProgressiveKnowledge,
        ProgressivePrices,
        MaxLevel,
        StaticXPRequirement,
        XPCurve,
    ]),
    OptionGroup("Extra Locations", [
        PopTierChecks,
        Tier3PopRequirement,
        Tier4PopRequirement,
        Tier5PopRequirement,
        RoundSanity,
    ]),
    OptionGroup("Trap Options", [
        TrapPercentage,
        TrapWeights,
    ]),
]
