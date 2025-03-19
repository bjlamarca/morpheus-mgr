from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame,
                             QGroupBox, QGraphicsView, QGraphicsScene, QGraphicsTextItem)
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

        print('LogMsgBox: ', msg_dict)
        self.txt_edit.setText(html)

    def msg_update(self, sender, msg):
        print('LogMsgBox: ', msg)
        self.txt_edit.setText(str(msg))

class Paint(QWidget):
        def __init__(self):
            super().__init__()
            print('LogViewer init')
            main_layout = QVBoxLayout()
            self.lbl = QLabel()
            canvas = QPixmap(400, 300)
            canvas.fill(Qt.white)
            self.lbl.setPixmap(canvas)
            main_layout.addWidget(self.lbl)
            self.setLayout(main_layout)
            self.text = "Hello, I am Morpheus!"
    
        def paintEvent(self, event):
            print('LogViewer paintEvent')
            painter = QPainter(self)
            painter.setPen(QColor(255, 255, 255))
            font = QFont()
            font.setPointSize(20)
            painter.setFont(font)
            text_rect = QRect(10, 10, 380, 180)
            painter.drawText(text_rect, Qt.AlignCenter, "Hello, I am Morpheus!")
            painter.end()

            # pen = QPen(QColor("red"))
            # pen.setWidth(3)
            # self.line = self.scene.addLine(10, 10, 10, 100, pen)
    
            # Calculate text rectangle to center text
            text_rect = QRect(0, 0, self.width(), self.height())
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.text)


class LogViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.pos = 10
        self.text = "Hello, I am Morpheus!"
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Create a line
        pen = QPen(QColor("red"))
        pen.setWidth(3)
        self.line = self.scene.addLine(10, 10, 10, 100, pen)
        text_item = QGraphicsTextItem(self.text)
        self.scene.addItem(text_item)

    def update_text(self, text):
        self.text = text
        print('Text: ', self.text)
        pen = QPen(QColor("red"))
        pen.setWidth(3)
        self.line = self.scene.addLine(self.pos, 60, 70, 100, pen)
        text_item = QGraphicsTextItem(self.text)
        self.scene.addItem(text_item)
        self.update()
        self.pos += 5
    

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


        
