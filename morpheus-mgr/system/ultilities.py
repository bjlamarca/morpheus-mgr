
import sys
from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QFile, QTextStream

BASE_DIR = str(Path(__file__).resolve().parent.parent)

def get_icon_obj(icon):
    path = BASE_DIR + '\\files\\graphics\\' + icon + '.png'
    return QIcon(QPixmap(path))

def get_pix_obj(icon):
    path = BASE_DIR + '\\files\\graphics\\' + icon + '.png'
    return QPixmap(path)
    

def load_stylesheet():
    print('Base dir:', BASE_DIR)
    qss_file = QFile(BASE_DIR + '\\files\\style\\Combinear.qss')
    if not qss_file.open(QFile.ReadOnly | QFile.Text):
        print("Error opening QSS file")
        sys.exit(1)
    qss_stream = QTextStream(qss_file)
    qss_content = qss_stream.readAll()
    return qss_content