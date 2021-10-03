import PySimpleGUI as sg

sg.theme('DarkPurple1')

layout = [
    [sg.Text("prueba")],
    [sg.Input(KEY='-input-')],
    [sg.Text(size=(40,1), key='-OUTPUT-')],
    [sg.Button('OK')],
    [sg.Button('salir')]

]
window = sg.Window(title="km", layout=layout, margins=(100,50))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'salir':
        break
    window['-OUTPUT-'].update(values['-INPUT-'])
window.close()