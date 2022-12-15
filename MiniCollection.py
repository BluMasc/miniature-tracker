# hello_psg.py

import PySimpleGUI as sg
import os
from googletrans import Translator

trans = Translator(service_urls=['translate.googleapis.com'])
layout = [  [sg.Text('Welche Worte sollen uebersetzt werden?')],
            [sg.Input(key='-IN-', enable_events=True)],

            [sg.Button('TRANSLATE', bind_return_key=True)],

            [sg.Text("Ajawo' Script:"),sg.Text("",font=["Ajawo Script", 18],key='_AJAWO_',size=(20,1))],

            [sg.Button('Discord Copy')]

            ]

# Create the window
window = sg.Window("Ajawo' Translator", layout)

def translate ():
    ui = values["-IN-"]

    uis = str(ui)

    tui = trans.translate(uis)
    print(tui.text)
    window.Element('_AJAWO_').Update(tui.text)

def copytoclip ():
    ui = values["-IN-"]
    uis = str(ui)
    tui = trans.translate(uis)
    print(tui.text)
    window.Element('_AJAWO_').Update(tui.text)
    char_to_replace = {
                        ' ':"    ",
                        'a':":AjawoHouse: ",
                        'b':":AjawoWave: ",
                        'c':":AjawoSwoosh: ",
                        'd':":AjawoPincer: ",
                        'e':":AjawoHorns: ",
                        'f':":AjawoSnake: ",
                        'g':":AjawoIron: ",
                        'h':":AjawoBow: ",
                        'i':":AjawoCandle: ",
                        'j':":AjawoBird: ",
                        'k':":AjawoFaucet: ",
                        'l':":AjawoParalel: ",
                        'm':":AjawoSerpent: ",
                        'n':":AjawoCyclon: ",
                        'o':":AjawoScythe: ",
                        'p':":AjawoTree: ",
                        'q':":AjawoCrown: ",
                        'r':":AjawoChair: ",
                        's':":AjawoCup: ",
                        't':":AjawoBoat: ",
                        'u':":AjawoFling: ",
                        'v':":AjawoKick: ",
                        'w':":AjawoGrab: ",
                        'x':":AjawoDagger: ",
                        'y':":AjawoHook: ",
                        'z':":AjawoClam: ",
                        '.':":AjawoCircle: ",
                        ',':":AjawoLocation: ",
                        "'":":AjawoReverseLocation: ",
                        '!':":AjawoScratch: ",
                        '?':":AjawoThreeway: ",
                        ';':":AjawoRaindrop: ",
                        ':':":AjawoHalfcircle: ",
                        '"':":AjawoFairy: "
                        }
    out = tui.text.lower().translate(str.maketrans(char_to_replace))
    command = 'echo ' + out.strip() + '| clip'
    os.system(command)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "TRANSLATE":
        translate()
    elif event == "Discord Copy":
        copytoclip()
    window.refresh()
window.close()
