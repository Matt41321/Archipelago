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

    display_name_to_id: Dict[str, str] = {
        "Monkey Meadow": "MonkeyMeadow",
        "In The Loop": "InTheLoop",
        "Middle Of The Road": "MiddleOfTheRoad",
        "Tinkerton": "Tinkerton",
        "Tree Stump": "TreeStump",
        "Town Centre": "TownCentre",
        "One Two Tree": "OneTwoTree",
        "Scrapyard": "Scrapyard",
        "The Cabin": "TheCabin",
        "Resort": "Resort",
        "Skates": "Skates",
        "Lotus Island": "LotusIsland",
        "Candy Falls": "CandyFalls",
        "Winter Park": "WinterPark",
        "Carved": "Carved",
        "Park Path": "ParkPath",
        "Alpine Run": "AlpineRun",
        "Frozen Over": "FrozenOver",
        "Cubism": "Cubism",
        "Four Circles": "FourCircles",
        "Hedge": "Hedge",
        "End Of The Road": "EndOfTheRoad",
        "Logs": "Logs",
        "Spa Pits": "SpaPits",
        "Three Mines Around": "ThreeMinesAround",
        "Luminous Cove": "LuminousCove",
        "Sulfur Springs": "SulfurSprings",
        "Water Park": "WaterPark",
        "Polyphemus": "Polyphemus",
        "Covered Garden": "CoveredGarden",
        "Quarry": "Quarry",
        "Quiet Street": "QuietStreet",
        "Bloonarius Prime": "BloonariusPrime",
        "Balance": "Balance",
        "Encrypted": "Encrypted",
        "Bazaar": "Bazaar",
        "Adora's Temple": "AdorasTemple",
        "Spring Spring": "SpringSpring",
        "Karts N Darts": "KartsNDarts",
        "Moon Landing": "MoonLanding",
        "Haunted": "Haunted",
        "Downstream": "Downstream",
        "Firing Range": "FiringRange",
        "Cracked": "Cracked",
        "Streambed": "Streambed",
        "Chutes": "Chutes",
        "Rake": "Rake",
        "Spice Islands": "SpiceIslands",
        "Lost Crevasse": "LostCrevasse",
        "Ancient Portal": "AncientPortal",
        "Castle Revenge": "CastleRevenge",
        "Dark Path": "DarkPath",
        "Erosion": "Erosion",
        "Midnight Mansion": "MidnightMansion",
        "Sunken Columns": "SunkenColumns",
        "X Factor": "XFactor",
        "Mesa": "Mesa",
        "Geared": "Geared",
        "Spillway": "Spillway",
        "Cargo": "Cargo",
        "Pat's Pond": "PatsPond",
        "Peninsula": "Peninsula",
        "High Finance": "HighFinance",
        "Another Brick": "AnotherBrick",
        "Off The Coast": "OffTheCoast",
        "Cornfield": "Cornfield",
        "Underground": "Underground",
        "Enchanted Glade": "EnchantedGlade",
        "Last Resort": "LastResort",
        "Party Parade": "PartyParade",
        "Sunset Gulch": "SunsetGulch",
        "Mushroom Grotto": "MushroomGrotto",
        "Glacial Trail": "GlacialTrail",
        "Dark Dungeons": "DarkDungeons",
        "Sanctuary": "Sanctuary",
        "Ravine": "Ravine",
        "Flooded Valley": "FloodedValley",
        "Infernal": "Infernal",
        "Bloody Puddles": "BloodyPuddles",
        "Workshop": "Workshop",
        "Quad": "Quad",
        "Dark Castle": "DarkCastle",
        "Muddy Puddles": "MuddyPuddles",
        "#ouch": "#ouch",
        "Tricky Tracks": "TrickyTracks",
    }

    id_to_display_name: Dict[str, str] = {v: k for k, v in display_name_to_id.items()}

    _normalized_lookup: Dict[str, str] = {
        k.lower().replace(" ", "").replace("'", ""): v
        for k, v in display_name_to_id.items()
    }

    @classmethod
    def resolve_map_name(cls, name: str) -> str | None:
        """Convert a user-supplied map name to an internal ID. Returns None if not found."""
        if name in cls.display_name_to_id:
            return cls.display_name_to_id[name]
        normalized = name.lower().replace(" ", "").replace("'", "")
        return cls._normalized_lookup.get(normalized)

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
