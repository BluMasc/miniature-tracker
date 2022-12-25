import os
import json
from pathlib import Path
import re

p = Path(__file__).with_name('config.json')

with p.open('r') as f:
  cfg = json.load(f)

with open(cfg["File Location"], 'r') as f:
  goaldata = json.load(f)

with open("C:/Users/Chrom/Documents/GitHub/miniature-tracker/models.json", 'r') as f:
  sourcedata = json.load(f)

regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

i = 0
unconvertedTags=[]
for mini in sourcedata:
    out = {"name":mini["name"],"PhysicalOptions":{"Painters":[],"Status":1,"Material":[],"Kitbash Sources":[] },"source":mini["source"],"comment":mini["comment"],"tags":{"enviromentTags":[],"planeTags":[],"SizeTags":[],"CreatureTypeTags":[],"CreatureClassTag":[],"CreatureMovementTag":[],"CreatureAttackTags":[],"SpeciesTag":[],"AdditionalTag":[]},"storageLocation":"?","statblocks":mini["statblocks"],"link":"?","price":-1}
    for n, name in enumerate(goaldata["PhysicalOptions"]["Painters"]):
        if name.lower() in mini["painted"].lower():
            out["PhysicalOptions"]["Painters"].append(n)
    # for n, name in enumerate(goaldata["PhysicalOptions"]["Material"]):
    #     if name.lower() in mini["source"].lower():
    #         print(name)
    #         out["PhysicalOptions"]["Material"].append(n)
    url = re.findall(regex, mini["source"])
    if url:
        out["link"] = url[0][0]
    for n, name in enumerate(goaldata["possibleTags"]["enviromentTags"]):
        if name.lower() in mini["tags"]:
            out["tags"]["enviromentTags"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["planeTags"]):
        if name.lower() in mini["tags"]:
            out["tags"]["planeTags"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["SizeTags"]):
        if name.lower() in mini["tags"]:
            out["tags"]["SizeTags"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["CreatureTypeTags"]):
        if name.lower() in mini["tags"]:
            out["tags"]["CreatureTypeTags"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["CreatureClassTag"]):
        if name.lower() in mini["tags"]:
            out["tags"]["CreatureClassTag"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["CreatureMovementTag"]):
        if name.lower() in mini["tags"]:
            out["tags"]["CreatureMovementTag"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["CreatureAttackTags"]):
        if name.lower() in mini["tags"]:
            out["tags"]["CreatureAttackTags"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["SpeciesTag"]):
        if name.lower() in mini["tags"]:
            out["tags"]["SpeciesTag"].append(n)
    for n, name in enumerate(goaldata["possibleTags"]["AdditionalTag"]):
        if name.lower() in mini["tags"]:
            out["tags"]["AdditionalTag"].append(n)
    weaponTags=["axe","ballandchain","bow","dagger","lance","net",'scythe',"spear","sword"]
    for name in weaponTags:
        if name.lower() in mini["tags"]:
            out["tags"]["CreatureAttackTags"].append(0)
    if "boss" in mini["tags"]:
        out["tags"]["AdditionalTag"].append(6)
    if "caster" in mini["tags"]:
        out["tags"]["CreatureAttackTags"].append(2)
    if "magic" in mini["tags"]:
        out["tags"]["CreatureAttackTags"].append(2)
    if "spell" in mini["tags"]:
        out["tags"]["CreatureAttackTags"].append(2)
    if "character" in mini["tags"]:
        out["tags"]["AdditionalTag"].append(1)
    if "cold" in mini["tags"]:
        out["tags"]["enviromentTags"].append(2)
    if "dream" in mini["tags"]:
        out["tags"]["planeTags"].append(11)
    out["old"]=mini
    while str(i) in goaldata["Minis"]:
        i+=1
    goaldata["Minis"][str(i)]=out

with open("C:/Users/Chrom/Documents/GitHub/miniature-tracker/modelsTest.json", "w") as outfile:
    json.dump(goaldata, outfile, indent=4)
