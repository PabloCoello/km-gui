from ctypes import alignment
from curses import color_content
from tkinter.constants import TRUE
import PySimpleGUI as sg
import os
import json
from km_tools import km
import pandas as pd

def get_layout():
    return [
        [sg.Text('KMEANS TOOL', font=("Helvetica", 20), text_color='black')],
        [sg.T("")],
        [sg.Text("Choose a file: ", font=("Helvetica", 15))],
        [sg.Input(size=(41)), sg.FileBrowse(key='-IN-', font=("Helvetica", 15), size=10)],
        [sg.Button('Submit', font=("Helvetica", 15), size=(10))],
        [sg.T("")],
        [sg.Text('Select features for clusterization:', font=("Helvetica", 15))],
        [sg.Listbox(values=[], size=(56, 5 + 1),enable_events=True, key='-VARNAMES-', select_mode='extended')],
        [sg.Button("Set features", font=("Helvetica", 15), size=10)],
        [sg.T("")],
        [sg.Canvas(key='-CANVAS1-')],
        [sg.Canvas(key='-CANVAS2-')],
        [sg.Text("Insert number of clusters:  ", font=("Helvetica", 15)), sg.Input(key='-NCLUST-', size=(27, 1))],
        [sg.Text("Insert number of iterations:", font=("Helvetica", 15)), sg.Input(key='-NIT-', size=(27, 1))],
        [sg.Checkbox('Multiple analysis:', font=("Helvetica", 15), default=False, key="-MULTIPLE-")],
        [sg.Button("Calculate", font=("Helvetica", 15), size=10)],
        [sg.T("")],
        [sg.T("")],
        [sg.Button("Save result", font=("Helvetica", 15), size=10), sg.T("     "), sg.Button("Save centroids", font=("Helvetica", 15), size=10), sg.T("     "), sg.Button("Show plot", font=("Helvetica", 15), size=10)]
    ] 

sg.theme('DarkBlue3')

window = sg.Window(title="km", layout=get_layout(), margins=(100,50))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'salir':
        break
    elif event == "Submit":
        data = pd.read_excel(values["-IN-"], engine='openpyxl')
        window['-VARNAMES-'].update(data.columns)
    elif event == 'Set features':
        res = km(data, values['-VARNAMES-'])
        window['-CANVAS1-'].update(res.get_optimal_nclust(40, 1000))
    elif event == 'Calculate':
        if values['-MULTIPLE-'] == False:
            res.fit_km(int(values['-NCLUST-']), int(values['-NIT-']))
            data['km_labels'] = res.get_labels()
        else:
            data = res.perform_km_multiple_analysis(int(values['-NCLUST-']), int(values['-NIT-']))
    elif event == 'Save result':
        data.to_excel('km_result.xlsx')
    elif event == 'Save centroids':
        if values['-MULTIPLE-'] == False:
            cent = pd.DataFrame(res.get_centroids())
        else:
            cent = pd.DataFrame(res.clusters)
        cent.columns = list(map(lambda x: 'cluster_' + str(x),cent.columns))
        cent.to_excel('km_centroids.xlsx')
    elif event == 'Show plot':
        window['-CANVAS2-'].update(res.get_km_plot())

window.close()