try:
	from PySide6 import QtWidgets, QtGui, QtCore
except:
	from PySide2 import QtWidgets, QtGui, QtCore
	
import os

def load_icons_from_folder(folder_path) :
    if not os.path.exists(folder_path) :
        return []
    exts = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    return sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(exts)
    ])

def load_and_scale_pixmap(path, width, height) :
    pix = QtGui.QPixmap(path)
    return pix.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)