try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except :
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from . import util
import os
from functools import partial

BASE_DIR = os.path.dirname(__file__)
FACE_DIR = os.path.join(BASE_DIR, 'face_folder')

ICON_FOLDERS = {
    "Foundation" : "foundation_folder",
    "Eyeliner" : "eyeliner_folder",
    "Blush" : "blush_folder",
    "Eyeshadow" : "eyeshadow_folder",
    "Lip" : "lip_folder",
    "Hairstyle":  "hair_folder",
    "Clothes" : "clothes_folder",
    "Accessory" : "accessory_folder",
}

CATEGORY_TO_FOLDER = {
    "Foundation" : "foundation_folder",
    "Eyeliner" : "eyeliner_folder",      
    "Blush" : "cheek_folder",            
    "Eyeshadow" : "eyesColor_folder",    
    "Lip" : "lipsColor_folder",          
    "Hairstyle" : "hair_folder",         
    "Clothes" : "clothes_folder",        
    "Accessory" : "accessories_folder"     
}

CATEGORY_TO_LAYER = {
    "Foundation" : "Face",
    "Eyeliner" : "Eyes",
    "Blush" : "Cheek",
    "Eyeshadow" : "EyesColor",
    "Lip" : "LipsColor",
    "Hairstyle" : "Hair",
    "Clothes" : "Clothes",
    "Accessory" : "Accessories"
}

class MakeupUI(QtWidgets.QDialog) :
    def __init__(self, parent=None) :
        super().__init__(parent)

        self.setWindowTitle("Let's Do Makeup !")
        self.resize(800, 650)
        self.setStyleSheet('background-color: #c8bfe7;')

        self.preview_w = 650
        self.preview_h = 650
        self.layers = {layer: None for layer in CATEGORY_TO_LAYER.values()}

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)

        self.setup_face_view()
        self.setup_category_buttons()
        self.setup_right_panel()

        self.current_face_index = 1
        self.update_layer_image("Face", self.current_face_index)

    def setup_face_view(self) :
        self.faceScene = QtWidgets.QGraphicsScene()
        self.faceScene.setSceneRect(0, 0, self.preview_w, self.preview_h)

        self.faceView = QtWidgets.QGraphicsView(self.faceScene)
        self.faceView.setFixedSize(self.preview_w, self.preview_h)
        self.faceView.setStyleSheet('border: 3px solid #c8bfe7; background-color: white;')
        self.faceView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.faceView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.faceView.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.faceView.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.mainLayout.addWidget(self.faceView)

    def setup_category_buttons(self) :
        self.categoryFrame = QtWidgets.QFrame()
        self.categoryLayout = QtWidgets.QVBoxLayout(self.categoryFrame)
        self.categoryLayout.setSpacing(5)
        self.categoryLayout.setContentsMargins(10, 10, 10, 10)

        self.categoryButtons = ["Foundation", "Eyeliner", "Blush", "Eyeshadow", 
                                "Lip", "Hairstyle", "Clothes", "Accessory"]

        self.categoryGroup = QtWidgets.QButtonGroup(self)
        for i, name in enumerate(self.categoryButtons) :
            btn = QtWidgets.QPushButton(f"{i + 1}. {name}")
            btn.setCheckable(True)
            btn.setStyleSheet('''
                QPushButton {
                    color: black;
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 6px;
                    padding: 5px;
                }
                QPushButton:hover {
                    color: white;
                    background-color: #a59ebe;
                    border: 2px solid white;
                }
                QPushButton:checked {
                    color: white;
                    background-color: #8b7abf;
                    border: 2px solid white;
                    font-weight: bold;
                }
            ''')
            self.categoryGroup.addButton(btn, i)
            self.categoryLayout.addWidget(btn)

        self.categoryFrame.setFixedSize(160, 520)
        self.mainLayout.addWidget(self.categoryFrame)

    def setup_right_panel(self) :
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.rightLayout, stretch=2)

        self.gridOuterFrame = QtWidgets.QFrame()
        self.gridOuterFrame.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 2.2px solid black;
                border-radius: 10px;
            }
        ''')
        self.gridOuterLayout = QtWidgets.QVBoxLayout(self.gridOuterFrame)
        self.gridOuterLayout.setContentsMargins(10, 10, 10, 10)

        self.stack = QtWidgets.QStackedWidget()
        self.gridOuterLayout.addWidget(self.stack)

        for name in self.categoryButtons:
            folder_path = os.path.join(BASE_DIR, ICON_FOLDERS[name])
            page = self.createGridPage(name, folder_path)
            self.stack.addWidget(page)

        self.gridOuterFrame.setFixedSize(250, 590)
        self.stack.setStyleSheet('border-radius:6px;')
        self.rightLayout.addWidget(self.gridOuterFrame, alignment=QtCore.Qt.AlignCenter)

        self.nextAndBackButtonLayout = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("Back")
        self.nextButton = QtWidgets.QPushButton("Next")
        for btn in (self.backButton, self.nextButton):
            btn.setFixedSize(125, 40)
            btn.setStyleSheet('''
                QPushButton {
                    color: black;
                    background-color: white;
                    border: 2px solid black;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: white;
                    background-color: #a59ebe;
                    border: 2px solid black;
                }
            ''')
        self.nextAndBackButtonLayout.addWidget(self.backButton)
        self.nextAndBackButtonLayout.addWidget(self.nextButton)
        self.rightLayout.addLayout(self.nextAndBackButtonLayout)

        self.categoryGroup.buttons()[0].setChecked(True)
        self.categoryGroup.buttonClicked.connect(self.switchCategory)
        self.backButton.clicked.connect(self.goBack)
        self.nextButton.clicked.connect(self.goNext)
        self.updateNextBackButtons()

    def update_layer_image(self, layer_name, index_or_path) :
        if layer_name == "Face" and isinstance(index_or_path, int) :
            path = os.path.join(FACE_DIR, f"face_{index_or_path:02d}.png")
        else :
            path = index_or_path

        if not os.path.exists(path) :
            print(f"⚠️ Image not found: {path}")
            return

        pix = util.load_and_scale_pixmap(path, self.preview_w, self.preview_h)
        if self.layers[layer_name] :
            self.layers[layer_name].setPixmap(pix)
        else :
            item = QtWidgets.QGraphicsPixmapItem(pix)
            z_order = {
                "Face" : 0, "EyesColor" : 1, "Cheek" : 2, "LipsColor" : 3,
                "Eyes" : 4, "Clothes" : 5, "Hair" : 6, "Accessories" : 7
            }
            item.setZValue(z_order.get(layer_name, 0))
            self.faceScene.addItem(item)
            self.layers[layer_name] = item

    def createGridPage(self, category, folder_path) :
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        icons = util.load_icons_from_folder(folder_path)
        if not icons :
            label = QtWidgets.QLabel(f"No images found in {category}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(label)
            return widget

        layer_name = CATEGORY_TO_LAYER.get(category, None)
        num_columns = 2

        for i, icon_path in enumerate(icons) :
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(80, 80)
            btn.setIcon(QtGui.QIcon(icon_path))
            btn.setIconSize(QtCore.QSize(70, 70))
            btn.setStyleSheet('''
                QPushButton {
                    border: 2px solid black;
                    border-radius: 6px;
                    background-color: white;
                }
                QPushButton:hover {
                    border: 3px solid #a59ebe;
                    background-color: #f2e9ff;
                }
            ''')
            layout.addWidget(btn, i // num_columns, i % num_columns)

            if layer_name :
                if category == "Foundation" :
                    btn.clicked.connect(partial(self.update_layer_image, layer_name, i + 1))
                else :
                    real_folder = CATEGORY_TO_FOLDER.get(category)
                    real_path = os.path.join(BASE_DIR, real_folder, os.path.basename(icon_path))
                    btn.clicked.connect(partial(self.update_layer_image, layer_name, real_path))

        return widget

    def switchCategory(self, button) :
        index = self.categoryGroup.id(button)
        self.stack.setCurrentIndex(index)
        self.updateNextBackButtons()

    def goBack(self):
        index = self.stack.currentIndex()
        if index > 0 :
            self.stack.setCurrentIndex(index - 1)
            self.categoryGroup.buttons()[index - 1].setChecked(True)
        self.updateNextBackButtons()

    def goNext(self):
        index = self.stack.currentIndex()
        if index < self.stack.count() - 1 :
            self.stack.setCurrentIndex(index + 1)
            self.categoryGroup.buttons()[index + 1].setChecked(True)
        elif index == self.stack.count() - 1 :
            QtWidgets.QMessageBox.information(self, "Let's Do Makeup !", "FINISH")
        self.updateNextBackButtons()

    def updateNextBackButtons(self) :
        index = self.stack.currentIndex()
        count = self.stack.count()
        self.backButton.setEnabled(index > 0)
        self.nextButton.setText("Finish" if index == count - 1 else "Next")

def run() :
    global ui
    try :
        ui.close()
    except :
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MakeupUI(parent=ptr)
    ui.show()