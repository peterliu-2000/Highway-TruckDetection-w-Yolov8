import PySimpleGUI as sg

def create_window(theme):
    sg.theme(theme)
    #sg.set_options(font='')
    layout = [
                [sg.Text('视频识别', font='_ 14 bold')],
                [sg.Text('视频路径'), sg.In(size=(40,1), key='video'), sg.FileBrowse('选择视频')],
                [sg.Text('-------------------------------------------------------------', font=20)],
                [sg.Text('置信度阈值',expand_x=True, justification='center', font=30), sg.Text('缩放百分比',expand_x=True, justification='center',font=30)],
                [sg.Slider(range=(0,10),orientation='h', default_value=6, size=(18,18), key='confidence',font=25,expand_x=True),sg.Slider(range=(0,100),orientation='h', default_value=50, size=(18,18), font=25, key='scale_percent', expand_x=True)],
                [sg.Text('-------------------------------------------------------------', font=20)],
                [sg.Checkbox('显示车辆计数',key='counter'), sg.Checkbox('同窗口显示', key='show')],
                [sg.Button('运行'), sg.Button('停止'), sg.Button('取消')],
                [sg.Image(filename='', key='display')]
    ]
    window = sg.Window('高速公路篷布货车识别系统', layout)
    return window