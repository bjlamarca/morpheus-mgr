
import sys
from pathlib import Path

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QFile, QTextStream
from hue.hueui import HueMainWindow

BASE_DIR = Path(__file__).resolve().parent.parent

def get_icon_obj(icon):
    path = 'C:\\Dev\\showdemon2\\showdemon\\files\\graphics\\' + icon + '.png'
    return QIcon(QPixmap(path))

def get_pix_obj(icon):
    path = 'C:\\Dev\\showdemon2\\showdemon\\files\\graphics\\' + icon + '.png'
    return QPixmap(path)
    

def load_stylesheet():
    qss_file = QFile('C:\\Dev\\showdemon2\\showdemon\\files\\style\\Combinear.qss')
    if not qss_file.open(QFile.ReadOnly | QFile.Text):
        print("Error opening QSS file")
        sys.exit(1)
    qss_stream = QTextStream(qss_file)
    qss_content = qss_stream.readAll()
    return qss_content


class WindowHandler():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance



    def __init__(cls):
        cls.win_obj_list = []
        #add primary windows to list
        hue_win = HueMainWindow()
        cls.win_obj_list.append(['huewin', hue_win, False])
        
        

    def show_window(cls, window):
        for win in cls.win_obj_list:
            if win[0] == window:
                win_obj = win[1]
                win_obj.show()
                win[2] = True

    def close_window(cls, window):
        for win in cls.win_obj_list:
            if win[0] == window:
                win_obj = win[1]
                win_obj.close()
                win[2] = False

    def close_all_windows(cls): 
        for win in cls.win_obj_list:
            win_obj = win[1]
            win_obj.close()
            win[2] = False