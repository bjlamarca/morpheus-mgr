import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenu, QGroupBox, QPushButton, QMdiArea
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtCore import Qt

from ui.huemain import HueMainWindow

from ui.utilities import WindowHandler
from system.ultilities import load_stylesheet
from system.websocket import webs_test



class MainWindowOld(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morpheus")
        self.win_handler = WindowHandler()
        menu_bar = self.menuBar()
        
        win_menu = QMenu("Window", self)

        hue_action = QAction("Hue", self)
        hue_action.triggered.connect(lambda: self.call_window("huewin"))
        win_menu.addAction(hue_action)
        menu_bar.addMenu(win_menu)

        #Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.websocket_grpbox = QGroupBox("Websocket")
        websocket_layout = QHBoxLayout()
        btn_connect = QPushButton("Connect")
        btn_connect.clicked.connect(self.connect_websocket)
        websocket_layout.addWidget(btn_connect)
        websocket_layout.addStretch()
        self.websocket_grpbox.setLayout(websocket_layout)
        
        main_layout.addWidget(self.websocket_grpbox)
        main_layout.addStretch()

    def closeEvent(self, event: QCloseEvent):
        #ThreadTracker().stop_all_threads()
        self.win_handler.close_all_windows()
        event.accept

    def call_window(self, name):
        self.win_handler.show_window(name)

    def connect_websocket(self):
        webs_test()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdi_area)

        #self.mdi_area.subWindowActivated.connect(self.update_menus)

        #self.create_actions()
        self.create_menus()
        #self.create_tool_bars()
        #self.create_status_bar()
        #self.update_menus()

        #self.read_settings()

        self.setWindowTitle("Morpheus Manager")

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
    window.setGeometry(200, 200, 1000, 800)
    window.show()
    app.exec_()