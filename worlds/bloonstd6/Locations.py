from typing import Dict, List, NamedTuple, Optional
from BaseClasses import Location, Region
from .Utils import Shared


class MapData(NamedTuple):
    code: Optional[int]


class BTD6Medal(Location):
    game: str = "Bloons TD6"

    def __init__(
        self,
        player: int,
        name: str = "",
        code: int | None = None,
        parent: Region | None = None,
    ):
        super().__init__(player, name, code, parent)


class BTD6Map(Location):
    game: str = "Bloons TD6"


class BTD6Hero(Location):
    game: str = "Bloons TD6"


class BTD6Knowledge(Location):
    game: str = "Bloons TD6"


class BTD6Level(Location):
    game: str = "Bloons TD6"


class BloonsLocations:
    locations: Dict[str, int] = {}

    map_names_by_difficulty: Dict[str, List[str]] = {
        "beginner": [
            "MonkeyMeadow",
            "InTheLoop",
            "MiddleOfTheRoad",
            "Tinkerton",
            "TreeStump",
            "TownCentre",
            "OneTwoTree",
            "Scrapyard",
            "TheCabin",
            "Resort",
            "Skates",
            "LotusIsland",
            "CandyFalls",
            "WinterPark",
            "Carved",
            "ParkPath",
            "AlpineRun",
            "FrozenOver",
            "Cubism",
            "FourCircles",
            "Hedge",
            "EndOfTheRoad",
            "Logs",
            "SpaPits",
            "ThreeMinesAround",
        ],
        "intermediate": [
            "LuminousCove",
            "SulfurSprings",
            "WaterPark",
            "Polyphemus",
            "CoveredGarden",
            "Quarry",
            "QuietStreet",
            "BloonariusPrime",
            "Balance",
            "Encrypted",
            "Bazaar",
            "AdorasTemple",
            "SpringSpring",
            "KartsNDarts",
            "MoonLanding",
            "Haunted",
            "Downstream",
            "FiringRange",
            "Cracked",
            "Streambed",
            "Chutes",
            "Rake",
            "SpiceIslands",
            "LostCrevasse",
            "AncientPortal",
        ],
        "advanced": [
            "CastleRevenge",
            "DarkPath",
            "Erosion",
            "MidnightMansion",
            "SunkenColumns",
            "XFactor",
            "Mesa",
            "Geared",
            "Spillway",
            "Cargo",
            "PatsPond",
            "Peninsula",
            "HighFinance",
            "AnotherBrick",
            "OffTheCoast",
            "Cornfield",
            "Underground",
            "EnchantedGlade",
            "LastResort",
            "PartyParade",
            "SunsetGulch",
            "MushroomGrotto",           
        ],
        "expert": [
            "GlacialTrail",
            "DarkDungeons",
            "Sanctuary",
            "Ravine",
            "FloodedValley",
            "Infernal",
            "BloodyPuddles",
            "Workshop",
            "Quad",
            "DarkCastle",
            "MuddyPuddles",
            "#ouch",
            "TrickyTracks",
        ],
    }

    auto_location_groups: Dict[str, set] = {}

    def __init__(self) -> None:
        index = 1

        for _, list in self.map_names_by_difficulty.items():
            for name in list:
                self.locations[f"{name}-Easy"] = index
                self.locations[f"{name}-PrimaryOnly"] = index + 1
                self.locations[f"{name}-Deflation"] = index + 2
                self.locations[f"{name}-Medium"] = index + 3
                self.locations[f"{name}-MilitaryOnly"] = index + 4
                self.locations[f"{name}-Apopalypse"] = index + 5
                self.locations[f"{name}-Reverse"] = index + 6
                self.locations[f"{name}-Hard"] = index + 7
                self.locations[f"{name}-MagicOnly"] = index + 8
                self.locations[f"{name}-DoubleMoabHealth"] = index + 9
                self.locations[f"{name}-HalfCash"] = index + 10
                self.locations[f"{name}-AlternateBloonsRounds"] = index + 11
                self.locations[f"{name}-Impoppable"] = index + 12
                self.locations[f"{name}-Chimps"] = index + 13
                self.locations[f"{name}-Unlock"] = index + 14
                index += 15

        for i in range(149):
            self.locations[f"Level {i+2}"] = index
            index += 1

        for hero in Shared.heroIDs:
            self.locations[hero] = index
            index += 1

        for name in Shared.knowledgeIDs:
            self.locations[f"{name}-Tree"] = index
            index += 1

        for name in Shared.monkeyIDs:
            if name == "MonkeyVillage":
                continue
            self.locations[f"{name}-Tier3"] = index
            self.locations[f"{name}-Tier4"] = index + 1
            self.locations[f"{name}-Tier5"] = index + 2
            index += 3

        all_maps = [m for maps in self.map_names_by_difficulty.values() for m in maps]
        for map_name in all_maps:
            for i in range(1, 101):
                self.locations[f"{map_name}-Round {i}"] = index
                index += 1

        self.auto_location_groups["knowledge"] = set(
            name for name in self.locations.keys() if name.endswith("-Tree")
        )
        self.auto_location_groups["poptiers"] = set(
            name for name in self.locations.keys() if name.endswith(("-Tier3", "-Tier4", "-Tier5"))
        )
        self.auto_location_groups["level"] = set(
            name for name in self.locations.keys() if name.startswith("Level ")
        )
        self.auto_location_groups["rounds"] = set(
            name for name in self.locations.keys() if "-Round " in name
        )

    def get_maps(self, minDiff=0, maxDiff=3) -> List[str]:
        """List all Map IDs within the difficulties that can be played."""
        filtered_list: List[str] = []

        index = 0

        for diff, list in self.map_names_by_difficulty.items():
            if index <= maxDiff and index >= minDiff:
                filtered_list += list
            index += 1

        return filtered_list
