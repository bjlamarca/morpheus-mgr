
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout)
from PySide6.QtGui import Qt


from ui.utilities import get_icon_obj
from hue.models import HueBridge, HueDevice, HueButton, HueLight
from hue.utilities import HueUtilities
from hue.bridge import HueBridgeUtils
from ui.widgets import YesNoBox, LogViewer
from system.signals import Signal



class HueMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Philips Hue")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)

        self.tab_widget = QTabWidget()
        self.tab_manuf = QWidget()
        
        device_tab_widget = DeviceTab()
        general_tab_widget = GeneralTab()
        bridge_tab_widget = BridgeTab()

        self.tab_widget.addTab(device_tab_widget, "Devices")
        self.tab_widget.addTab(general_tab_widget, "General")
        self.tab_widget.addTab(bridge_tab_widget, "Bridges")
        self.layout.addWidget(self.tab_widget)
        self.layout.addStretch()

class DeviceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_device_layout = QVBoxLayout()
        self.setLayout(self.tab_device_layout)
        
        device_tbl_layout = QHBoxLayout()
        self.device_table = QTableWidget()
        self.device_table.setMinimumWidth(450)
        device_tbl_layout.addWidget(self.device_table)
        device_tbl_layout.addStretch()                
 
        self.tab_device_layout.addLayout(device_tbl_layout)
    
    def showEvent(self, event):
        self.fill_device_table()
        
    def fill_device_table(self):
        self.device_table.clear()
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

class GeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        signal = Signal()
        self.tab_general_layout = QVBoxLayout()
        self.setLayout(self.tab_general_layout)
        horz_layout = QHBoxLayout()

        btn_grpbox = QGroupBox()
        bridge_Vlayout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        btn_sync_device_types = QPushButton('Sync Device Types')
        btn_sync_device_types.clicked.connect(self.sync_device_types)
        btn_layout.addWidget(btn_sync_device_types)
        
        combo_layout = QHBoxLayout()
        self.bridge_combo = QComboBox()
        combo_layout.addWidget(self.bridge_combo)
        
        sync_bridge_layout = QHBoxLayout()  
        btn_sync_bridge = QPushButton('Sync Bridge')
        btn_sync_bridge.clicked.connect(self.sync_bridge)
        sync_bridge_layout.addWidget(btn_sync_bridge)
        
        bridge_Vlayout.addLayout(btn_layout)
        bridge_Vlayout.addLayout(combo_layout)
        bridge_Vlayout.addLayout(sync_bridge_layout)
        
        btn_grpbox.setLayout(bridge_Vlayout)
        horz_layout.addWidget(btn_grpbox)
        horz_layout.addStretch()
        self.tab_general_layout.addLayout(horz_layout)

        log_layout = QHBoxLayout()
        self.log_viewer = LogViewer()
        log_layout.addWidget(self.log_viewer)
        log_layout.addStretch()
        

        self.tab_general_layout.addLayout(horz_layout)
        self.tab_general_layout.addLayout(log_layout)
        self.tab_general_layout.addStretch()
        
        self.log_viewer.hide()
        self.fill_bridge_combo()
        signal.connect('hue_mgr_ui', self.updates_msg)

    def showEvent(self, event):
        self.fill_bridge_combo()

    def fill_bridge_combo(self):
        self.bridge_combo.clear()
        self.bridge_combo.addItem('Select Bridge', 0)
        bridge_qs = HueBridge.select()
        for bridge in bridge_qs:
            self.bridge_combo.addItem(bridge.name, bridge.id)


    def sync_device_types(self):
        hue_bridge = HueBridgeUtils()
        responce = hue_bridge.sync_device_types('hue_mgr_ui')

    def sync_bridge(self):
        bridge_id = self.bridge_combo.currentData()
        if bridge_id > 0:            
            hue_bridge = HueBridgeUtils()
            responce = hue_bridge.sync_bridge(bridge_id, 'hue_mgr_ui')

           
    def updates_msg(self, sender, msg_dict):
        self.log_viewer.update_log(msg_dict)
                


class BridgeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_bridge_layout = QVBoxLayout()
        self.setLayout(self.tab_bridge_layout)
        
        bridge_btn_layout = QHBoxLayout()
        btn_add_bridge = QPushButton('Add Bridge')
        btn_add_bridge.clicked.connect(self.add_bridge)
        btn_add_bridge.setIcon(get_icon_obj('plus-circle'))
        btn_edit_bridge = QPushButton('Edit Bridge')
        btn_edit_bridge.clicked.connect(self.edit_bridge)
        btn_edit_bridge.setIcon(get_icon_obj('pencil'))
        btn_del_bridge = QPushButton('Delete Bridge')
        btn_del_bridge.clicked.connect(self.del_bridge)
        btn_del_bridge.setIcon(get_icon_obj('cross-circle'))
        bridge_btn_layout.addWidget(btn_add_bridge)
        bridge_btn_layout.addWidget(btn_edit_bridge)
        bridge_btn_layout.addWidget(btn_del_bridge)
        bridge_btn_layout.addStretch()
        
        bridge_msgbox_layout = QHBoxLayout()
        self.bridge_msgbox = YesNoBox()
        bridge_msgbox_layout.addWidget(self.bridge_msgbox)
        bridge_msgbox_layout.addStretch()
        
        bridge_tbl_layout = QHBoxLayout()
        self.bridge_table = QTableWidget()
        self.bridge_table.setMinimumWidth(450)
        bridge_tbl_layout.addWidget(self.bridge_table)
        bridge_tbl_layout.addStretch()

        bridge_msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        bridge_msg_layout.addWidget(self.msg_label)
        bridge_msg_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        
        self.tab_bridge_layout.addLayout(bridge_btn_layout)
        self.tab_bridge_layout.addLayout(bridge_msgbox_layout)
        self.tab_bridge_layout.addLayout(bridge_tbl_layout)
        self.tab_bridge_layout.addStretch()

        self.bridge_msgbox.hide()

      
    def showEvent(self, event):
        self.fill_bridge_table()
        
   
    def fill_bridge_table(self):
        self.bridge_table.clear()
        self.bridge_table.setColumnCount(4)
        self.bridge_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bridge_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bridge_table.setHorizontalHeaderLabels(['Name', 'IP Address', 'Username', 'ID'])
        #self.bridge_table.horizontalHeader().setStretchLastSection(True)
        bridge_qs = HueBridge.select()
        self.bridge_table.setRowCount(bridge_qs.count())
        row = 0
        for bridge in bridge_qs:
            self.bridge_table.setItem(row, 0, QTableWidgetItem(bridge.name))
            self.bridge_table.setItem(row, 1, QTableWidgetItem(bridge.ip_addr))
            self.bridge_table.setItem(row, 2, QTableWidgetItem(bridge.username))
            self.bridge_table.setItem(row, 3, QTableWidgetItem(str(bridge.id)))
            row += 1



    def add_bridge(self):
        dlg_add_bridge = BridgeAddEdit(self, dlg_type='add')
        dlg_add_bridge.resize(400, 200)
        dlg_add_bridge.show()

    def edit_bridge(self):
        curr_row = self.bridge_table.currentRow()   
        if curr_row != -1:
            bridge_id = self.bridge_table.item(curr_row, 3).text()   
            dlg_edit_bridge = BridgeAddEdit(self, dlg_type='edit', bridge_id=bridge_id)
            dlg_edit_bridge.resize(400, 200)
            dlg_edit_bridge.show()
        
    def del_bridge(self, caller=None, value=0):
        curr_row = self.bridge_table.currentRow()
        if  curr_row != -1:
            if caller == False:
                bridge_id = int(self.bridge_table.item(self.bridge_table.currentRow(), 3).text())
                self.bridge_msgbox.set_msg('Are you sure you want to delete this bridge?')
                self.bridge_msgbox.set_return_func(self.del_bridge, bridge_id)
                self.bridge_msgbox.show()
                
        if caller == 'yes':
            bridge_id = value
            hue_util = HueUtilities()
            result = hue_util.delete_bridge(bridge_id)
            if result['status'] == 'success':
                self.msg_label.setText(result['message'])
                self.bridge_msgbox.hide()
                self.fill_bridge_table()
            elif result['status'] == 'error':
                self.msg_label.setText(result['message'])
                self.msg_label.setStyleSheet('color: red')
                self.bridge_msgbox.hide()
                
        elif caller == 'no':
            self.bridge_msgbox.hide()


class BridgeAddEdit(QDialog):
    def __init__(self, parent=None, dlg_type=None, bridge_id=None):
        super().__init__(parent)
        self.dlg_type = dlg_type
        self.bridge_id = bridge_id
        if self.dlg_type == 'add':
            self.setWindowTitle("Add Bridge")
        elif self.dlg_type == 'edit':   
            self.setWindowTitle("Edit Bridge")
        
        bridge_layout = QVBoxLayout(self)
        
        self.name = QLineEdit()
        self.ip_addr = QLineEdit()
        self.username = QLineEdit()
        self.key = QLineEdit()
        
        form_layout = QFormLayout()
        form_layout.addRow("Name", self.name)
        form_layout.addRow("IP Address", self.ip_addr)
        form_layout.addRow("Username", self.username)
        form_layout.addRow("Key", self.key)
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.close)
        if self.dlg_type == 'add':
            self.btn_add_edit = QPushButton('Add')
            self.btn_add_edit.clicked.connect(self.add_bridge)
        elif self.dlg_type == 'edit':
            self.btn_add_edit = QPushButton('Save')
            self.btn_add_edit.clicked.connect(self.edit_bridge)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_add_edit)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        bridge_layout.addLayout(form_layout)
        bridge_layout.addLayout(btn_layout)
        bridge_layout.addLayout(msg_layout)
        bridge_layout.addStretch()

        if self.dlg_type == 'edit':
            bridge_obj = HueBridge.get_by_id(self.bridge_id)
            self.name.setText(bridge_obj.name)
            self.ip_addr.setText(bridge_obj.ip_addr)
            self.username.setText(bridge_obj.username)
            self.key.setText(bridge_obj.key)

        
        
    def add_bridge(self):
        hue_util = HueUtilities()
        responce = hue_util.add_bridge(self.name.text(), self.ip_addr.text(), self.username.text(), self.key.text())
        if responce['status'] == 'success':
            self.parent().fill_bridge_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")


    def edit_bridge(self):
        hue_util = HueUtilities()
        responce = hue_util.edit_bridge(self.bridge_id, self.name.text(), self.ip_addr.text(), self.username.text(), self.key.text())
        if responce['status'] == 'success':
            self.parent().fill_bridge_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")

