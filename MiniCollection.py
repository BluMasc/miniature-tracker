# hello_psg.py

import PySimpleGUI as sg
import os
import json
from pathlib import Path

p = Path(__file__).with_name('config.json')

with p.open('r') as f:
  cfg = json.load(f)

values = [str(i) for i in range(20)]

chooseColumn = [  [sg.Text('Models')],
            [sg.Input(key='-IN-', enable_events=True), sg.Button('Search', bind_return_key=True), sg.Button('Help')],
            [sg.Listbox(
                values=values,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                enable_events=True,
                size=(60, 20),
                key="list"),
                sg.Column("")],

            ]
editAddon = [
            [sg.Button('Edit') ,sg.Button('Add'),sg.Button('Delete')]
            ]

if cfg["Edit Mode"]:
    chooseColumn = chooseColumn+editAddon

infoColumn = [
    [sg.Text('Model', key='-text-',font=("",20))],
    [sg.Image(key="-IMAGE-")],
    [sg.Column([[sg.Text('Source',font="bold"),sg.Text('-', key='-source-')],
        [sg.Text('Link',font="bold"),sg.Text('-', key='-link-')],
        [sg.Text('Price',font="bold"),sg.Text('-', key='-price-')],
        [sg.Text('Painted By',font="bold"),sg.Text('-', key='-painted-')],
        [sg.Text('Status',font="bold"),sg.Text('-', key='-status-')],
        [sg.Text('Material',font="bold"),sg.Text('-', key='-material-')],
        [sg.Text('Location',font="bold"),sg.Text('-', key='-location-')]]),
    sg.Column([[sg.Text('Enviroment',font="bold"),sg.Text('-', key='-enviroment-')],
        [sg.Text('Plane',font="bold"),sg.Text('-', key='-plane-')],
        [sg.Text('Size',font="bold"),sg.Text('-', key='-size-')],
        [sg.Text('Type',font="bold"),sg.Text('-', key='-type-')],
        [sg.Text('Class',font="bold"),sg.Text('-', key='-class-')],
        [sg.Text('Attacks',font="bold"),sg.Text('-', key='-atk-')],
        [sg.Text('Tags',font="bold"),sg.Text('-', key='-tag-')]])],


]

layout = [
    [
        sg.Column(chooseColumn),
        sg.VSeperator(),
        sg.Column(infoColumn, element_justification='c'),
    ]
]

searchIndicators =[["","Name (: is default comperator)"],["so","Source"],["li","link"],["pr","price"]]
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
            sg.Table(values=searchIndicators, headings=inHeaders)
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

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "Help":
        open_help_window()
    elif event == "Discord Copy":
        copytoclip()
    window.refresh()
window.close()
