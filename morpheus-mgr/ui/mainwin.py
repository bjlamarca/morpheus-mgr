import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QMenu, QGroupBox, QPushButton, QMdiArea, QTabWidget)
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtCore import Qt

from ui.huemain import HueMainWindow

from ui.utilities import WindowHandler
from system.ultilities import load_stylesheet
from system.websocket import webs_test



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morpheus")
        menu_bar = self.menuBar()
        
        win_menu = QMenu("Window", self)

        hue_action = QAction("Hue", self)
        hue_action.triggered.connect(lambda: self.add_tab("huewin"))
        win_menu.addAction(hue_action)
        menu_bar.addMenu(win_menu)

        #Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        tab_layout = QHBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setMovable(True)
        tab_layout.addWidget(self.tab_widget)
        tab_layout.addStretch()

        main_layout.addLayout(tab_layout)

    
        main_layout.addStretch()
    
    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def closeEvent(self, event: QCloseEvent):
        event.accept

    def add_tab(self, name):
        if name == "huewin":
            hue_win = HueMainWindow()
            self.tab_widget.addTab(hue_win, "Hue")
            self.tab_widget.setCurrentWidget(hue_win)


    def connect_websocket(self):
        webs_test()




    def create_menus(self):
        menu_bar = self.menuBar()
        
        win_menu = QMenu("Window", self)

        hue_action = QAction("Hue", self)
        hue_action.triggered.connect(lambda: self.call_window("huewin"))
        win_menu.addAction(hue_action)
        menu_bar.addMenu(win_menu)
        
    def call_window(self, name):
        if name == "huewin":
            hue_win = HueMainWindow()
            sub = self.mdi_area.addSubWindow(hue_win)
            sub.show()
            


def start_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = MainWindow()
    #window.setGeometry(200, 200, 1000, 800)
    window.showMaximized()
    app.exec_()




    # self.websocket_grpbox = QGroupBox("Websocket")
        # websocket_layout = QHBoxLayout()
        # btn_connect = QPushButton("Connect")
        # btn_connect.clicked.connect(self.connect_websocket)
        # websocket_layout.addWidget(btn_connect)
        # websocket_layout.addStretch()
        # self.websocket_grpbox.setLayout(websocket_layout)
        
        #main_layout.addWidget(self.websocket_grpbox)