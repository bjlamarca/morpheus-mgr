import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox)
from PySide6.QtGui import Qt



class HueMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Philips Hue")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)

        self.tab_widget = QTabWidget()
        self.tab_manuf = QWidget()
        self.tab_device = QWidget()
        self.tab_widget.addTab(self.tab_device, "Bridges")
        #self.tab_widget.addTab(self.tab_manuf, "Manufacture")
        
        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        
        self.layout.addWidget(self.tab_widget)
        self.layout.addLayout(msg_layout)
        
        self.init_tab_bridges()

    def init_tab_bridges(self):
        self.tab_device_layout = QVBoxLayout(self.tab_device)
        self.tab_device.setLayout(self.tab_device_layout)
        
        
        bridge_tbl_layout = QHBoxLayout()
        self.bridge_table = QTableWidget()
        self.bridge_table.setMaximumWidth(500)
        bridge_tbl_layout.addWidget(self.bridge_table)
        bridge_tbl_layout.addStretch()
        
        self.bridge_table.doubleClicked.connect(self.edit_bridge)
        
        self.tab_device_layout.addWidget(self.bridge_table)
        self.btn_layout = QHBoxLayout()
        self.add_bridge_btn = QPushButton("Add Bridge")
        self.add_bridge_btn.clicked.connect(self.add_bridge)
        self.btn_layout.addWidget(self.add_bridge_btn)
        self.btn_layout.addStretch()
        self.tab_device_layout.addLayout(self.btn_layout)

    def showEvent(self, event):
        self.fill_bridge_table()
        
    
    def init_tab_general(self):
        self.tab_general = QWidget()
        self.tab_general_layout = QVBoxLayout(self.tab_general)
        self.tab_general.setLayout(self.tab_general_layout)
        self.tab_general.addTab(self.tab_general, "General")

    def fill_bridge_table(self):
        self.bridge_table.clear()
        self.bridge_table.setColumnCount(3)
        self.bridge_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bridge_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bridge_table.setHorizontalHeaderLabels(["Name", "IP Address", "Username"])
        self.bridge_table.horizontalHeader().setStretchLastSection(True)

    def add_bridge(self):
        pass

    def edit_bridge(self):
        pass
        
        
