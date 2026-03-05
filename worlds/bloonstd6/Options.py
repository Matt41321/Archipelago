from Options import Choice, Toggle, Range, PerGameCommonOptions
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

    range_start = 15
    range_end = 60
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

    Basic: The Easy, Medium, Hard, and Impoppable Medals are all checks.
    Advanced: The Easy, Medium, Hard, Impoppable, and Chimps Medals are all checks.
    Expert: All Medals are checks.
    """

    display_name = "Difficulty"
    option_Basic = 4
    option_Advanced = 5
    option_Expert = 14
    default = 4


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
    Would you like to randomize all starting monkeys or include the Dart Monkey in the starting monkeys.

    True/On: All Starting Monkeys will be random.
    False/Off: The first starting monkey no matter how many you include will always be the vanilla Dart Monkey.
    """

    display_name = "Random Starting Monkeys"


class StartingMonkeyAmount(Range):
    """
    How many starting Monkeys would you like?
    """

    range_start = 1
    range_end = 3
    default = 1
    display_name = "Starting Monkey Amount"


class XPCurve(Toggle):
    """
    False: Static
    True: Curved

    Static: A Configurable Amount of XP is Required to Level Up EACH time.
    Curved: Uses the default XP Curve from BTD6
    """

    display_name = "XP Curve"


class StaticXPRequirement(Range):
    """
    Min Req. 500 XP
    Max Req. 10,000 XP
    """

    display_name = "Static XP Requirement"
    range_start = 500
    range_end = 10000
    default = 5000


class MaxLevel(Range):
    """
    What do you want to be the maximum level of the randomizer.

    Levels start at 0, and you're required to go to at least 40
    """

    display_name = "Maximum Level"
    range_start = 40
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
    """

    display_name = "Pop Tier Checks"


class Tier3PopRequirement(Range):
    """
    Number of pops required with a monkey to unlock its Tier 3 upgrades and send a check.
    Only used when Pop Tier Checks is enabled.
    """

    display_name = "Tier 3 Pop Requirement"
    range_start = 100
    range_end = 1000
    default = 200


class Tier4PopRequirement(Range):
    """
    Number of pops required with a monkey to unlock its Tier 4 upgrades and send a check.
    Only used when Pop Tier Checks is enabled.
    """

    display_name = "Tier 4 Pop Requirement"
    range_start = 1000
    range_end = 10000
    default = 2000


class Tier5PopRequirement(Range):
    """
    Number of pops required with a monkey to unlock its Tier 5 upgrades and send a check.
    Only used when Pop Tier Checks is enabled.
    """

    display_name = "Tier 5 Pop Requirement"
    range_start = 5000
    range_end = 100000
    default = 10000


@dataclass
class BloonsTD6Options(PerGameCommonOptions):
    starting_map_count: StartingMaps
    total_maps: TotalMaps
    min_map_diff: MinMapDiff
    max_map_diff: MaxMapDiff
    rando_difficulty: Difficulty
    medalreq: MedalRequirementPercentage
    starting_monkey: StartingMonkeys
    num_start_monkey: StartingMonkeyAmount
    xp_curve: XPCurve
    static_req: StaticXPRequirement
    max_level: MaxLevel
    progressive_knowledge: ProgressiveKnowledge
    pop_tier_checks: PopTierChecks
    tier3_pop_requirement: Tier3PopRequirement
    tier4_pop_requirement: Tier4PopRequirement
    tier5_pop_requirement: Tier5PopRequirement
