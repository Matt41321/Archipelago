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

    Default: Beat the victory map on the highest available difficulty (Impoppalbe/Chimps)
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


class ModifiedBloonsWeight(Range):
    """
    How heavily weighted the trap pool is towards "Modified Bloons" traps.
    Modified Bloons causes most bloons to gain a random property (Camo, Regrow, Fortified) for next three rounds.
    """

    display_name = "Modified Bloons Weight"
    range_start = 0
    range_end = 100
    default = 10


class FreezeWeight(Range):
    """
    How heavily weighted the trap pool is towards "Freeze Trap" traps.
    Freeze Trap causes all towers to stop attacking for 10 seconds.
    """

    display_name = "Freeze Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class BeeWeight(Range):
    """
    How heavily weighted the trap pool is towards "Bee Trap" traps.
    Bee Trap sends swarms of bees flying across the screen.
    """

    display_name = "Bee Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class SpeedUpWeight(Range):
    """
    How heavily weighted the trap pool is towards "Speed Up Trap" traps.
    Speed Up Trap causes all bloons to speed up for the next two rounds.
    """

    display_name = "Speed Up Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class LiteratureWeight(Range):
    """
    How heavily weighted the trap pool is towards "Literature Trap" traps.
    Literature Trap makes you smart.
    """

    display_name = "Literature Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


@dataclass
class BloonsTD6Options(PerGameCommonOptions):
    goal: Goal
    total_medals: TotalMedals
    medalreq: MedalRequirementPercentage
    total_maps: TotalMaps
    starting_map_count: StartingMaps
    min_map_diff: MinMapDiff
    max_map_diff: MaxMapDiff
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
    trap_percentage: TrapPercentage
    modified_bloons_weight: ModifiedBloonsWeight
    freeze_weight: FreezeWeight
    bee_weight: BeeWeight
    speed_up_weight: SpeedUpWeight
    literature_weight: LiteratureWeight
