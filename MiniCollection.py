# hello_psg.py

import PySimpleGUI as sg
import os
import json
from pathlib import Path
from MiniatureClass import Miniature
import re

p = Path(__file__).with_name('config.json')

with p.open('r') as f:
  cfg = json.load(f)

if "PySimpleGUITheme" in cfg:
    sg.theme(cfg["PySimpleGUITheme"])

with open(cfg["File Location"], 'r') as f:
  data = json.load(f)

originalValues = sorted([Miniature(n,m)  for m,n in data["Minis"].items()])
filteredValues = originalValues.copy()

enviromentTags = data["possibleTags"]["enviromentTags"]
planeTags = data["possibleTags"]["planeTags"]
sizeTags = data["possibleTags"]["SizeTags"]
creatureTypeTags = data["possibleTags"]["CreatureTypeTags"]
creatureClassTag = data["possibleTags"]["CreatureClassTag"]
creatureMovementTag = data["possibleTags"]["CreatureMovementTag"]
creatureAttackTags = data["possibleTags"]["CreatureAttackTags"]
additionalTags = data["possibleTags"]["AdditionalTag"]
painters = data["PhysicalOptions"]["Painters"]
statuses = data["PhysicalOptions"]["Status"]
materials = data["PhysicalOptions"]["Material"]

chooseColumn = [  [sg.Text('Models')],
            [sg.Input(key='-IN-', enable_events=True), sg.Button('Search', bind_return_key=True), sg.Button('Help')],
            [sg.Listbox(
                values=filteredValues,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                enable_events=True,
                size=(60, 20),
                key="--list--")],

            ]
editAddon = [
            [sg.Button('Edit') ,sg.Button('Add'),sg.Button('Delete')]
            ]

if cfg["Edit Mode"]:
    chooseColumn = chooseColumn+editAddon

infoColumn = [
    [sg.Text('Model', key='-text-',font=("",20),size=(30, 1))],
    [sg.Image(key="-IMAGE-",size=(400, 300))],
    [sg.Column([[sg.Text('Source',font="bold"),sg.Text('-', key='-source-',size=(20, 1))],
        [sg.Text('Link',font="bold"),sg.Text('-', key='-link-',size=(20, 1))],
        [sg.Text('Price',font="bold"),sg.Text('-', key='-price-',size=(20, 1))],
        [sg.Text('Painted By',font="bold"),sg.Text('-', key='-painted-',size=(20, 1))],
        [sg.Text('Status',font="bold"),sg.Text('-', key='-status-',size=(20, 1))],
        [sg.Text('Material',font="bold"),sg.Text('-', key='-material-',size=(20, 1))],
        [sg.Text('Location',font="bold"),sg.Text('-', key='-location-',size=(20, 1))]]),
    sg.Column([[sg.Text('Enviroment',font="bold"),sg.Text('-', key='-enviroment-',size=(20, 1))],
        [sg.Text('Plane',font="bold"),sg.Text('-', key='-plane-',size=(20, 1))],
        [sg.Text('Size',font="bold"),sg.Text('-', key='-size-',size=(20, 1))],
        [sg.Text('Type',font="bold"),sg.Text('-', key='-type-',size=(20, 1))],
        [sg.Text('Class',font="bold"),sg.Text('-', key='-class-',size=(20, 1))],
        [sg.Text('Attacks',font="bold"),sg.Text('-', key='-atk-',size=(20, 1))],
        [sg.Text('Tags',font="bold"),sg.Text('-', key='-tag-',size=(20, 1))]])],


]

layout = [
    [
        sg.Column(chooseColumn),
        sg.VSeperator(),
        sg.Column(infoColumn, element_justification='c'),
    ]
]

searchIndicators =[["",'name'],["sc","source"],["li","link"],["pr","price"],["lo","location"],["pt","painters"],["st","status"],["mt","material"]]
inHeaders = ["Indicator","Atribute"]
searchComperators=[[":","contains"],["=","is equal to"],["~","is equal to regex"],["#","does not contain"]]
coHeaders = ["Comperators", "Function"]

# Create the window
window = sg.Window("Mini Tracker", layout)
def open_help_window():
    helplayout = [
        [
            sg.Text('Help',font=("",20))
        ],
        [
            sg.Text('If you want to search by name you can just enter the text that the name should contain')
        ],
        [
            sg.Text('(not using ";" or any comparison symbol).')
        ],
        [
            sg.Text('You can specify search parameters by writing an indicator followed by a symbol for comparison.')
        ],
        [
            sg.Text('Each parameter is seperated by a ";". ')
        ],
        [sg.Column(
        [[
            sg.Text('Indicators',font=("",15))
        ],
        [
            sg.Table(values=searchIndicators, headings=inHeaders,size=(80, 10))
        ]]),
        sg.VSeperator(),
        sg.Column(
        [[
            sg.Text('Comperators',font=("",15))
        ],
        [
            sg.Table(values=searchComperators, headings=coHeaders)
        ]])
        ]
    ]
    helpwindow = sg.Window("Mini Tracker Help", helplayout, modal=True)
    choice = None
    while True:
        event, values = helpwindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    helpwindow.close()

def function_in(x,y):
    return (x in y)
def function_eq(x,y):
    return (x == y)
def function_rx(x,y):
    pattern = re.compile(x)
    return (pattern.match(y))
def function_ni(x,y):
    return not(x in y)

def search(termString):
    preFilteredValues = originalValues.copy()
    #print(filteredValues)
    terms = termString.split(";")
    for term in terms:
        #any([n in term for n in [":","=","~","#"]]):""
        function=function_in
        if ":" in term:
            function=function_in
            indTxt = term.split(":")
        elif "=" in term:
            function=function_eq
            indTxt = term.split("=")
        elif "~" in term:
            function=function_rx
            indTxt = term.split("~")
        elif "#" in term:
            function=function_ni
            indTxt = term.split("#")
        if indTxt:
            if indTxt[0]=="":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.name), preFilteredValues))
            elif indTxt[0]=="sc":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.source), preFilteredValues))
            elif indTxt[0]=="li":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.link), preFilteredValues))
            elif indTxt[0]=="pr":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.price), preFilteredValues))
        else:
            preFilteredValues = list(filter(lambda mini: function(term,mini.name), preFilteredValues))
    global filteredValues
    filteredValues = preFilteredValues.copy()
    window.Element("--list--").Update(filteredValues)

def update_values(miniature):
    window.Element('-text-').Update(miniature)
    window.Element('-IMAGE-').Update(cfg["Images Location"]+"/"+miniature.id+".png")
    window.Element('-source-').Update(miniature.source)
    window.Element('-link-').Update(miniature.link)
    if miniature.price == -1:
        window.Element('-price-').Update("?")
    else:
        window.Element('-price-').Update("{:.2f}€".format(miniature.price))
    pntrs = ""
    for painter in miniature.painters:
        pntrs = pntrs+painters[painter]+", "
    window.Element('-painted-').Update(pntrs[:-2])
    window.Element('-status-').Update(statuses[miniature.status])
    mtrl=""
    for material in miniature.material:
        mtrl = mtrl+materials[material]+", "
    window.Element('-material-').Update(mtrl[:-2])
    window.Element('-location-').Update(miniature.location)
    envr=""
    for enviroment in miniature.enviroments:
        envr = envr+enviromentTags[enviroment]+", "
    window.Element('-enviroment-').Update(envr[:-2])
    plns=""
    for plane in miniature.planes:
        plns = plns+planeTags[plane]+", "
    window.Element('-plane-').Update(plns[:-2])
    sz = ""
    for size in miniature.sizes:
        sz = sz+sizeTags[size]+", "
    window.Element('-size-').Update(sz[:-2])
    tp = ""
    for type in miniature.types:
        tp = tp+creatureTypeTags[type]+", "
    window.Element('-type-').Update(tp[:-2])
    cls=""
    for clas in miniature.classes:
        cls = cls+creatureClassTag[clas]+", "
    window.Element('-class-').Update(cls[:-2])
    atk=""
    for attack in miniature.attacks:
        atk = atk+creatureAttackTags[attack]+", "
    window.Element('-atk-').Update(atk[:-2])
    tgs=""
    for tag in miniature.tags:
        tgs = tgs+additionalTags[tag]+", "
    window.Element('-tag-').Update(tgs[:-2])

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "Help":
        open_help_window()
    elif event == "Search":
        search(values["-IN-"])
    elif event == "--list--":
        ids = window[event].GetIndexes()
        obj = filteredValues[ids[0]]
        update_values(obj)
    window.refresh()
window.close()
