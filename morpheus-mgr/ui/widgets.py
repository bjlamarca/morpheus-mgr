from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame,
                             QGroupBox, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QTableWidget, 
                             QTableWidgetItem, QCheckBox)
from PySide6.QtGui import Qt, QPainter, QColor, QBrush, QFont, QPixmap, QPen
from PySide6.QtCore import QRect
from PySide6.QtWebEngineWidgets import QWebEngineView
from system.signals import Signal



class LogMsgBox(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        signal = Signal()
        
        self.html_list = []
        self.setMinimumHeight(150)
        layout = QVBoxLayout()
        
        txt_layout = QHBoxLayout()
        self.txt_edit = QLineEdit()
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
        #signal.connect('hue_mgr', self.msg_update)

    def set_msg(self, msg_dict):
        if msg_dict['status'] == 'clear':
            self.txt_edit.clear()
        if msg_dict['status'] == 'error':
            self.html_list.append('<li style="color:red;">' + msg_dict['message'] + '</li>')
        elif msg_dict['status'] == 'info':
            self.html_list.append('<li style="color:aqua;">' + msg_dict['message'] + '</li>')
        elif msg_dict['status'] == 'success':
            self.html_list.append('<li style="color:lawngreen;">' + msg_dict['message'] + '</li>')
        
        html = '<ul style="list-style-type:none;">' + ''.join(self.html_list) + '</ul>'
        self.txt_edit.setText(html)

    def msg_update(self, sender, msg):
        self.txt_edit.setText(str(msg))



class LogViewer(QGroupBox):
    def __init__(self):
        super().__init__()
        self.log = []
        self.setTitle('Log Viewer')
        #self.setMinimumHeight(200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        log_tbl_layout = QHBoxLayout()
        self.log_tbl = QTableWidget()
        #self.log_tbl.setMinimumWidth(200)
        #self.log_tbl.setMinimumHeight(400)
        log_tbl_layout.addWidget(self.log_tbl)
        log_tbl_layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_close = QPushButton('Close')
        btn_close.clicked.connect(self.hide)
        btn_layout.addWidget(btn_close)
        btn_layout.addStretch()

        self.layout.addLayout(log_tbl_layout)
        self.layout.addLayout(btn_layout)
        self.layout.addStretch()

    def update_log(self, msg_dict):
        print('LogViewer: ', msg_dict)
        if msg_dict['status'] == 'clear':
            self.log = []
            self.log_tbl.clear()
            self.show()
        else:
            self.log.append(msg_dict.copy())
            #print('log: ', self.log)
        
            self.log_tbl.clear()
            self.log_tbl.verticalHeader().setVisible(False)
            self.log_tbl.horizontalHeader().setVisible(False)
            self.log_tbl.setColumnCount(1)
            self.log_tbl.setColumnWidth(0, 350)
            self.log_tbl.setRowCount(len(self.log))
            for index, logitem in enumerate(self.log):
                if logitem['status'] == 'error':
                    row_color = QColor('red')
                if logitem['status'] == 'warning':
                    row_color = QColor('orange')
                elif logitem['status'] == 'info':
                    row_color = QColor('aqua')
                elif logitem['status'] == 'success':
                    row_color = QColor('lawngreen')
                else:
                    row_color = QColor('white')
                    
                tbl_item = QTableWidgetItem(logitem['message'])
                tbl_item.setForeground(row_color)
                self.log_tbl.setItem(index, 0, tbl_item)
            self.show()
            

class LogViewerGraphics(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.pos = 20
        self.text = "Hello, I am Morpheus!"
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Create a line
        
        text_item = QGraphicsTextItem(self.text)
        text_item.setPos(-10, 10)
        self.scene.addItem(text_item)

    def update_text(self, text):
        self.text = text
        print('Text: ', self.text)
        #pen = QPen(QColor("red"))
        # pen.setWidth(3)
        # self.line = self.scene.addLine(self.pos, 60, 70, 100, pen)
        text_item = QGraphicsTextItem(self.text)
        text_item.setPos(-10, self.pos)
        self.scene.addItem(text_item)
        
        self.update()
        self.pos += 20
    

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
        self.setFixedSize(15, 15)
        self.color = 'grey'

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.color == 'grey':
            brush = QBrush(QColor(128, 128, 128))
        elif self.color == 'red':
            brush = QBrush(QColor(255, 0, 0))
        elif self.color == 'green':
            brush = QBrush(QColor(0, 255, 0))
        elif self.color == 'blue':
            brush = QBrush(QColor(0, 0, 255))
        elif self.color == 'yellow':
            brush = QBrush(QColor(255, 255, 0))
        elif self.color == 'orange':
            brush = QBrush(QColor(255, 165, 0))
        elif self.color == 'purple':
            brush = QBrush(QColor(128, 0, 128))

        # Set brush color to green
        
        painter.setBrush(brush)

        # Draw the circle, centered in the widget
        diameter = min(self.width(), self.height())
        diameter = diameter / 1.5
        painter.drawEllipse(self.width()/2 - diameter/2, self.height()/2 - diameter/2, diameter, diameter)


    def set_color(self, color):
        self.color = color
        self.update()

