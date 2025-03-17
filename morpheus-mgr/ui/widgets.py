from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QComboBox, QDialog,
                               QLineEdit, QCheckBox, QFrame, QMessageBox, QGroupBox, QFormLayout, QTextEdit)
from PySide6.QtGui import Qt, QPainter, QColor, QBrush

class LogMsgBox(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.html_list = []
        self.setMinimumHeight(150)
        layout = QVBoxLayout()
        
        txt_layout = QHBoxLayout()
        self.txt_edit = QTextEdit()
        self.txt_edit.setReadOnly(True)
        self.txt_edit.setStyleSheet("background-color: black;")
        txt_layout.addWidget(self.txt_edit)
        
        btn_layout = QHBoxLayout()
        btn_close = QPushButton('Close')
        btn_close.clicked.connect(self.hide)
        btn_layout.addWidget(btn_close)
        btn_layout.addStretch()
        
        
        layout.addLayout(txt_layout)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def set_msg(self, msg_dict):
        self.show()
        if msg_dict['status'] == 'error':
            self.html_list.append('<li style="color:red;">' + msg_dict['message'] + '</li>')
        elif msg_dict['status'] == 'info':
            self.html_list.append('<li style="color:aqua;">' + msg_dict['message'] + '</li>')
        elif msg_dict['status'] == 'success':
            self.html_list.append('<li style="color:lawngreen;">' + msg_dict['message'] + '</li>')
        
        html = '<ul style="list-style-type:none;">' + ''.join(self.html_list) + '</ul>'

        self.txt_edit.setHtml(html)

    def clear_msg(self):
        self.html = ''
        self.txt_edit.clear()

    

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

class CircleIndicatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Green Circle")
        self.setFixedSize(25, 25)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set brush color to green
        brush = QBrush(QColor(0, 255, 0))
        painter.setBrush(brush)

        # Draw the circle, centered in the widget
        diameter = min(self.width(), self.height())
        painter.drawEllipse(self.width()/2 - diameter/2, self.height()/2 - diameter/2, diameter, diameter)


        
