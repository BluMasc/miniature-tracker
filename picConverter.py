old =  "D:/MiniCollection/MiniatureTracking/Pictures"
new = "C:/Users/bluma/Documents/projects/miniature-tracker/pics"
names = "C:/Users/bluma/Documents/projects/miniature-tracker/modelsTest.json"

from PIL import Image,ImageTk
import json
import os

with open(names, 'r') as f:
  data = json.load(f)
ids = {}
for k,v in data["Minis"].items():
    if "old" in v:
        ids[v["old"]["imgName"]]=k

for filename in os.listdir(old):
    f = os.path.join(old, filename)
    if os.path.isfile(f):
        if filename in ids:
            im = Image.open(f)
            im.thumbnail((800,600))
            im.save(f"{new}/{ids[filename]}.png")
