from tkinter.constants import TRUE
import PySimpleGUI as sg
import os
import json
from km_tools import km
import pandas as pd

def get_layout():
    return [
        [sg.Text('Kmeans Tool', font=("Helvetica", 15), size=(20, 1), text_color='green')],
        [sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key='-IN-')],
        [sg.Button("Submit")],
        [sg.Text('Select features for clusterization', font=("Helvetica", 15), size=(40, 1))],
        [sg.Listbox(values=[], size=(30, 5 + 1),enable_events=True, key='-VARNAMES-', select_mode='extended')],
        [sg.Button("Set features")],
        [sg.Canvas(key='-CANVAS1-')],
        [sg.Canvas(key='-CANVAS2-')],
        [sg.Text("Insert number of clusters"), sg.Input(key='-NCLUST-')],
        [sg.Text("Insert number of iterations"), sg.Input(key='-NIT-')],
        [sg.Checkbox('Multiple analysis:', default=False, key="-MULTIPLE-")],
        [sg.Button("Calculate")],
        [sg.Button("Save result"), sg.Button("Save centroids"), sg.Button("Show plot")]
    ] 

sg.theme('DarkPurple1')

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