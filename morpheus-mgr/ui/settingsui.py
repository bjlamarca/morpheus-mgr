from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout)
from PySide6.QtGui import Qt

from ui.widgets import YesNoBox, LogViewer
from system.ultilities import get_icon_obj
from system.settings import ServerConnection


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
        super().__init__()
        self.tab_server_layout = QVBoxLayout()
        self.setLayout(self.tab_server_layout)
        
        server_layout = QVBoxLayout()


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
        
        self.tab_server_layout.addLayout(server_btn_layout)
        self.tab_server_layout.addLayout(server_msgbox_layout)
        self.tab_server_layout.addLayout(server_tbl_layout)
        self.tab_server_layout.addStretch()

        self.server_msgbox.hide()
        
    def showEvent(self, event):
        self.fill_server_table()
        
   
    def fill_server_table(self):
        self.server_table.clear()
        self.server_table.setColumnCount(4)
        self.server_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.server_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.server_table.setHorizontalHeaderLabels(['Name', 'IP Address'])
        #self.server_table.horizontalHeader().setStretchLastSection(True)
        server_conn = ServerConnection()
        server_list = server_conn.get_server_list()
        self.server_table.setRowCount(len(server_list))
        row = 0
        for server in server_list:
            self.server_table.setItem(row, 0, QTableWidgetItem(server.name))
            self.server_table.setItem(row, 1, QTableWidgetItem(server.ip_addr))
            self.server_table.setItem(row, 2, QTableWidgetItem(server.username))
            self.server_table.setItem(row, 3, QTableWidgetItem(str(server.id)))
            row += 1



    def add_server(self):
        dlg_add_server = serverAddEdit(self, dlg_type='add')
        dlg_add_server.resize(400, 200)
        dlg_add_server.show()

    def edit_server(self):
        curr_row = self.server_table.currentRow()   
        if curr_row != -1:
            server_id = self.server_table.item(curr_row, 3).text()   
            dlg_edit_server = serverAddEdit(self, dlg_type='edit', server_id=server_id)
            dlg_edit_server.resize(400, 200)
            dlg_edit_server.show()
        
    def del_server(self, caller=None, value=0):
        curr_row = self.server_table.currentRow()
        if  curr_row != -1:
            if caller == False:
                server_id = int(self.server_table.item(self.server_table.currentRow(), 3).text())
                self.server_msgbox.set_msg('Are you sure you want to delete this server?')
                self.server_msgbox.set_return_func(self.del_server, server_id)
                self.server_msgbox.show()
                
        if caller == 'yes':
            server_id = value
            hue_util = HueUtilities()
            result = hue_util.delete_server(server_id)
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
       

        
class GeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        general_tab_layout = QVBoxLayout()
        self.setLayout(self.general_tab_layout)
