
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout, QGridLayout,
                               QHeaderView)
from PySide6.QtGui import Qt
from ui.utilities import get_icon_obj
from hue.models import HueBridge, HueDevice, HueButton, HueLight
from hue.utilities import HueUtilities
from hue.bridge import HueBridgeUtils
from ui.widgets import LogViewer
from system.signals import Signal



class HueDeviceAllWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        signal = Signal()
        
        #### Device Table
        dev_tbl_grpbox = QGroupBox()
        self.device_table = QTableWidget()
        dev_tbl_layout = QVBoxLayout(dev_tbl_grpbox)
        dev_tbl_layout.addWidget(self.device_table)
        dev_tbl_grpbox.setLayout(dev_tbl_layout)

        #### Sync functions
        sync_grpbox = QGroupBox()
        sync_grid_layout = QGridLayout()
        btn_sync_device_types = QPushButton('Sync Device Types')
        sync_lbl = QLabel('Sync Bridge')
        self.bridge_combo = QComboBox()
        btn_sync_device_types.clicked.connect(self.sync_device_types)
        btn_sync_bridge = QPushButton()
        btn_sync_bridge.setIcon(get_icon_obj('sync'))
        btn_sync_bridge.setMaximumWidth(25)

        btn_sync_bridge.clicked.connect(self.sync_bridge)
        sync_grid_layout.addWidget(btn_sync_device_types, 0, 0, 1, 3)
        sync_grid_layout.addWidget(sync_lbl, 1, 0, 1, 1)
        sync_grid_layout.addWidget(self.bridge_combo, 1, 1, 1, 1)
        sync_grid_layout.addWidget(btn_sync_bridge, 1, 2, 1, 1)
        sync_grpbox.setLayout(sync_grid_layout)

        #### Log viewer
        log_layout = QHBoxLayout()
        self.log_viewer = LogViewer()
        log_layout.addWidget(self.log_viewer)
        log_layout.addStretch()

        #### Main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(dev_tbl_grpbox, 0, 0, 2, 2)
        grid_layout.addWidget(sync_grpbox, 0, 2, 1, 1)
        grid_layout.addLayout(log_layout, 1, 2, 1, 2)

        V_layout = QVBoxLayout()
        V_layout.addLayout(grid_layout)
        H_layout = QHBoxLayout()
        H_layout.addLayout(V_layout)
        H_layout.addStretch()
        self.setWindowTitle("Devices")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.addLayout(H_layout)
        self.setLayout(self.main_layout)
        self.fill_device_table()
        self.fill_bridge_combo()
        
        signal.connect(self.receive_signals)
        signal.connect(self.receive_signals)

    def showEvent(self, event):
        pass
        
    def fill_device_table(self):
        self.device_table.clear()
        dev_tbl_header = self.device_table.horizontalHeader()
        dev_tbl_header.setStretchLastSection(True)
        dev_tbl_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.device_table.setMinimumWidth(450)
        self.device_table.setColumnCount(4)
        self.device_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.device_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.device_table.setHorizontalHeaderLabels(['Name', 'Device Type', 'Online', 'ID'])
        self.device_table.setColumnWidth(0, 150)
        self.device_table.setColumnWidth(1, 150)
        device_qs = HueDevice.select()
        self.device_table.setRowCount(device_qs.count())
        for index, device in enumerate(device_qs):
            self.device_table.setItem(index, 0, QTableWidgetItem(device.name))
            self.device_table.setItem(index, 1, QTableWidgetItem(device.device_type.display_name))
            self.device_table.setItem(index, 2, QTableWidgetItem(str(device.online)))

    def fill_bridge_combo(self):
        self.bridge_combo.clear()
        self.bridge_combo.addItem('Select Bridge', 0)
        bridge_qs = HueBridge.select()
        for bridge in bridge_qs:
            self.bridge_combo.addItem(bridge.name, bridge.id)


    def sync_device_types(self):
        hue_bridge = HueBridgeUtils()
        responce = hue_bridge.sync_device_types('hue_ui')

    def sync_bridge(self):
        bridge_id = self.bridge_combo.currentData()
        if bridge_id > 0:            
            hue_bridge = HueBridgeUtils()
            responce = hue_bridge.sync_bridge(bridge_id, 'hue_ui')

    def receive_signals(self, sender, msg_dict):
        self.log_viewer.update_log(msg_dict)
    
