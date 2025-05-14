from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout, QGridLayout,
                               QHeaderView)
from PySide6.QtGui import Qt
from ui.utilities import get_icon_obj
from ui.widgets import ChoiceBox, LogViewer, StatusBar
from hue.models import HueBridge
from hue.utilities import HueUtilities


class HueBridgeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        #### Bridge List 
        bridge_list_grpbox = QGroupBox('Bridges')
        bridge_btn_layout = QGridLayout()
        btn_add_bridge = QPushButton('Add Bridge')
        btn_add_bridge.clicked.connect(self.add_bridge)
        btn_add_bridge.setIcon(get_icon_obj('plus-circle'))
        btn_edit_bridge = QPushButton('Edit Bridge')
        btn_edit_bridge.clicked.connect(self.edit_bridge)
        btn_edit_bridge.setIcon(get_icon_obj('pencil'))
        btn_del_bridge = QPushButton('Delete Bridge')
        btn_del_bridge.clicked.connect(self.del_bridge)
        btn_del_bridge.setIcon(get_icon_obj('cross-circle'))
        bridge_btn_layout.addWidget(btn_add_bridge, 0, 0, 1, 1)
        bridge_btn_layout.addWidget(btn_edit_bridge, 0, 1, 1, 1)
        bridge_btn_layout.addWidget(btn_del_bridge, 0, 2, 1, 1)
        
        bridge_choicebox_layout = QHBoxLayout()
        self.bridge_choicebox = ChoiceBox()
        bridge_choicebox_layout.addWidget(self.bridge_choicebox)
        bridge_choicebox_layout.addStretch()
        
        bridge_tbl_layout = QHBoxLayout()
        self.bridge_table = QTableWidget()
        self.bridge_table.doubleClicked.connect(self.edit_bridge)
        hub_tbl_header = self.bridge_table.horizontalHeader()
        hub_tbl_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive) 
        hub_tbl_header.setStretchLastSection(True) 
        self.bridge_table.setMinimumWidth(375)
        bridge_tbl_layout.addWidget(self.bridge_table)
        bridge_tbl_layout.addStretch()

        bridge_list_layout = QVBoxLayout()
        bridge_list_layout.addLayout(bridge_btn_layout)
        bridge_list_layout.addLayout(bridge_choicebox_layout)
        bridge_list_layout.addLayout(bridge_tbl_layout)
        bridge_list_grpbox.setLayout(bridge_list_layout)

        #### Log viewer
        log_layout = QHBoxLayout()
        self.log_viewer = LogViewer()
        log_layout.addWidget(self.log_viewer)
        log_layout.addStretch()

        #### Status bar
        self.status_bar = StatusBar()
        
        #### Main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(bridge_list_grpbox, 0, 0, 1, 2)
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
        
        self.bridge_choicebox.hide()
        self.status_bar.set_msg({'type': 'message','status': 'info', 'message': 'Ready'}, 7)

      
    def showEvent(self, event):
        self.fill_bridge_table()
        
   
    def fill_bridge_table(self):
        self.bridge_table.clear()
        self.bridge_table.setColumnCount(3)
        self.bridge_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bridge_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bridge_table.setHorizontalHeaderLabels(['ID', 'Name', 'IP Address'])
        self.bridge_table.setColumnWidth(0, 50)
        self.bridge_table.setColumnWidth(1, 150)
        self.bridge_table.verticalHeader().setVisible(False)
        #self.bridge_table.horizontalHeader().setStretchLastSection(True)
        bridge_qs = HueBridge.select()
        self.bridge_table.setRowCount(bridge_qs.count())
        row = 0
        for bridge in bridge_qs:
            self.bridge_table.setItem(row, 0, QTableWidgetItem(str(bridge.id)))
            self.bridge_table.setItem(row, 1, QTableWidgetItem(bridge.name))
            self.bridge_table.setItem(row, 2, QTableWidgetItem(bridge.ip_addr))
            row += 1

    def add_bridge(self):
        dlg_add_bridge = BridgeAddEdit(self, dlg_type='add')
        dlg_add_bridge.resize(400, 200)
        dlg_add_bridge.show()

    def edit_bridge(self):
        curr_row = self.bridge_table.currentRow()   
        if curr_row != -1:
            bridge_id = self.bridge_table.item(curr_row, 0).text()   
            dlg_edit_bridge = BridgeAddEdit(self, dlg_type='edit', bridge_id=bridge_id)
            dlg_edit_bridge.resize(400, 200)
            dlg_edit_bridge.show()
        
    def del_bridge(self, caller=None, value=0):
        curr_row = self.bridge_table.currentRow()
        if  curr_row != -1:
            if caller == False:
                bridge_id = int(self.bridge_table.item(self.bridge_table.currentRow(), 3).text())
                self.bridge_choicebox.set_msg('Are you sure you want to delete this bridge?')
                self.bridge_choicebox.set_return_func(self.del_bridge, bridge_id)
                self.bridge_choicebox.show()
                
        if caller == 'yes':
            bridge_id = value
            hue_util = HueUtilities()
            result = hue_util.delete_bridge(bridge_id)
            if result['status'] == 'success':
                self.msg_label.setText(result['message'])
                self.bridge_choicebox.hide()
                self.fill_bridge_table()
            elif result['status'] == 'error':
                self.msg_label.setText(result['message'])
                self.msg_label.setStyleSheet('color: red')
                self.bridge_choicebox.hide()
                
        elif caller == 'no':
            self.bridge_choicebox.hide()


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


        