
import sys
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QFile, QTextStream


def get_icon_obj(icon):
    path = 'C:\\Dev\\showdemon2\\showdemon\\files\\graphics\\' + icon + '.png'
    return QIcon(QPixmap(path))

def get_pix_obj(icon):
    path = 'C:\\Dev\\showdemon2\\showdemon\\files\\graphics\\' + icon + '.png'
    return QPixmap(path)
    

def load_stylesheet():
    qss_file = QFile('C:\\Dev\\showdemon2\\showdemon\\files\\style\\Combinear.qss')
    if not qss_file.open(QFile.ReadOnly | QFile.Text):
        print("Error opening QSS file")
        sys.exit(1)
    qss_stream = QTextStream(qss_file)
    qss_content = qss_stream.readAll()
    return qss_content