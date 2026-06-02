import PySimpleGUI as sg
import multiprocessing
import psutil

def worker():
    while True:
        x = 1000000 * 1000000
        x = x ** 2

if __name__ == '__main__':
    multiprocessing.freeze_support()
    processes = []
    is_stressing = False  
    
    layout = [
        [sg.Push(), sg.Button('Число', key='-START-'), sg.Button('Стоп', key='-STOP-'), sg.Push()],
        [sg.Push(), sg.Text('Результат', key='-LOAD-', font=('Helvetica', 20)), sg.Push()]
    ]
    
    window = sg.Window('рандомайзинер', layout, size=(400, 200))

    while True:
        event, values = window.read(timeout=500)
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            for p in processes: p.terminate()
            break
            
        if is_stressing:
            cpu_usage = psutil.cpu_percent()
            window['-LOAD-'].update(f'Результат: {cpu_usage}')
        else:
            window['-LOAD-'].update('Результат: 0')
            
        
        if event == '-START-' and not is_stressing:
            is_stressing = True
            for i in range(multiprocessing.cpu_count()):
                p = multiprocessing.Process(target=worker)
                p.start()
                processes.append(p)
        
        if event == '-STOP-':
            is_stressing = False
            for p in processes: p.terminate()
            processes = []

    window.close()