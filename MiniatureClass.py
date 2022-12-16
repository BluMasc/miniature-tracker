class Miniature:
    def __init__(self, dict, id):
        self.id = id
        self.name = dict["name"]
        self.painters = dict["PhysicalOptions"]["Painters"]
        self.status = dict["PhysicalOptions"]["Status"]
        self.material = dict["PhysicalOptions"]["Material"]
        self.kitSources = dict["PhysicalOptions"]["Kitbash Sources"]
        self.source = dict["source"]
        self.comment = dict["comment"]
        self.enviroments = dict["tags"]["enviromentTags"]
        self.planes = dict["tags"]["planeTags"]
        self.sizes = dict["tags"]["SizeTags"]
        self.types = dict["tags"]["CreatureTypeTags"]
        self.classes = dict["tags"]["CreatureClassTag"]
        self.movements = dict["tags"]["CreatureMovementTag"]
        self.attacks = dict["tags"]["CreatureAttackTags"]
        self.tags = dict["tags"]["AdditionalTag"]
        self.location = dict["storageLocation"]
        self.statblocks = dict["statblocks"]
        self.link = dict["link"]
        self.price = dict["price"]
    def __str__(self):
        return f"({self.id}){self.name}"
    def __lt__(self, other):
         return self.name < other.name
