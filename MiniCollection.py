# hello_psg.py

import PySimpleGUI as sg
import os
import json
from pathlib import Path
from MiniatureClass import Miniature
import re
from PIL import Image,ImageTk
import webbrowser

linkregex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

p = Path(__file__).with_name('config.json')

with p.open('r') as f:
  cfg = json.load(f)

if "PySimpleGUITheme" in cfg:
    sg.theme(cfg["PySimpleGUITheme"])

with open(cfg["File Location"], 'r') as f:
  data = json.load(f)

dictValues = data["Minis"]
originalValues = sorted([Miniature(n,m)  for m,n in data["Minis"].items()])
filteredValues = originalValues.copy()

enviromentTags = data["possibleTags"]["enviromentTags"]
planeTags = data["possibleTags"]["planeTags"]
sizeTags = data["possibleTags"]["SizeTags"]
creatureTypeTags = data["possibleTags"]["CreatureTypeTags"]
creatureSpeciesTags = data["possibleTags"]["SpeciesTag"]
creatureClassTag = data["possibleTags"]["CreatureClassTag"]
creatureMovementTag = data["possibleTags"]["CreatureMovementTag"]
creatureAttackTags = data["possibleTags"]["CreatureAttackTags"]
additionalTags = data["possibleTags"]["AdditionalTag"]
painters = data["PhysicalOptions"]["Painters"]
statuses = data["PhysicalOptions"]["Status"]
materials = data["PhysicalOptions"]["Material"]
scanSources = data["Sources"]

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
    [sg.Column([[sg.Text('Source',font="bold"),sg.Text('-', key='-source-',size=(20, None))],
        [sg.Text('Link',font="bold"),sg.Text('-', key='-link-',enable_events=True,size=(20, None))],
        [sg.Text('Price',font="bold"),sg.Text('-', key='-price-',size=(20, None))],
        [sg.Text('Painted By',font="bold"),sg.Text('-', key='-painted-',size=(20, None))],
        [sg.Text('Status',font="bold"),sg.Text('-', key='-status-',size=(20, None))],
        [sg.Text('Material',font="bold"),sg.Text('-', key='-material-',size=(20, None))],
        [sg.Text('Location',font="bold"),sg.Text('-', key='-location-',size=(20, None))]]),
    sg.Column([[sg.Text('Enviroment',font="bold"),sg.Text('-', key='-enviroment-',size=(20, None))],
        [sg.Text('Plane',font="bold"),sg.Text('-', key='-plane-',size=(20, None))],
        [sg.Text('Size',font="bold"),sg.Text('-', key='-size-',size=(20, None))],
        [sg.Text('Type',font="bold"),sg.Text('-', key='-type-',size=(20, None))],
        [sg.Text('Subtypes',font="bold"),sg.Text('-', key='-species-',size=(20, None))],
        [sg.Text('Class',font="bold"),sg.Text('-', key='-class-',size=(20, None))],
        [sg.Text('Movements',font="bold"),sg.Text('-', key='-mov-',size=(20, None))],
        [sg.Text('Attacks',font="bold"),sg.Text('-', key='-atk-',size=(20, None))],
        [sg.Text('Tags',font="bold"),sg.Text('-', key='-tag-',size=(20, None))]])],


]

layout = [
    [
        sg.Column(chooseColumn),
        sg.VSeperator(),
        sg.Column(infoColumn, element_justification='c'),
    ]
]

searchIndicators =[["nm",'Name'],["sc","Source"],["li","Link"],["pr","Price"],["lo","Location"],["pt","Painters"],["st","Status"],["mt","Material"],["cm","Comment"],["ev","Enviroment"],["pl","Planes"],["sz","Sizes"],["tp","Types"],["cl","Classes"],["mv","Movements"],["at","Attacks"],["tg","Tags"],["sp","Species"]]
inHeaders = ["Indicator","Atribute"]
searchComperators=[[":","contains"],["=","is equal to"],["~","is equal to regex"],["#","does not contain"]]
coHeaders = ["Comperators", "Function"]

# Create the window
window = sg.Window("Mini Tracker", layout)

def open_edit_window(initialMini, id):
    mini = initialMini.copy()
    price = str(mini["price"])
    if price == "-1":
        price = ""
    link = f'{cfg["Images Location"]}/{id}.png'
    linkExists = "\u274C"
    if os.path.exists(link):
        linkExists = "\u2714"
    editorLayout=[
        [[sg.Text(f'Edit/Add Model ({id})',font=("",20))],
        [sg.Text('Name:',font="bold"),sg.Input(default_text=mini["name"], key='-NAME-', size=(30, None), enable_events=True),sg.Text('Source:',font="bold"),sg.Input(default_text=mini["source"], key='-SOURCE-', size=(30, None), enable_events=True)],
        [sg.Text('Link:',font="bold"),sg.Input(default_text=mini["link"], key='-LINK-', size=(30, None), enable_events=True),
        sg.Text('Price (€):',font="bold"),sg.Input(default_text=price, key='-PRICE-', size=(30, None), enable_events=True)],
        [sg.Text('Location:',font="bold"),sg.Input(default_text=mini["storageLocation"], key='-LOCATION-', size=(30, None), enable_events=True),sg.Text('Comment:',font="bold"),sg.Input(default_text=mini["comment"], key='-COMMENT-', size=(30, None), enable_events=True)],[
        [sg.Column([
            [sg.Text('Painters',font="bold")],[sg.Listbox(values=painters,default_values=([painters[painter] for painter in mini["PhysicalOptions"]["Painters"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 5),
                key="--painters--")],
                    [sg.Input(key='-PAINT-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddPainter', size=(5, None))]
            ]),
            sg.Column([
                [sg.Text('Status',font="bold")],[sg.Listbox(values=statuses,default_values=([statuses[mini["PhysicalOptions"]["Status"]]
                    ]),
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    enable_events=True,
                    size=(15, 5),
                    key="--status--")],
                        [sg.Input(key='-STATUS-', size=(10, None), enable_events=True),
                         sg.Button("Add", key='AddStatus', size=(5, None))]
                ]),
                sg.Column([
                    [sg.Text('Material',font="bold")],[sg.Listbox(values=materials,default_values=([materials[painter] for painter in mini["PhysicalOptions"]["Material"]
                        ]),
                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        enable_events=True,
                        size=(15, 5),
                        key="--material--")],
                            [sg.Input(key='-MATERIAL-', size=(10, None), enable_events=True),
                             sg.Button("Add", key='AddMaterial', size=(5, None))]
                    ]),
                    sg.Column([
                        [sg.Text('Kitbash Sources',font="bold")],[sg.Multiline(default_text="\n".join(mini["PhysicalOptions"]["Kitbash Sources"]),
                            enable_events=True,
                            size=(15, 7),
                            key="--kitSources--")]
                        ]),
                        sg.Column([
                        [sg.Text(link,font="bold",key="--imagepos--"),sg.Text(linkExists,key="--imageexists--")],[sg.FileBrowse("Change Image", key='ChangeImage',enable_events=True,file_types=(("Image Files", "*.png"),("Image Files", "*.jpg"),("Image Files", "*.bmp"),("Image Files", "*.jpeg"),("Image Files", "*.gif"),("Image Files", "*.ico"),("Image Files", "*.webp")))]
                        ], element_justification='c')
        ]],[
        [sg.Column([
            [sg.Text('Enviroments',font="bold")],[sg.Listbox(values=enviromentTags,default_values=([enviromentTags[enviroment] for enviroment in mini["tags"]["enviromentTags"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--enironments--")],
                    [sg.Input(key='-ENV-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddEnv', size=(5, None))],
            [sg.Text('Planes',font="bold")],[sg.Listbox(values=planeTags,default_values=([planeTags[enviroment] for enviroment in mini["tags"]["planeTags"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--planes--")],
                    [sg.Input(key='-PLNS-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddPlanes', size=(5, None))]
            ]),sg.Column([
            [sg.Text('Sizes',font="bold")],[sg.Listbox(values=sizeTags,default_values=([sizeTags[enviroment] for enviroment in mini["tags"]["SizeTags"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--sizes--")],
                    [sg.Input(key='-SIZE-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddSize', size=(5, None))],
            [sg.Text('Creature Types',font="bold")],[sg.Listbox(values=creatureTypeTags,default_values=([creatureTypeTags[enviroment] for enviroment in mini["tags"]["CreatureTypeTags"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--crtypes--")],
                    [sg.Input(key='-CRTP-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddCreatureType', size=(5, None))]
            ]),sg.Column([
            [sg.Text('Classes',font="bold")],[sg.Listbox(values=creatureClassTag,default_values=([creatureClassTag[enviroment] for enviroment in mini["tags"]["CreatureClassTag"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--classes--")],
                    [sg.Input(key='-CLASS-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddClass', size=(5, None))],
            [sg.Text('Species',font="bold")],[sg.Listbox(values=creatureSpeciesTags,default_values=([creatureSpeciesTags[enviroment] for enviroment in mini["tags"]["SpeciesTag"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--speciess--")],
                    [sg.Input(key='-SPCS-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddSpecies', size=(5, None))]
            ]),sg.Column([
            [sg.Text('Movements',font="bold")],[sg.Listbox(values=creatureMovementTag,default_values=([creatureMovementTag[enviroment] for enviroment in mini["tags"]["CreatureMovementTag"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--movements--")],
                    [sg.Input(key='-MOVEMENT-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddMove', size=(5, None))],
            [sg.Text('Attacks',font="bold")],[sg.Listbox(values=creatureAttackTags,default_values=([creatureAttackTags[enviroment] for enviroment in mini["tags"]["CreatureAttackTags"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 10),
                key="--atacks--")],
                    [sg.Input(key='-ATKS-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddAttack', size=(5, None))]
            ]),
            sg.Column([
            [sg.Text('Tags',font="bold")],[sg.Listbox(values=additionalTags,default_values=([additionalTags[enviroment] for enviroment in mini["tags"]["AdditionalTag"]
                ]),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                enable_events=True,
                size=(15, 24),
                key="--tags--")],
                    [sg.Input(key='-TAG-', size=(10, None), enable_events=True),
                     sg.Button("Add", key='AddTag', size=(5, None))]])
        ]],[sg.Button('Save'),sg.Button('Exit')]]

    ]
    helpwindow = sg.Window("Edit/Add Mini", editorLayout, modal=True, element_justification='c')
    choice = None

    while True:
        event, values = helpwindow.read()
        if event == sg.WIN_CLOSED:
            return initialMini
            break
        if event == "Exit":
            if sg.popup_ok_cancel("Exit without saving?"):
                mini = initialMini.copy()
                break
        if event == '-PRICE-':
            if re.match(r'^$|^\d+(?:\.\d*)?$', values['-PRICE-']) is None:
                if values['-PRICE-'] == ".":
                    helpwindow['-PRICE-'].update("0.")
                    price = values['-PRICE-']
                else:
                    helpwindow['-PRICE-'].update(price)
            else:
                price = values['-PRICE-']
        if event == "AddPainter":
            newPainter = values['-PAINT-']
            if not newPainter.strip() == "":
                if not newPainter in painters:
                    painters.append(newPainter)
                painterid = painters.index(newPainter)
                indices = list(helpwindow['--painters--'].GetIndexes())
                if painterid in indices:
                    indices.remove(painterid)
                else:
                    indices.append(painterid)
                mini["PhysicalOptions"]["Painters"]=indices
                helpwindow['--painters--'].update(values=painters,set_to_index=indices,scroll_to_index=painterid)
        if event == "AddStatus":
            newStatus = values['-STATUS-']
            if not newStatus.strip() == "":
                if not newStatus in statuses:
                    statuses.append(newStatus)
                statusid = statuses.index(newStatus)
                mini["PhysicalOptions"]["Status"]=statusid
                helpwindow['--status--'].update(values=statuses,set_to_index=[statusid],scroll_to_index=statusid)
        if event == "AddMaterial":
            newStatus = values['-MATERIAL-']
            if not newStatus.strip() == "":
                if not newStatus in materials:
                    materials.append(newStatus)
                statusid = materials.index(newStatus)
                indices = list(helpwindow['--material--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["PhysicalOptions"]["Material"]=indices
                helpwindow['--material--'].update(values=materials,set_to_index=indices,scroll_to_index=statusid)
        if event == "ChangeImage":
            link = values["ChangeImage"]
            linkExists = "\u274C"
            if os.path.exists(link):
                linkExists = "\u2714"
            helpwindow['--imagepos--'].update(link)
            helpwindow['--imageexists--'].update(linkExists)
        if event == "AddEnv":
            newStatus = values['-ENV-']
            if not newStatus.strip() == "":
                if not newStatus in enviromentTags:
                    enviromentTags.append(newStatus)
                statusid = enviromentTags.index(newStatus)
                indices = list(helpwindow['--enironments--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["enviromentTags"]=indices
                helpwindow['--enironments--'].update(values=enviromentTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddPlanes":
            newStatus = values['-PLNS-']
            if not newStatus.strip() == "":
                if not newStatus in planeTags:
                    planeTags.append(newStatus)
                statusid = planeTags.index(newStatus)
                indices = list(helpwindow['--planes--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["planeTags"]=indices
                helpwindow['--planes--'].update(values=planeTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddSize":
            newStatus = values['-SIZE-']
            if not newStatus.strip() == "":
                if not newStatus in sizeTags:
                    sizeTags.append(newStatus)
                statusid = sizeTags.index(newStatus)
                indices = list(helpwindow['--sizes--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["SizeTags"]=indices
                helpwindow['--sizes--'].update(values=sizeTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddCreatureType":
            newStatus = values['-CRTP-']
            if not newStatus.strip() == "":
                if not newStatus in creatureTypeTags:
                    creatureTypeTags.append(newStatus)
                statusid = creatureTypeTags.index(newStatus)
                indices = list(helpwindow['--crtypes--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["CreatureTypeTags"]=indices
                helpwindow['--crtypes--'].update(values=creatureTypeTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddClass":
            newStatus = values['-CLASS-']
            if not newStatus.strip() == "":
                if not newStatus in creatureClassTag:
                    creatureClassTag.append(newStatus)
                statusid = creatureTypeTags.index(newStatus)
                indices = list(helpwindow['--classes--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["CreatureClassTag"]=indices
                helpwindow['--classes--'].update(values=creatureClassTag,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddSpecies":
            newStatus = values['-SPCS-']
            if not newStatus.strip() == "":
                if not newStatus in creatureSpeciesTags:
                    creatureSpeciesTags.append(newStatus)
                statusid = creatureSpeciesTags.index(newStatus)
                indices = list(helpwindow['--speciess--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["SpeciesTag"]=indices
                helpwindow['--speciess--'].update(values=creatureSpeciesTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddMove":
            newStatus = values['-MOVEMENT-']
            if not newStatus.strip() == "":
                if not newStatus in creatureMovementTag:
                    creatureMovementTag.append(newStatus)
                statusid = creatureMovementTag.index(newStatus)
                indices = list(helpwindow['--movements--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["CreatureMovementTag"]=indices
                helpwindow['--movements--'].update(values=creatureMovementTag,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddAttack":
            newStatus = values['-ATKS-']
            if not newStatus.strip() == "":
                if not newStatus in creatureAttackTags:
                    creatureAttackTags.append(newStatus)
                statusid = creatureAttackTags.index(newStatus)
                indices = list(helpwindow['--atacks--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["CreatureAttackTags"]=indices
                helpwindow['--atacks--'].update(values=creatureAttackTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "AddTag":
            newStatus = values['-TAG-']
            if not newStatus.strip() == "":
                if not newStatus in additionalTags:
                    additionalTags.append(newStatus)
                statusid = additionalTags.index(newStatus)
                indices = list(helpwindow['--tags--'].GetIndexes())
                if statusid in indices:
                    indices.remove(statusid)
                else:
                    indices.append(statusid)
                mini["tags"]["AdditionalTag"]=indices
                helpwindow['--tags--'].update(values=additionalTags,set_to_index=indices,scroll_to_index=statusid)
        if event == "Save":
            if link != f'{cfg["Images Location"]}/{id}.png':
                if os.path.exists(link):
                    im = Image.open(link)
                    im.thumbnail((800,600))
                    im.save(f'{cfg["Images Location"]}/{id}.png')
            mini["name"]= values['-NAME-']
            mini["source"]= values['-SOURCE-']
            mini["comment"]= values['-COMMENT-']
            mini["link"]= values['-LINK-']
            mini["storageLocation"]= values["-LOCATION-"]
            try:
                mini["price"]=float(values["-PRICE-"])
            except:
                mini["price"]=-1
            mini["PhysicalOptions"]["Painters"] = list(helpwindow['--painters--'].GetIndexes())
            mini["PhysicalOptions"]["Status"]=list(helpwindow['--status--'].GetIndexes())[0]
            mini["PhysicalOptions"]["Material"] = list(helpwindow['--material--'].GetIndexes())
            mini["PhysicalOptions"]["Kitbash Sources"] = values['--kitSources--'].split()
            mini["tags"]["enviromentTags"] = list(helpwindow['--enironments--'].GetIndexes())
            mini["tags"]["planeTags"] = list(helpwindow['--planes--'].GetIndexes())
            mini["tags"]["SizeTags"] = list(helpwindow['--sizes--'].GetIndexes())
            mini["tags"]["CreatureTypeTags"] = list(helpwindow['--crtypes--'].GetIndexes())
            mini["tags"]["CreatureClassTag"] = list(helpwindow['--classes--'].GetIndexes())
            mini["tags"]["SpeciesTag"] = list(helpwindow['--speciess--'].GetIndexes())
            mini["tags"]["CreatureMovementTag"] = list(helpwindow['--movements--'].GetIndexes())
            mini["tags"]["CreatureAttackTags"] = list(helpwindow['--atacks--'].GetIndexes())
            mini["tags"]["AdditionalTag"] = list(helpwindow['--tags--'].GetIndexes())
            break

    helpwindow.close()
    return mini

def open_help_window():
    helplayout = [
        [
            sg.Text('Help',font=("",20))
        ],
        [
            sg.Text('Default searching seraches all fields.')
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
            sg.Table(values=sorted(searchIndicators), headings=inHeaders,size=(80, 10))
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

def function_all(x,mini):
    if function_in(x,mini.name):
        return True
    if function_in(x,mini.source):
        return True
    if function_in(x,mini.link):
        return True
    if function_in(x,mini.price):
        return True
    if function_in(x,mini.location):
        return True
    if function_in(x," ".join([painters[painter] for painter in mini.painters])):
        return True
    if function_in(x,statuses[mini.status]):
        return True
    if function_in(x," ".join([materials[material] for material in mini.material])):
        return True
    if function_in(x,mini.comment):
        return True
    if function_in(x," ".join([enviromentTags[enviroment] for enviroment in mini.enviroments])):
        return True
    if function_in(x," ".join([planeTags[plane] for plane in mini.planes])):
        return True
    if function_in(x," ".join([sizeTags[size] for size in mini.sizes])):
        return True
    if function_in(x," ".join([creatureTypeTags[type] for type in mini.types])):
        return True
    if function_in(x," ".join([creatureClassTag[clas] for clas in mini.classes])):
        return True
    if function_in(x," ".join([creatureMovementTag[movement] for movement in mini.movements])):
        return True
    if function_in(x," ".join([creatureAttackTags[attack] for attack in mini.attacks])):
        return True
    if function_in(x," ".join([additionalTags[tag] for tag in mini.tags])):
        return True
    if function_in(x," ".join([creatureSpeciesTags[species] for species in mini.species])):
        return True
    return False
def function_in(x,y):
    return (x.lower() in str(y).lower())
def function_eq(x,y):
    return (x == str(y))
def function_rx(x,y):
    pattern = re.compile(x)
    return (pattern.match(str(y)))
def function_ni(x,y):
    return not(x.lower() in str(y).lower())

def search(termString):
    preFilteredValues = originalValues.copy()
    #print(filteredValues)
    terms = termString.split(";")
    for term in terms:
        #any([n in term for n in [":","=","~","#"]]):""
        function=function_all
        indTxt=False
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
            if indTxt[0]=="nm":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.name), preFilteredValues))
            elif indTxt[0]=="sc":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.source), preFilteredValues))
            elif indTxt[0]=="li":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.link), preFilteredValues))
            elif indTxt[0]=="pr":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.price), preFilteredValues))
            elif indTxt[0]=="lo":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.location), preFilteredValues))
            elif indTxt[0]=="pt":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([painters[painter] for painter in mini.painters])), preFilteredValues))
            elif indTxt[0]=="st":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],statuses[mini.status]), preFilteredValues))
            elif indTxt[0]=="mt":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([materials[material] for material in mini.material])), preFilteredValues))
            elif indTxt[0]=="cm":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1],mini.comment), preFilteredValues))
            elif indTxt[0]=="ev":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([enviromentTags[enviroment] for enviroment in mini.enviroments])), preFilteredValues))
            elif indTxt[0]=="pl":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([planeTags[plane] for plane in mini.planes])), preFilteredValues))
            elif indTxt[0]=="sz":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([sizeTags[size] for size in mini.sizes])), preFilteredValues))
            elif indTxt[0]=="tp":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([creatureTypeTags[type] for type in mini.types])), preFilteredValues))
            elif indTxt[0]=="cl":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([creatureClassTag[clas] for clas in mini.classes])), preFilteredValues))
            elif indTxt[0]=="mv":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([creatureMovementTag[movement] for movement in mini.movements])), preFilteredValues))
            elif indTxt[0]=="at":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([creatureAttackTags[attack] for attack in mini.attacks])), preFilteredValues))
            elif indTxt[0]=="tg":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([additionalTags[tag] for tag in mini.tags])), preFilteredValues))
            elif indTxt[0]=="sp":
                preFilteredValues = list(filter(lambda mini: function(indTxt[1]," ".join([creatureSpeciesTags[species] for species in mini.species])), preFilteredValues))
        elif term:
            preFilteredValues = list(filter(lambda mini: function_all(term,mini), preFilteredValues))
    global filteredValues
    filteredValues = preFilteredValues.copy()
    window.Element("--list--").Update(filteredValues)
def save():
    out = {"possibleTags": { "enviromentTags": enviromentTags,"planeTags": planeTags,"SizeTags": sizeTags,"CreatureTypeTags": creatureTypeTags,"CreatureClassTag": creatureClassTag,"CreatureMovementTag": creatureMovementTag,"CreatureAttackTags": creatureAttackTags, "SpeciesTag": creatureSpeciesTags,"AdditionalTag": additionalTags},
        "PhysicalOptions": {"Painters": painters, "Status": statuses,"Material": materials},
        "Sources": scanSources,
        "Minis": dictValues}
    with open(cfg["File Location"], "w") as outfile:
        json.dump(out, outfile, indent=4)
def update_values(miniature):
    window.Element('-text-').Update(miniature)
    path = cfg["Images Location"]+"/"+miniature.id+".png"
    if os.path.exists(path):
        image = Image.open(path)
    else:
        image = Image.new(mode="RGB", size=(400, 300))
    image.thumbnail((400,300))
    tk_img = ImageTk.PhotoImage(image)
    window.Element('-IMAGE-').Update(data=tk_img)
    kitbash = ""
    if miniature.kitSources:
        kitbash = " ["
        for source in miniature.kitSources:
            kitbash += source+", "
        kitbash = kitbash[:-2]+"]"
    window.Element('-source-').Update(miniature.source+kitbash)
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
    sc = ""
    for species in miniature.species:
        sc = sc+creatureSpeciesTags[species]+", "
    window.Element('-species-').Update(sc[:-2])
    cls=""
    for clas in miniature.classes:
        cls = cls+creatureClassTag[clas]+", "
    window.Element('-class-').Update(cls[:-2])
    mov=""
    for movement in miniature.movements:
        mov = mov+creatureMovementTag[movement]+", "
    window.Element('-mov-').Update(mov[:-2])
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
    elif event == "-link-":
        link = window.Element('-link-').DisplayText
        if re.match(linkregex,link):
            webbrowser.open(link, new=0, autoraise=True)
    elif event == 'Edit':
        ids = window.Element('--list--').GetIndexes()
        if filteredValues and ids:
            obj = filteredValues[ids[0]]
            mini = dictValues[obj.id]
            id = window["--list--"].GetIndexes()[0]
            dictValues[obj.id] = open_edit_window(mini, obj.id)
            save()
            originalValues = sorted([Miniature(n,m)  for m,n in data["Minis"].items()])
            filteredValues = originalValues.copy()
            search(values["-IN-"])
            window.Element("--list--").Update(filteredValues,set_to_index=[id],scroll_to_index=id)
            obj = filteredValues[id]
            update_values(obj)
    elif event == 'Add':
        id = 0
        while str(id) in dictValues:
            id+=1
        id = str(id)
        mini = {"name": "","PhysicalOptions": {"Painters": [],"Status": 0,"Material": [],"Kitbash Sources": []},"source": "","comment": "","tags": {"enviromentTags": [],"planeTags": [],"SizeTags": [], "CreatureTypeTags": [], "CreatureClassTag": [],"CreatureMovementTag": [],"CreatureAttackTags": [],"SpeciesTag": [],"AdditionalTag": []},"storageLocation": "?","statblocks": [],"link": "","price": ""}
        out = open_edit_window(mini, id)
        if out["name"] != "":
            dictValues[id] = out
        save()
        originalValues = sorted([Miniature(n,m)  for m,n in data["Minis"].items()])
        filteredValues = originalValues.copy()
        search(values["-IN-"])
        window.Element("--list--").Update(filteredValues)
    window.refresh()
window.close()
