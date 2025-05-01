import time, threading
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame,
                             QGroupBox, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QTableWidget, 
                             QTableWidgetItem, QCheckBox, QTextEdit, QHeaderView)
from PySide6.QtGui import Qt, QPainter, QColor, QBrush, QFont, QPixmap, QPen, QPalette
from PySide6.QtCore import QRect
from PySide6.QtWebEngineWidgets import QWebEngineView
from system.signals import Signal



class StatusBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.msg_num = 1
        #signal = Signal()
        self.setMinimumHeight(150)
        self.msg_lbl = QLabel()
        self.msg_id_lbl = QLabel()
        V_layout = QVBoxLayout()
        H_layout = QHBoxLayout()
        H_layout.addWidget(self.msg_lbl)
        V_layout.addStretch()
        V_layout.addLayout(H_layout)
        self.setLayout(V_layout)
        #signal.connect('hue_mgr', self.msg_update)

    def set_msg(self, msg_dict, clear_time=10):
        self.clear_time = clear_time
        self.msg_num = self.msg_num + 1
        self.msg_id_lbl.setText(str(self.msg_num))
        if msg_dict['type'] == 'message':
            if msg_dict['status'] == 'clear':
                self.msg_lbl.clear()
            if msg_dict['status'] == 'error':
                text_color = 'red'
            elif msg_dict['status'] == 'info':
                text_color = 'aqua'
            elif msg_dict['status'] == 'success':
                text_color = 'lawngreen'
            elif msg_dict['status'] == 'warning':
                text_color = 'orange'
            else:
               text_color = 'white'
           
        self.msg_lbl.setStyleSheet("QLabel { color : " + text_color + "; }")
        self.msg_lbl.setText(str(msg_dict['message']))
        if self.clear_time > 0:
            thread = threading.Thread(target=self.clear_msg)
            thread.daemon = True
            thread.start()

    def msg_update(self, sender, msg):
        self.msg_lbl.setText(str(msg))

    def clear_msg(self):
        time.sleep(self.clear_time)
        if self.msg_id_lbl.text() == str(self.msg_num):
            self.msg_lbl.clear()
            self.msg_id_lbl.clear()

class LogViewer(QGroupBox):
    def __init__(self):
        super().__init__()
        self.log = []
        self.setTitle('Log Viewer')
        main_layout = QVBoxLayout() 
        log_tbl_layout = QHBoxLayout()
        self.log_tbl = QTableWidget()
        log_tbl_layout.addWidget(self.log_tbl)
        btn_layout = QHBoxLayout()
        btn_close = QPushButton('Close')
        btn_close.clicked.connect(self.hide)
        btn_layout.addWidget(btn_close)
        main_layout.addLayout(log_tbl_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def update_log(self, msg_dict):
        if msg_dict['status'] == 'clear':
            self.log = []
            self.log_tbl.clear()
            self.show()
        else:
            self.log.append(msg_dict.copy())
            self.log_tbl.clear()
            self.log_tbl.verticalHeader().setVisible(False)
            self.log_tbl.horizontalHeader().setVisible(False)
            self.log_tbl.setColumnCount(1)
            #self.log_tbl.setColumnWidth(0, 350)
            header = self.log_tbl.horizontalHeader()
            #header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive) # Allows interactive resizing of other columns
            header.setStretchLastSection(True)
            self.log_tbl.setRowCount(len(self.log))
            for index, logitem in enumerate(self.log):
                if logitem['status'] == 'error':
                    row_color = QColor('red')
                elif logitem['status'] == 'warning':
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
            
class ChoiceBox(QGroupBox):
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
        #pen = QPen(QColor("red"))
        # pen.setWidth(3)
        # self.line = self.scene.addLine(self.pos, 60, 70, 100, pen)
        text_item = QGraphicsTextItem(self.text)
        text_item.setPos(-10, self.pos)
        self.scene.addItem(text_item)
        
        self.update()
        self.pos += 20