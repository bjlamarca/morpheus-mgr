from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout, QGridLayout,
                               QHeaderView)
from PySide6.QtGui import Qt
from ui.utilities import get_icon_obj
from ui.widgets import ChoiceBox, LogViewer, StatusBar
from soteria.utilities import SoteriaUtilities
from soteria.models import SoteriaDevice
from devices.models import DeviceType   
 


class SoteriaSettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        #### Soteria List 
        device_list_grpbox = QGroupBox('Devices')
        device_btn_layout = QGridLayout()
        btn_add_device = QPushButton('Add Device')
        btn_add_device.clicked.connect(self.add_device)
        btn_add_device.setIcon(get_icon_obj('plus-circle'))
        btn_edit_device = QPushButton('Edit Device')
        btn_edit_device.clicked.connect(self.edit_device)
        btn_edit_device.setIcon(get_icon_obj('pencil'))
        btn_del_device = QPushButton('Delete Device')
        btn_del_device.clicked.connect(self.del_device)
        btn_del_device.setIcon(get_icon_obj('cross-circle'))
        device_btn_layout.addWidget(btn_add_device, 0, 0, 1, 1)
        device_btn_layout.addWidget(btn_edit_device, 0, 1, 1, 1)
        device_btn_layout.addWidget(btn_del_device, 0, 2, 1, 1)
        
        device_choicebox_layout = QHBoxLayout()
        self.device_choicebox = ChoiceBox()
        device_choicebox_layout.addWidget(self.device_choicebox)
        device_choicebox_layout.addStretch()
        
        device_tbl_layout = QHBoxLayout()
        self.device_table = QTableWidget()
        self.device_table.doubleClicked.connect(self.edit_device)
        hub_tbl_header = self.device_table.horizontalHeader()
        hub_tbl_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive) 
        hub_tbl_header.setStretchLastSection(True) 
        self.device_table.setMinimumWidth(550)
        device_tbl_layout.addWidget(self.device_table)
        device_tbl_layout.addStretch()

        device_list_layout = QVBoxLayout()
        device_list_layout.addLayout(device_btn_layout)
        device_list_layout.addLayout(device_choicebox_layout)
        device_list_layout.addLayout(device_tbl_layout)
        device_list_grpbox.setLayout(device_list_layout)

        #### Log viewer
        log_layout = QHBoxLayout()
        self.log_viewer = LogViewer()
        log_layout.addWidget(self.log_viewer)
        log_layout.addStretch()

        #### Status bar
        self.status_bar = StatusBar()
        
        #### Main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(device_list_grpbox, 0, 0, 1, 2)
        grid_layout.addLayout(log_layout, 0, 2, 1, 2)
        
        V_layout = QVBoxLayout()
        V_layout.addLayout(grid_layout)
        V_layout.addStretch()
        V_layout.addWidget(self.status_bar)
        H_layout = QHBoxLayout()
        H_layout.addLayout(V_layout)
        H_layout.addStretch()
        self.setWindowTitle("Devices")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.addLayout(H_layout)
        self.setLayout(self.main_layout)
        
        self.device_choicebox.hide()
        self.status_bar.set_msg({'type': 'message','status': 'info', 'message': 'Ready'}, 7)

      
    def showEvent(self, event):
        self.fill_device_table()
        
   
    def fill_device_table(self):
        self.device_table.clear()
        self.device_table.setColumnCount(5)
        self.device_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.device_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.device_table.setHorizontalHeaderLabels(['ID', 'Name', 'Type', 'Connected', 'IP Address', ])
        self.device_table.setColumnWidth(0, 50)
        self.device_table.setColumnWidth(1, 150)
        #self.device_table.verticalHeader().setVisible(False)
        #self.device_table.horizontalHeader().setStretchLastSection(True)
        device_qs = SoteriaDevice.select()
        self.device_table.setRowCount(device_qs.count())
        row = 0
        for device in device_qs:
            self.device_table.setItem(row, 0, QTableWidgetItem(str(device.id)))
            self.device_table.setItem(row, 1, QTableWidgetItem(device.name))
            self.device_table.setItem(row, 2, QTableWidgetItem(device.device_type.display_name))
            self.device_table.setItem(row, 3, QTableWidgetItem(device.connected))
            self.device_table.setItem(row, 4, QTableWidgetItem(device.ip_address))
            row += 1

    def add_device(self):
        dlg_add_device = SoteriaAddEdit(self, dlg_type='add')
        dlg_add_device.resize(400, 200)
        dlg_add_device.show()

    def edit_device(self):
        curr_row = self.device_table.currentRow()   
        if curr_row != -1:
            device_id = self.device_table.item(curr_row, 0).text()   
            dlg_edit_device = SoteriaAddEdit(self, dlg_type='edit', device_id=device_id)
            dlg_edit_device.resize(400, 200)
            dlg_edit_device.show()
        
    def del_device(self, caller=None, value=0):
        curr_row = self.device_table.currentRow()
        if  curr_row != -1:
            if caller == False:
                device_id = int(self.device_table.item(self.device_table.currentRow(), 0).text())
                self.device_choicebox.set_msg('Are you sure you want to delete this device?')
                self.device_choicebox.set_return_func(self.del_device, device_id)
                self.device_choicebox.show()
                
        if caller == 'yes':
            device_id = value
            soteria_util = SoteriaUtilities()
            result = soteria_util.delete_device(device_id) 
            if result['status'] == 'success':
                self.status_bar.set_msg(result)
                self.device_choicebox.hide()
                self.fill_device_table()
            elif result['status'] == 'error':
                self.msg_label.setText(result)
                self.device_choicebox.hide()
                
        elif caller == 'no':
            self.device_choicebox.hide()


class SoteriaAddEdit(QDialog):
    def __init__(self, parent=None, dlg_type=None, device_id=None):
        super().__init__(parent)
        self.dlg_type = dlg_type
        self.device_id = device_id
        if self.dlg_type == 'add':
            self.setWindowTitle("Add Soteria")
        elif self.dlg_type == 'edit':   
            self.setWindowTitle("Edit Soteria")
        
        device_layout = QVBoxLayout(self)
        
        self.le_name = QLineEdit()
        self.le_model_number = QLineEdit()
        self.cmbox_device_type = QComboBox()
        self.le_identifier = QLineEdit()
        self.ip_addr = QLineEdit()
        self.le_mac_addr = QLineEdit()
        self.chkbx_supervised = QCheckBox()

        form_layout = QFormLayout()
        form_layout.addRow("Name", self.le_name)
        form_layout.addRow("Model Number", self.le_model_number)
        form_layout.addRow("Device Type", self.cmbox_device_type)
        form_layout.addRow("Identifier", self.le_identifier)
        form_layout.addRow("IP Address", self.ip_addr)
        form_layout.addRow("MAC Address", self.le_mac_addr)
        form_layout.addRow("Supervised", self.chkbx_supervised)
       
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.close)
        if self.dlg_type == 'add':
            self.btn_add_edit = QPushButton('Add')
            self.btn_add_edit.clicked.connect(self.add_device)
        elif self.dlg_type == 'edit':
            self.btn_add_edit = QPushButton('Save')
            self.btn_add_edit.clicked.connect(self.edit_device)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_add_edit)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        device_layout.addLayout(form_layout)
        device_layout.addLayout(btn_layout)
        device_layout.addLayout(msg_layout)
        device_layout.addStretch()

        self.fill_cmbox()
        if self.dlg_type == 'edit':
            device_obj = SoteriaDevice.get_by_id(self.device_id)
            self.le_name.setText(device_obj.name)
            self.le_model_number.setText(device_obj.model_number)
            self.cmbox_device_type.setCurrentIndex(self.cmbox_device_type.findData(device_obj.device_type.id))
            self.le_identifier.setText(device_obj.identifier)
            self.ip_addr.setText(device_obj.ip_address)
            self.le_mac_addr.setText(device_obj.mac_address)
            self.chkbx_supervised.setChecked(device_obj.supervised)

    def fill_cmbox(self):
        device_type_qs = DeviceType.select()
        self.cmbox_device_type.clear()
        for device_type in device_type_qs:
            self.cmbox_device_type.addItem(device_type.display_name, device_type.id)
        self.cmbox_device_type.setCurrentIndex(-1)
        self.cmbox_device_type.setEditable(True)
        self.cmbox_device_type.lineEdit().setPlaceholderText("Select Device Type")
        
    def add_device(self):
        soteria_util = SoteriaUtilities()
        dev_dict = self.create_device_dict()
        responce = soteria_util.add_device(dev_dict)
        if responce['status'] == 'success':
            self.parent().fill_device_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")


    def edit_device(self):
        soteria_util = SoteriaUtilities()
        dev_dict = self.create_device_dict()
        responce = soteria_util.edit_device(dev_dict)
        if responce['status'] == 'success':
            self.parent().fill_device_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")


    def create_device_dict(self):
        dev_dict = {
            'device_id': self.device_id,
            'name': self.le_name.text(),
            'model_number': self.le_model_number.text(),
            'device_type': self.cmbox_device_type.currentData(),
            'identifier': self.le_identifier.text(),
            'ip_address': self.ip_addr.text(),
            'mac_address': self.le_mac_addr.text(),
            'supervised': self.chkbx_supervised.isChecked()
        }
        return dev_dict