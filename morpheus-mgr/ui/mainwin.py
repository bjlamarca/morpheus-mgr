import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenu, QGroupBox, QPushButton
from PySide6.QtGui import QAction, QCloseEvent

from ui.utilities import WindowHandler
from system.ultilities import load_stylesheet
from system.websocket import webs_test



class MainWindow(QMainWindow):
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


def start_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = MainWindow()
    window.setGeometry(200, 200, 800, 200)
    window.show()
    app.exec_()