from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout)
from PySide6.QtGui import Qt

from ui.widgets import YesNoBox, LogViewer, CircleIndicatorWidget
from ui.utilities import get_icon_obj
from system.hub import HubManger, HubSocket
from system.signals import Signal


class SettingsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.setLayout(self.main_layout)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.hubs_tab = HubsTab()
        self.general_tab = QWidget()
        self.tab_widget.addTab(self.hubs_tab, "Hubs")
        self.tab_widget.addTab(self.general_tab, "General")

class HubsTab(QWidget):
    def __init__(self):
        super().__init__()
        signal = Signal()
        self.socket = HubSocket()
        self.current_hub = None
        self.current_db_hub = None
        self.tab_hub_layout = QVBoxLayout()
        self.setLayout(self.tab_hub_layout)
        
        connect_layout = QHBoxLayout()
        btn_connect_hub = QPushButton('Connect to Hub')
        btn_connect_hub.clicked.connect(self.connect_hub)
        btn_test_hub = QPushButton('Test Hub')
        btn_test_hub.clicked.connect(self.test_socket)
        hub_indicator = CircleIndicatorWidget()
        connect_layout.addWidget(btn_connect_hub)
        connect_layout.addWidget(btn_test_hub)
        connect_layout.addWidget(hub_indicator)
        connect_layout.addStretch()

        hub_layout = QHBoxLayout()
        hub_Vlayout = QVBoxLayout()
        self.hub_combo = QComboBox()
        self.hub_combo.activated.connect(self.hub_changed)
        self.hub_db_combo = QComboBox()
        self.hub_db_combo.activated.connect(self.hub_db_changed)
        
        form_combo_layout = QFormLayout()
        form_combo_layout.addRow("Hub", self.hub_combo)
        form_combo_layout.addRow("Database Hub", self.hub_db_combo)
        
        hub_Vlayout.addLayout(form_combo_layout)
        hub_layout.addLayout(hub_Vlayout)
        hub_layout.addStretch()

        list_btn_layout = QHBoxLayout()
        btn_add_hub = QPushButton('Add hub')
        btn_add_hub.clicked.connect(self.add_hub)
        btn_add_hub.setIcon(get_icon_obj('plus-circle'))
        btn_edit_hub = QPushButton('Edit hub')
        btn_edit_hub.clicked.connect(self.edit_hub)
        btn_edit_hub.setIcon(get_icon_obj('pencil'))
        btn_del_hub = QPushButton('Delete hub')
        btn_del_hub.clicked.connect(self.del_hub)
        btn_del_hub.setIcon(get_icon_obj('cross-circle'))
        list_btn_layout.addWidget(btn_add_hub)
        list_btn_layout.addWidget(btn_edit_hub)
        list_btn_layout.addWidget(btn_del_hub)
        list_btn_layout.addStretch()
        
        hub_msgbox_layout = QHBoxLayout()
        self.hub_msgbox = YesNoBox()
        hub_msgbox_layout.addWidget(self.hub_msgbox)
        hub_msgbox_layout.addStretch()
        
        hub_tbl_layout = QHBoxLayout()
        self.hub_table = QTableWidget()
        self.hub_table.setMinimumWidth(450)
        hub_tbl_layout.addWidget(self.hub_table)
        hub_tbl_layout.addStretch()

        hub_msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        hub_msg_layout.addWidget(self.msg_label)
        hub_msg_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        
        log_layout = QHBoxLayout()
        self.log_viewer = LogViewer()
        log_layout.addWidget(self.log_viewer)
        log_layout.addStretch()

        self.tab_hub_layout.addLayout(connect_layout)
        self.tab_hub_layout.addLayout(hub_layout)
        self.tab_hub_layout.addLayout(list_btn_layout)
        self.tab_hub_layout.addLayout(hub_msgbox_layout)
        self.tab_hub_layout.addLayout(hub_tbl_layout)
        self.tab_hub_layout.addLayout(msg_layout)
        self.tab_hub_layout.addLayout(log_layout)
        self.tab_hub_layout.addStretch()

        self.hub_msgbox.hide()
        self.log_viewer.hide()

        signal.connect('hub_mgr_ui', self.update_log)

        
        
    def connect_hub(self):
        self.socket.connect_socket()
        
    def test_socket(self):
        self.socket.send('A message!!!')

    def showEvent(self, event):
        self.fill_hub_table()
        self.fill_hub_combos()

    def fill_hub_combos(self):
        hub_mgr = HubManger()
        self.hub_combo.clear()
        self.hub_db_combo.clear()
        hub_list = hub_mgr.get_hub_list()
        for hub in hub_list:
            self.hub_combo.addItem(hub['name'], hub['id'])
            self.hub_db_combo.addItem(hub['name'], hub['id'])
        self.current_hub = hub_mgr.get_current_hub()
        self.current_db_hub = hub_mgr.get_current_db_hub()
        self.hub_combo.setCurrentIndex(self.hub_combo.findData(self.current_hub['id']))
        self.hub_db_combo.setCurrentIndex(self.hub_db_combo.findData(self.current_db_hub['id']))

        
    def fill_hub_table(self):
        self.hub_table.clear()
        self.hub_table.setColumnCount(3)
        self.hub_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hub_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.hub_table.setHorizontalHeaderLabels(['Name', 'IP Address', 'ID'])
        #self.hub_table.horizontalHeader().setStretchLastSection(True)
        hub_conn = HubManger()
        hub_list = hub_conn.get_hub_list()
        self.hub_table.setRowCount(len(hub_list))
        for index, hub in enumerate(hub_list):
            self.hub_table.setItem(index, 0, QTableWidgetItem(hub['name']))
            self.hub_table.setItem(index, 1, QTableWidgetItem(hub['ip_addr']))
            self.hub_table.setItem(index, 2, QTableWidgetItem(str(hub['id'])))
            
                        
    def hub_changed(self, index):
        reply = QMessageBox.question(None, "Question", "Are you sure you want to change the Hub?", 
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            hub_mgr = HubManger()
            hub_id = self.hub_combo.currentData()
            result_dict = hub_mgr.set_current_hub(hub_id)
            self.msg_label.setText(result_dict['message'])
            if result_dict['status'] == 'error':
                self.msg_label.setStyleSheet('color: red')
            elif result_dict['status'] == 'success':
                self.msg_label.setStyleSheet('color: green')
        else:
            self.hub_combo.setCurrentIndex(self.hub_combo.findData(self.current_hub['id']))
        print('Index:', index)

    def hub_db_changed(self, index):
        reply = QMessageBox.question(None, "Question", "Are you sure you want to change the Database Hub?", 
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            hub_mgr = HubManger()
            hub_id = self.hub_db_combo.currentData()
            result_dict = hub_mgr.set_current_db_hub(hub_id)
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
                hub_id = int(self.hub_table.item(self.hub_table.currentRow(), 2).text())
                self.hub_msgbox.set_msg('Are you sure you want to delete this hub?')
                self.hub_msgbox.set_return_func(self.del_hub, hub_id)
                self.hub_msgbox.show()
                
        if caller == 'yes':
            hub_id = value
            hub_mgr = HubManger()
            result = hub_mgr.delete_hub(hub_id)
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

    def update_log(self, sender, msg_dict):
        self.log_viewer.update_log(msg_dict)
       
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
        
class GeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        general_tab_layout = QVBoxLayout()
        self.setLayout(self.general_tab_layout)
