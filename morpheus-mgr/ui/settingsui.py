from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout)
from PySide6.QtGui import Qt

from ui.widgets import YesNoBox, LogViewer
from ui.utilities import get_icon_obj
from system.server import ServerManger


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

        self.servers_tab = ServersTab()
        self.general_tab = QWidget()
        self.tab_widget.addTab(self.servers_tab, "Servers")
        self.tab_widget.addTab(self.general_tab, "General")

class ServersTab(QWidget):
    def __init__(self):
        self.current_server = None
        self.current_db_server = None
        super().__init__()
        self.tab_server_layout = QVBoxLayout()
        self.setLayout(self.tab_server_layout)
        
        server_layout = QHBoxLayout()
        server_Vlayout = QVBoxLayout()
        self.server_combo = QComboBox()
        self.server_combo.activated.connect(self.server_changed)
        self.server_db_combo = QComboBox()
        self.server_db_combo.activated.connect(self.server_db_changed)
        
        form_combo_layout = QFormLayout()
        form_combo_layout.addRow("Server", self.server_combo)
        form_combo_layout.addRow("Database Server", self.server_db_combo)
        
        server_Vlayout.addLayout(form_combo_layout)
        server_layout.addLayout(server_Vlayout)
        server_layout.addStretch()

        list_btn_layout = QHBoxLayout()
        btn_add_server = QPushButton('Add server')
        btn_add_server.clicked.connect(self.add_server)
        btn_add_server.setIcon(get_icon_obj('plus-circle'))
        btn_edit_server = QPushButton('Edit server')
        btn_edit_server.clicked.connect(self.edit_server)
        btn_edit_server.setIcon(get_icon_obj('pencil'))
        btn_del_server = QPushButton('Delete server')
        btn_del_server.clicked.connect(self.del_server)
        btn_del_server.setIcon(get_icon_obj('cross-circle'))
        list_btn_layout.addWidget(btn_add_server)
        list_btn_layout.addWidget(btn_edit_server)
        list_btn_layout.addWidget(btn_del_server)
        list_btn_layout.addStretch()
        
        server_msgbox_layout = QHBoxLayout()
        self.server_msgbox = YesNoBox()
        server_msgbox_layout.addWidget(self.server_msgbox)
        server_msgbox_layout.addStretch()
        
        server_tbl_layout = QHBoxLayout()
        self.server_table = QTableWidget()
        self.server_table.setMinimumWidth(450)
        server_tbl_layout.addWidget(self.server_table)
        server_tbl_layout.addStretch()

        server_msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        server_msg_layout.addWidget(self.msg_label)
        server_msg_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        
        self.tab_server_layout.addLayout(server_layout)
        self.tab_server_layout.addLayout(list_btn_layout)
        self.tab_server_layout.addLayout(server_msgbox_layout)
        self.tab_server_layout.addLayout(server_tbl_layout)
        self.tab_server_layout.addLayout(msg_layout)
        self.tab_server_layout.addStretch()

        self.server_msgbox.hide()
        

    def showEvent(self, event):
        self.fill_server_table()
        self.fill_server_combos()

    def fill_server_combos(self):
        server_mgr = ServerManger()
        self.server_combo.clear()
        self.server_db_combo.clear()
        server_list = server_mgr.get_server_list()
        for server in server_list:
            self.server_combo.addItem(server['name'], server['id'])
            self.server_db_combo.addItem(server['name'], server['id'])
        self.current_server = server_mgr.get_current_server()
        self.current_db_server = server_mgr.get_current_db_server()
        self.server_combo.setCurrentIndex(self.server_combo.findData(self.current_server['id']))
        self.server_db_combo.setCurrentIndex(self.server_db_combo.findData(self.current_db_server['id']))

        
    def fill_server_table(self):
        self.server_table.clear()
        self.server_table.setColumnCount(3)
        self.server_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.server_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.server_table.setHorizontalHeaderLabels(['Name', 'IP Address', 'ID'])
        #self.server_table.horizontalHeader().setStretchLastSection(True)
        server_conn = ServerManger()
        server_list = server_conn.get_server_list()
        self.server_table.setRowCount(len(server_list))
        for index, server in enumerate(server_list):
            self.server_table.setItem(index, 0, QTableWidgetItem(server['name']))
            self.server_table.setItem(index, 1, QTableWidgetItem(server['ip_addr']))
            self.server_table.setItem(index, 2, QTableWidgetItem(str(server['id'])))
            
                        
    def server_changed(self, index):
        reply = QMessageBox.question(None, "Question", "Are you sure you want to change the Server?", 
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            server_mgr = ServerManger()
            server_id = self.server_combo.currentData()
            result_dict = server_mgr.set_current_server(server_id)
            self.msg_label.setText(result_dict['message'])
            if result_dict['status'] == 'error':
                self.msg_label.setStyleSheet('color: red')
            elif result_dict['status'] == 'success':
                self.msg_label.setStyleSheet('color: green')
        else:
            self.server_combo.setCurrentIndex(self.server_combo.findData(self.current_server['id']))
        print('Index:', index)

    def server_db_changed(self, index):
        reply = QMessageBox.question(None, "Question", "Are you sure you want to change the Database Server?", 
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            server_mgr = ServerManger()
            server_id = self.server_db_combo.currentData()
            result_dict = server_mgr.set_current_db_server(server_id)
            self.msg_label.setText(result_dict['message'])
            if result_dict['status'] == 'error':
                self.msg_label.setStyleSheet('color: red')
            elif result_dict['status'] == 'success':
                self.msg_label.setStyleSheet('color: green')
        else:
            self.server_combo.setCurrentIndex(self.server_combo.findData(self.current_server['id']))

    def add_server(self):
        dlg_add_server = ServerAddEdit(self, dlg_type='add')
        dlg_add_server.resize(400, 200)
        dlg_add_server.show()

    def edit_server(self):
        curr_row = self.server_table.currentRow()   
        if curr_row != -1:
            server_id = int(self.server_table.item(curr_row, 2).text())
            dlg_edit_server = ServerAddEdit(self, dlg_type='edit', server_id=server_id)
            dlg_edit_server.resize(400, 200)
            dlg_edit_server.show()
        
    def del_server(self, caller=None, value=0):
        curr_row = self.server_table.currentRow()
        if  curr_row != -1:
            if caller == False:
                server_id = int(self.server_table.item(self.server_table.currentRow(), 2).text())
                self.server_msgbox.set_msg('Are you sure you want to delete this server?')
                self.server_msgbox.set_return_func(self.del_server, server_id)
                self.server_msgbox.show()
                
        if caller == 'yes':
            server_id = value
            server_mgr = ServerManger()
            result = server_mgr.delete_server(server_id)
            if result['status'] == 'success':
                self.msg_label.setText(result['message'])
                self.server_msgbox.hide()
                self.fill_server_table()
            elif result['status'] == 'error':
                self.msg_label.setText(result['message'])
                self.msg_label.setStyleSheet('color: red')
                self.server_msgbox.hide()
                
        elif caller == 'no':
            self.server_msgbox.hide()
       
class ServerAddEdit(QDialog):
    def __init__(self, parent=None, dlg_type=None, server_id=None):
        super().__init__(parent)
        self.dlg_type = dlg_type
        self.server_id = server_id
        if self.dlg_type == 'add':
            self.setWindowTitle("Add Server")
        elif self.dlg_type == 'edit':   
            self.setWindowTitle("Edit Server")
        
        server_layout = QVBoxLayout(self)
        
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
            self.btn_add_edit.clicked.connect(self.add_server)
        elif self.dlg_type == 'edit':
            self.btn_add_edit = QPushButton('Save')
            self.btn_add_edit.clicked.connect(self.edit_server)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_add_edit)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        server_layout.addLayout(form_layout)
        server_layout.addLayout(btn_layout)
        server_layout.addLayout(msg_layout)
        server_layout.addStretch()

        if self.dlg_type == 'edit':
            ser_conn = ServerManger()
            server = ser_conn.get_server_info(self.server_id)
            self.ledit_name.setText(server['name'])
            self.ledit_ipaddr.setText(server['ip_addr'])
           
    def add_server(self):
        serv_conn = ServerManger()
        responce = serv_conn.add_server(self.ledit_name.text(), self.ledit_ipaddr.text(),)
        if responce['status'] == 'success':
            self.parent().fill_server_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")


    def edit_server(self):
        serv_conn = ServerManger()
        responce = serv_conn.edit_server(self.ledit_name.text(), self.ledit_ipaddr.text(), self.server_id)
        if responce['status'] == 'success':
            self.parent().fill_server_table()
            self.close()
        elif responce['status'] == 'error':
            self.msg_label.setText(responce['message'])
            self.msg_label.setStyleSheet("color: red")
        
class GeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        general_tab_layout = QVBoxLayout()
        self.setLayout(self.general_tab_layout)
