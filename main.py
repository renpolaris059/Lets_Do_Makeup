try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

from . import util
import maya.OpenMayaUI as omui
import os

FACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'face_folder'))

ICON_FOLDERS = {
    "Foundation": "foundation_folder",
    "Blush": "blush_folder",
    "Eyeshadow": "eyeshadow_folder",
    "Eyeliner": "eyeliner_folder",
    "Lip": "lip_folder",
    "Hairstyle": "hair_folder",
    "Clothes": "clothes_folder",
    "Accessory": "accessory_folder",
}

def load_icons_from_folder(folder_path):
    if not os.path.exists(folder_path):
        return []
    exts = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    return [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(exts)
    ]

class MakeupUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Let's Do Makeup !")
        self.resize(800, 650)
        self.setStyleSheet('background-color: #c8bfe7;')

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(self.mainLayout)

        self.preview_w = 380
        self.preview_h = 650

        self.faceScene = QtWidgets.QGraphicsScene()
        self.faceScene.setSceneRect(0, 0, self.preview_w, self.preview_h)
        self.faceView = QtWidgets.QGraphicsView(self.faceScene)
        self.faceView.setFixedSize(self.preview_w, self.preview_h)
        self.faceView.setStyleSheet('''
            QGraphicsView {
                border: 3px solid #c8bfe7;
                background-color: #c8bfe7;
        }
        ''')
        self.faceView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.faceView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.faceView.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.faceView.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.mainLayout.addWidget(self.faceView)

        face = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(f'{FACE_DIR}/blank'))
        face.setZValue(0)
        self.faceScene.addItem(face)

        self.categoryFrame = QtWidgets.QFrame()
        self.categoryLayout = QtWidgets.QVBoxLayout(self.categoryFrame)
        self.categoryLayout.setSpacing(5)
        self.categoryLayout.setContentsMargins(10, 10, 10, 10)

        self.categoryButtons = list(ICON_FOLDERS.keys())
        self.categoryGroup = QtWidgets.QButtonGroup(self)

        for i, name in enumerate(self.categoryButtons):
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
            folder_path = os.path.join(base_dir, ICON_FOLDERS[name])
            page = self.createGridPage(name, folder_path)
            self.stack.addWidget(page)

        self.gridOuterFrame.setFixedSize(250, 590)
        self.stack.setStyleSheet('border-radius:6px;')
        self.rightLayout.addWidget(self.gridOuterFrame, alignment=QtCore.Qt.AlignCenter)

        self.nextAndBackButtonLayout = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setFixedSize(125, 100)
        self.nextButton = QtWidgets.QPushButton("Next")
        self.nextButton.setFixedSize(125, 100)

        for btn in (self.backButton, self.nextButton):
            btn.setFixedHeight(40)
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

    def createGridPage(self, category, folder_path):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        icons = load_icons_from_folder(folder_path)

        if not icons:
            label = QtWidgets.QLabel(f"No images found in {category}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(label)
            return widget

        num_columns = 2
        for i, icon_path in enumerate(icons):
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

        return widget

    def switchCategory(self, button):
        index = self.categoryGroup.id(button)
        self.stack.setCurrentIndex(index)
        self.updateNextBackButtons()

    def goBack(self):
        index = self.stack.currentIndex()
        if index > 0:
            self.stack.setCurrentIndex(index - 1)
            self.categoryGroup.buttons()[index - 1].setChecked(True)
        self.updateNextBackButtons()

    def goNext(self):
        index = self.stack.currentIndex()
        if index < self.stack.count() - 1:
            self.stack.setCurrentIndex(index + 1)
            self.categoryGroup.buttons()[index + 1].setChecked(True)
        elif index == self.stack.count() - 1:
            QtWidgets.QMessageBox.information(self, "Let's Do Makeup !", "FINISH")
        self.updateNextBackButtons()

    def updateNextBackButtons(self):
        index = self.stack.currentIndex()
        count = self.stack.count()
        self.backButton.setEnabled(index > 0)
        self.nextButton.setText("Finish" if index == count - 1 else "Next")

def run():
    global ui
    try:
        ui.close()
    except:
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MakeupUI(parent=ptr)
    ui.show()