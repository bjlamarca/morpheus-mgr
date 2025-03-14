from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout, QTextEdit)
from PySide6.QtGui import Qt

class LogMsgBox(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.html = ''
        self.setFixedHeight(100)
        layout = QVBoxLayout()
        self.txt_edit = QTextEdit()
        layout.addWidget(self.txt_edit)
        self.setLayout(layout)

    def set_msg(self, msg_dict):
        if msg_dict['type'] == 'error':
            self.html = self.html + '<p style="color:red;">' + msg_dict['msg'] + '</p>'
        elif msg_dict['type'] == 'info':
            self.html = self.html + '<p style="color:blue;">' + msg_dict['msg'] + '</p>'
        elif msg_dict['type'] == 'success':
            self.html = self.html + '<p style="color:green;">' + msg_dict['msg'] + '</p>'
        
        self.txt_edit.setHtml(self.html)

    

class YesNoBox(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        layout = QVBoxLayout()
        self.lbl_msg = QLabel()
        layout.addWidget(self.lbl_msg)
        btn_layout = QHBoxLayout()
        btn_yes = QPushButton('Yes')
        btn_yes.clicked.connect(lambda: self.return_func('yes', self.value))
        btn_no = QPushButton('No')
        btn_no.clicked.connect(lambda: self.return_func('no', self.value))
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        self.setLayout(layout)

    def set_msg(self, msg):
        self.lbl_msg.setText(msg)

    def set_return_func(self, func, value=0):
        self.return_func = func
        self.value = value

        
