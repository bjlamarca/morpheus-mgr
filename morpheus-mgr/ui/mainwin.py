import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QMenu, QGroupBox, QPushButton, QMdiArea, QTabWidget)
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtCore import Qt

from ui.hueui import HueDeviceAllWindow
from ui.hubsettingsui import HubSettingsMainWindow
from ui.utilities import load_stylesheet, get_icon_obj
from system.signals import Signal


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        signal = Signal()
        signal.connect('main_status_bar', self.update_status_bar)
        self.setWindowTitle("Morpheus")
        self.setWindowIcon(get_icon_obj("dream-catcher"))
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready", 5000)
        menu_bar = self.menuBar()
        
        system_menu = QMenu("System", self)
        settings_action = QAction("Hub Settings", self)
        settings_action.triggered.connect(lambda: self.add_tab("hub_settings"))
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        system_menu.addAction(settings_action)
        system_menu.addAction(exit_action)
        
        interface_menu = QMenu("Interfaces", self)
        hue_submenu = QMenu("Hue", self)
        interface_menu.addMenu(hue_submenu)
        hue_action = QAction("Devices", self)
        hue_action.triggered.connect(lambda: self.add_tab("huedevices"))
        hue_submenu.addAction(hue_action)
        
        menu_bar.addMenu(system_menu)
        menu_bar.addMenu(interface_menu)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setMovable(True)

        self.setCentralWidget(self.tab_widget)

        #self.add_tab("huewin")
        #self.add_tab("hub_settings")
        
    
    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def closeEvent(self, event: QCloseEvent):
        event.accept

    def add_tab(self, name):
        if name == "hub_settings":
            settings_win = HubSettingsMainWindow()
            self.tab_widget.addTab(settings_win, "Hub Settings")
            self.tab_widget.setCurrentWidget(settings_win)
        if name == "huedevices":
            hue_dev_all_win = HueDeviceAllWindow()
            self.tab_widget.addTab(hue_dev_all_win, "Hue - Devices")
            self.tab_widget.setCurrentWidget(hue_dev_all_win)


    def connect_websocket(self):
        pass

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

    def update_status_bar(self, sender, msg):
        self.status_bar.showMessage(msg, 5000)


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