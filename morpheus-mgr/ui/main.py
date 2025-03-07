from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenu, QGroupBox, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morpheus")
        
        
        

        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.websocket_grpbox = QGroupBox("Websocket")
        websocket_layout = QVBoxLayout()
        btn_connect = QPushButton("Connect")
        btn_connect.clicked.connect(self.connect_websocket)
        websocket_layout.addWidget(btn_connect)
        
        
        main_layout.addWidget(self.websocket_grpbox)


    def connect_websocket(self):
        pass