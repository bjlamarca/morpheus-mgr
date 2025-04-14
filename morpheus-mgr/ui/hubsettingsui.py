from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout, QHeaderView)
from PySide6.QtGui import Qt

from ui.widgets import YesNoBox, LogViewer, CircleIndicatorWidget
from ui.utilities import get_icon_obj
from system.hub import HubManger, HubSocket
from system.signals import Signal


class HubSettingsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        signal = Signal()
        self.socket = HubSocket()
        self.hub_mgr = HubManger() 
        self.current_hub = None
        self.current_db_hub = None
        
        #### Connect group box
        connect_grpbox = QGroupBox("Hub Connection")
        #connect_grpbox.setStyleSheet("QGroupBox { font-weight: bold; }")
        connect_grpbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        connect_grid_layout = QGridLayout()
        hub_lbl = QLabel('Hub:')
        self.hub_indicator = CircleIndicatorWidget()
        self.hub_combo = QComboBox()
        self.hub_combo.setMinimumWidth(100)
        self.hub_combo.activated.connect(self.hub_changed)
        db_label = QLabel('Database:')
        self.db_indicator = CircleIndicatorWidget()
        self.hub_db_combo = QComboBox()
        self.hub_db_combo.setMinimumWidth(100)
        self.hub_db_combo.activated.connect(self.hub_db_changed)
        btn_connect_hub = QPushButton('Connect to Hub')
        btn_connect_hub.clicked.connect(self.connect_hub)
        btn_disconnect_hub = QPushButton('Disconnect Hub')
        btn_disconnect_hub.clicked.connect(self.disconnect_hub)
        btn_test_hub = QPushButton('Test Hub')
        btn_test_hub.clicked.connect(self.test_socket)
        connect_grid_layout.setColumnStretch(0, 0)
        connect_grid_layout.setColumnStretch(1, 0)
        connect_grid_layout.setColumnStretch(2, 0)
        connect_grid_layout.addWidget(hub_lbl, 0, 0, 1, 1)
        connect_grid_layout.addWidget(self.hub_indicator, 0, 1, 1, 1)
        connect_grid_layout.addWidget(self.hub_combo, 0, 2, 1, 1)
        connect_grid_layout.addWidget(db_label, 1, 0, 1, 1)
        connect_grid_layout.addWidget(self.db_indicator, 1, 1, 1, 1)
        connect_grid_layout.addWidget(self.hub_db_combo, 1, 2, 1, 1)
        connect_grid_layout.addWidget(btn_connect_hub, 2, 0, 1, 3)
        connect_grid_layout.addWidget(btn_disconnect_hub, 3, 0, 1, 3)
        connect_grid_layout.addWidget(btn_test_hub, 4, 0, 1, 3)
        connect_grpbox.setLayout(connect_grid_layout)
        #### End Connect group box

        #### Hub list group box
        hub_list_grpbox = QGroupBox('Hubs')
        list_btn_layout = QGridLayout()
        btn_add_hub = QPushButton('Add hub')
        btn_add_hub.clicked.connect(self.add_hub)
        btn_add_hub.setIcon(get_icon_obj('plus-circle'))
        btn_edit_hub = QPushButton('Edit hub')
        btn_edit_hub.clicked.connect(self.edit_hub)
        btn_edit_hub.setIcon(get_icon_obj('pencil'))
        btn_del_hub = QPushButton('Delete hub')
        btn_del_hub.clicked.connect(self.del_hub)
        btn_del_hub.setIcon(get_icon_obj('cross-circle'))
        list_btn_layout.addWidget(btn_add_hub, 0, 0, 1, 1)
        list_btn_layout.addWidget(btn_edit_hub, 0, 1, 1, 1)
        list_btn_layout.addWidget(btn_del_hub, 0, 2, 1, 1)
        
        hub_msgbox_layout = QHBoxLayout()
        self.hub_msgbox = YesNoBox()
        hub_msgbox_layout.addWidget(self.hub_msgbox)
        hub_msgbox_layout.addStretch()
        
        hub_tbl_layout = QHBoxLayout()
        self.hub_table = QTableWidget()
        hub_tbl_header = self.hub_table.horizontalHeader()
        hub_tbl_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive) # Allows manual resizing
        hub_tbl_header.setStretchLastSection(True) # Last section stretches to fill space
        self.hub_table.setMinimumWidth(375)
        #self.hub_table.setMinimumHeight(400)
        hub_tbl_layout.addWidget(self.hub_table)
        hub_tbl_layout.addStretch()
        
        hub_msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        hub_msg_layout.addWidget(self.msg_label)
        hub_msg_layout.addStretch()
        
        hub_list_layout = QVBoxLayout()
        hub_list_layout.addLayout(list_btn_layout)
        hub_list_layout.addLayout(hub_msgbox_layout)
        hub_list_layout.addLayout(hub_tbl_layout)    
        
        hub_list_grpbox.setLayout(hub_list_layout)

        #### End Hub list group box

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        
        #### Log viewer
        log_layout = QHBoxLayout()
        self.log_viewer = LogViewer()
        log_layout.addWidget(self.log_viewer)
        log_layout.addStretch()
        
        #### Main window layout
        tab_grid_layout = QGridLayout()
        tab_grid_layout.addWidget(connect_grpbox, 0, 0, 1, 1)
        tab_grid_layout.addWidget(hub_list_grpbox, 1, 0, 1, 3)
        tab_grid_layout.addWidget(self.log_viewer, 2, 0, 1, 3)
        tab_V_layout = QVBoxLayout()
        tab_V_layout.addLayout(tab_grid_layout)
        tab_V_layout.addStretch()    
        tab_H_layout = QHBoxLayout()
        tab_H_layout.addLayout(tab_V_layout)
        tab_H_layout.addStretch()

        self.setWindowTitle("Hub Settings")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.addLayout(tab_H_layout)
        self.setLayout(self.main_layout)
        
        self.hub_msgbox.hide()
        #self.log_viewer.hide()
        
        signal.connect('hub_mgr_ui', self.receive_signals)
        signal.connect('system', self.receive_signals)
        self.hub_mgr.get_db_status('hub_mgr_ui')
        self.socket.get_status('hub_mgr_ui')
        
        self.fill_hub_table()
        self.fill_hub_combos()

    def showEvent(self, event):
        pass

    def receive_signals(self, sender, msg_dict):
        if msg_dict['area'] == 'system':
            if msg_dict['type'] == 'update':
                if msg_dict['item'] == 'hub_db_connect':
                    if msg_dict['value'] == 'connected':
                        self.db_indicator.set_color('green')
                    elif msg_dict['value'] == 'disconnected':
                        self.db_indicator.set_color('grey')
                    elif msg_dict['value'] == 'error':
                        self.db_indicator.set_color('red')
                elif msg_dict['item'] == 'hub_connect':
                    if msg_dict['value'] == 'connected':
                        self.hub_indicator.set_color('green')
                    elif msg_dict['value'] == 'disconnected':
                        self.hub_indicator.set_color('grey')
                    elif msg_dict['value'] == 'error':
                        self.hub_indicator.set_color('red')
            elif msg_dict['type'] == 'message':
                self.log_viewer.update_log(msg_dict)
            
        
        #self.log_viewer.update_log(msg_dict)      
        
    def connect_hub(self):
        self.socket.connect_socket('hub_mgr_ui')
        self.socket.get_status('hub_mgr_ui')
        
    def disconnect_hub(self):
        self.socket.disconnect_socket('hub_mgr_ui')
        self.socket.get_status('hub_mgr_ui')
        
    def test_socket(self):
        #self.socket.send('A message!!!')
        self.hub_mgr.get_db_status('hub_mgr_ui')
        self.socket.get_status('hub_mgr_ui')


    def fill_hub_combos(self):
        self.hub_combo.clear()
        self.hub_db_combo.clear()
        hub_list = self.hub_mgr.get_hub_list()
        for hub in hub_list:
            self.hub_combo.addItem(hub['name'], hub['id'])
            self.hub_db_combo.addItem(hub['name'], hub['id'])
        self.current_hub = self.hub_mgr.get_current_hub()
        self.current_db_hub = self.hub_mgr.get_current_db_hub()
        self.hub_combo.setCurrentIndex(self.hub_combo.findData(self.current_hub['id']))
        self.hub_db_combo.setCurrentIndex(self.hub_db_combo.findData(self.current_db_hub['id']))

        
    def fill_hub_table(self):
        self.hub_table.clear()
        self.hub_table.setColumnCount(3)
        self.hub_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hub_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.hub_table.setHorizontalHeaderLabels(['ID', 'Name', 'IP Address'])
        #self.hub_table.horizontalHeader().setStretchLastSection(True)
        hub_conn = HubManger()
        hub_list = hub_conn.get_hub_list()
        self.hub_table.setRowCount(len(hub_list))
        self.hub_table.setColumnWidth(0, 50)
        self.hub_table.setColumnWidth(1, 150)
        self.hub_table.verticalHeader().setVisible(False)
        for index, hub in enumerate(hub_list):
            self.hub_table.setItem(index, 0, QTableWidgetItem(str(hub['id'])))
            self.hub_table.setItem(index, 1, QTableWidgetItem(hub['name']))
            self.hub_table.setItem(index, 2, QTableWidgetItem(hub['ip_addr']))
            
                        
    def hub_changed(self, index):
        reply = QMessageBox.question(None, "Question", "Are you sure you want to change the Hub?", 
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            hub_id = self.hub_combo.currentData()
            result_dict = self.hub_mgr.set_current_hub(hub_id)
            self.msg_label.setText(result_dict['message'])
            if result_dict['status'] == 'error':
                self.msg_label.setStyleSheet('color: red')
            elif result_dict['status'] == 'success':
                self.msg_label.setStyleSheet('color: green')
        else:
            self.hub_combo.setCurrentIndex(self.hub_combo.findData(self.current_hub['id']))
       
    def hub_db_changed(self, index):
        reply = QMessageBox.question(None, "Question", "Are you sure you want to change the Database Hub?", 
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            hub_id = self.hub_db_combo.currentData()
            result_dict = self.hub_mgr.set_current_db_hub(hub_id)
            self.msg_label.setText(result_dict['message'])
            if result_dict['status'] == 'error':
                self.msg_label.setStyleSheet('color: red')
            elif result_dict['status'] == 'success':
                self.msg_label.setStyleSheet('color: green')
        else:
            self.hub_combo.setCurrentIndex(self.hub_combo.findData(self.current_hub['id']))

    def add_hub(self):
        dlg_add_hub = HubAddEdit(self, dlg_type='add')
        dlg_add_hub.resize(400, 200)
        dlg_add_hub.show()

    def edit_hub(self):
        curr_row = self.hub_table.currentRow()   
        if curr_row != -1:
            hub_id = int(self.hub_table.item(curr_row, 2).text())
            dlg_edit_hub = HubAddEdit(self, dlg_type='edit', hub_id=hub_id)
            dlg_edit_hub.resize(400, 200)
            dlg_edit_hub.show()
        
    def del_hub(self, caller=None, value=0):
        curr_row = self.hub_table.currentRow()
        if  curr_row != -1:
            if caller == False:
                hub_id = int(self.hub_table.item(self.hub_table.currentRow(), 0).text())
                self.hub_msgbox.set_msg('Are you sure you want to delete this hub?')
                self.hub_msgbox.set_return_func(self.del_hub, hub_id)
                self.hub_msgbox.show()
                
        if caller == 'yes':
            hub_id = value
            result = self.hub_mgr.delete_hub(hub_id)
            if result['status'] == 'success':
                self.msg_label.setText(result['message'])
                self.hub_msgbox.hide()
                self.fill_hub_table()
            elif result['status'] == 'error':
                self.msg_label.setText(result['message'])
                self.msg_label.setStyleSheet('color: red')
                self.hub_msgbox.hide()
                
        elif caller == 'no':
            self.hub_msgbox.hide()

    
       
class HubAddEdit(QDialog):
    def __init__(self, parent=None, dlg_type=None, hub_id=None):
        super().__init__(parent)
        self.dlg_type = dlg_type
        self.hub_id = hub_id
        if self.dlg_type == 'add':
            self.setWindowTitle("Add Hub")
        elif self.dlg_type == 'edit':   
            self.setWindowTitle("Edit Hub")
        
        hub_layout = QVBoxLayout(self)
        
        self.ledit_name = QLineEdit()
        self.ledit_ipaddr = QLineEdit()
              
        form_layout = QFormLayout()
        form_layout.addRow("Name", self.ledit_name)
        form_layout.addRow("IP Address", self.ledit_ipaddr)
    
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.close)
        if self.dlg_type == 'add':
            self.btn_add_edit = QPushButton('Add')
            self.btn_add_edit.clicked.connect(self.add_hub)
        elif self.dlg_type == 'edit':
            self.btn_add_edit = QPushButton('Save')
            self.btn_add_edit.clicked.connect(self.edit_hub)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_add_edit)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        hub_layout.addLayout(form_layout)
        hub_layout.addLayout(btn_layout)
        hub_layout.addLayout(msg_layout)
        hub_layout.addStretch()

        if self.dlg_type == 'edit':
            ser_conn = HubManger()
            hub = ser_conn.get_hub_info(self.hub_id)
            self.ledit_name.setText(hub['name'])
            self.ledit_ipaddr.setText(hub['ip_addr'])
           
    def add_hub(self):
        serv_conn = HubManger()
        responce = serv_conn.add_hub(self.ledit_name.text(), self.ledit_ipaddr.text(),)
        if responce['status'] == 'success':
            self.parent().fill_hub_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")


    def edit_hub(self):
        serv_conn = HubManger()
        responce = serv_conn.edit_hub(self.ledit_name.text(), self.ledit_ipaddr.text(), self.hub_id)
        if responce['status'] == 'success':
            self.parent().fill_hub_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")
        

