try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

foundation_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'foundation_folder'))

class MakeupUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Let's Do Makeup !")
        self.resize(900, 650)


        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)
        self.setStyleSheet('background-color: #c8bfe7;')

        self.facePreview = QtWidgets.QLabel("Face Preview")
        self.facePreview.setAlignment(QtCore.Qt.AlignCenter)
        self.facePreview.setStyleSheet(''' 
            QLabel {
                color: black;
                background-color: white;
                border: 3px solid black;
                font-size: 20px;
                font-weight: bold;
            }
        '''
        )
        self.facePreview.setFixedSize(400, 520)
        self.mainLayout.addWidget(self.facePreview)

        self.categoryFrame = QtWidgets.QFrame()
        self.categoryLayout = QtWidgets.QVBoxLayout(self.categoryFrame)
        self.categoryLayout.setSpacing(5)
        self.categoryLayout.setContentsMargins(10, 10, 10, 10)

        self.categoryButtons = [
            "Foundation", "Blush", "Eyeshadow", "Eyeliner",
            "Lip", "Hairstyle", "Clothes", "Accessory"
        ]

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
                    text-align: center;
                }
                QPushButton:hover {
                    color: white;
                    background-color: #a69ebf;
                    border: 2px solid white;
                }
                QPushButton:checked {
                    color: white;
                    background-color: #8b7abf;
                    border: 2px solid white;
                    font-weight: bold;
                }
            '''
            )
            self.categoryGroup.addButton(btn, i)
            self.categoryLayout.addWidget(btn)

        self.categoryFrame.setFixedSize(160, 520)
        self.mainLayout.addWidget(self.categoryFrame)

        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSpacing(10)
        self.mainLayout.addLayout(self.rightLayout, stretch=2)

        self.gridOuterFrame = QtWidgets.QFrame()
        self.gridOuterFrame.setStyleSheet(''' 
            QFrame {
                background-color: white;
                border: 3px solid black;
                border-radius: 10px;
            }
        '''
        )
        self.gridOuterLayout = QtWidgets.QVBoxLayout(self.gridOuterFrame)
        self.gridOuterLayout.setContentsMargins(10, 10, 10, 10)

        self.stack = QtWidgets.QStackedWidget()

        self.gridOuterLayout.addWidget(self.stack)

        for name in self.categoryButtons:
            page = self.createGridPage(name)
            self.stack.addWidget(page)

        self.gridOuterFrame.setFixedSize(250, 520)
        self.rightLayout.addWidget(self.gridOuterFrame, alignment=QtCore.Qt.AlignCenter)

        self.navLayout = QtWidgets.QHBoxLayout()
        self.navLayout.setSpacing(30)

        self.backBtn = QtWidgets.QPushButton("Back")
        self.nextBtn = QtWidgets.QPushButton("Next")

        for btn in (self.backBtn, self.nextBtn):
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
                    background-color: #a69ebf;
                    border: 2px solid white;
                }
            ''')

        self.navLayout.addWidget(self.backBtn)
        self.navLayout.addWidget(self.nextBtn)
        self.rightLayout.addLayout(self.navLayout)

        self.categoryGroup.buttons()[0].setChecked(True)
        self.categoryGroup.buttonClicked.connect(self.switchCategory)
        self.backBtn.clicked.connect(self.goBack)
        self.nextBtn.clicked.connect(self.goNext)

        self.updateNavButtons()

    def createGridPage(self, category):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        foundation_icons = [
            os.path.join(foundation_folder, "foundation 1.png"),
            os.path.join(foundation_folder, "foundation 2.png"),
            os.path.join(foundation_folder, "foundation 3.png"),
            os.path.join(foundation_folder, "foundation 4.png"),
            os.path.join(foundation_folder, "foundation 5.png"),
            os.path.join(foundation_folder, "foundation 6.png"),
            os.path.join(foundation_folder, "foundation 7.png"),
            os.path.join(foundation_folder, "foundation 8.png")
        ]
        for i in range(10):
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(80, 80)

            if category == "Foundation":
                if i < len(foundation_icons) and os.path.exists(foundation_icons[i]):
                    btn.setIcon(QtGui.QIcon(foundation_icons[i]))
                    btn.setIconSize(QtCore.QSize(60, 60))
                else:
                    btn.setText(f"{category} {i + 1}")
            else:
                btn.setText(f"{category} {i + 1}")

            btn.setStyleSheet('''
                QPushButton {
                    color: black;
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #f0d9f9;
                }
            ''')
            layout.addWidget(btn, i // 2, i % 2)

        return widget

    def switchCategory(self, button):
        index = self.categoryGroup.id(button)
        self.stack.setCurrentIndex(index)
        self.updateNavButtons()

    def goNext(self):
        index = self.stack.currentIndex()
        if index < self.stack.count() - 1:
            self.stack.setCurrentIndex(index + 1)
            self.categoryGroup.buttons()[index + 1].setChecked(True)
        elif index == self.stack.count() - 1:
            self.message = QtWidgets.QMessageBox.information(self,"Let's Do Makeup !","FINISH")
        self.updateNavButtons()

    def goBack(self):
        index = self.stack.currentIndex()
        if index > 0:
            self.stack.setCurrentIndex(index - 1)
            self.categoryGroup.buttons()[index - 1].setChecked(True)
        self.updateNavButtons()

    def updateNavButtons(self):
        index = self.stack.currentIndex()
        count = self.stack.count()
        self.backBtn.setEnabled(index > 0)
        self.nextBtn.setText("Finish" if index == count - 1 else "Next")

def run():
    global ui
    try:
        ui.close()
    except:
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MakeupUI(parent=ptr)
    ui.show()