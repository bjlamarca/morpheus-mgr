
import sys
from pathlib import Path


from ui.huemain import HueMainWindow

BASE_DIR = Path(__file__).resolve().parent.parent




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