# hello_psg.py

import PySimpleGUI as sg
import os
import json
from pathlib import Path
from MiniatureClass import Miniature

p = Path(__file__).with_name('config.json')

with p.open('r') as f:
  cfg = json.load(f)

if "PySimpleGUITheme" in cfg:
    sg.theme(cfg["PySimpleGUITheme"])

with open(cfg["File Location"], 'r') as f:
  data = json.load(f)

values = sorted([Miniature(n,m)  for m,n in data["Minis"].items()])

filteredValues = values.copy()

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
    [sg.Image(key="-IMAGE-")],
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

searchIndicators =[["",'Name (":" is default)'],["so","Source"],["li","link"],["pr","price"]]
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

def update_values(miniature):
    window.Element('-text-').Update(miniature)
    # Image missing
    window.Element('-source-').Update(miniature.source)
    window.Element('-link-').Update(miniature.link)
    window.Element('-price-').Update(miniature.price)
    window.Element('-painted-').Update(miniature.painters)
    window.Element('-status-').Update(miniature.status)
    window.Element('-material-').Update(miniature.material)
    window.Element('-location-').Update(miniature.location)
    window.Element('-enviroment-').Update(miniature.enviroments)
    window.Element('-plane-').Update(miniature.planes)
    window.Element('-size-').Update(miniature.sizes)
    window.Element('-type-').Update(miniature.types)
    window.Element('-class-').Update(miniature.classes)
    window.Element('-atk-').Update(miniature.attacks)
    window.Element('-tag-').Update(miniature.tags)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "Help":
        open_help_window()
    elif event == "--list--":
        ids = window[event].GetIndexes()
        obj = filteredValues[ids[0]]
        update_values(obj)
    window.refresh()
window.close()
