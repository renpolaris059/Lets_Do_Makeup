try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

# 🔸 กำหนดโฟลเดอร์ของแต่ละหมวด (ชื่อหมวด = ชื่อโฟลเดอร์)
ICON_FOLDERS = {
    "Foundation": "foundation_folder",
    "Blush": "blush_folder",
    "Eyeshadow": "eyeshadow_folder",
    "Eyeliner": "eyeliner_folder",
    "Lip": "lip_folder",
    "Hairstyle": "hair_folder",
    "Clothes": "clothes_folder",
    "Accessory": "accessory_folder"
}

# 🔸 ฟังก์ชันโหลด path ของภาพทั้งหมดในโฟลเดอร์
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
        self.resize(900, 650)
        self.setStyleSheet('background-color: #c8bfe7;')

        # 🟣 MAIN LAYOUT
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)

        # ---------------- Left (Face Preview) ----------------
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
        ''')
        self.facePreview.setFixedSize(400, 520)
        self.mainLayout.addWidget(self.facePreview)

        # ---------------- Middle (Category Buttons) ----------------
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
                    background-color: #a69ebf;
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

        # ---------------- Right (Stack of Grid Pages) ----------------
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.rightLayout, stretch=2)

        self.gridOuterFrame = QtWidgets.QFrame()
        self.gridOuterFrame.setStyleSheet('''
            QFrame {
                background-color: white;
                border: 3px solid black;
                border-radius: 10px;
            }
        ''')
        self.gridOuterLayout = QtWidgets.QVBoxLayout(self.gridOuterFrame)
        self.gridOuterLayout.setContentsMargins(10, 10, 10, 10)

        self.stack = QtWidgets.QStackedWidget()
        self.gridOuterLayout.addWidget(self.stack)

        # 🔹 สร้างหน้า grid สำหรับแต่ละหมวด
        base_dir = os.path.dirname(__file__)
        for name in self.categoryButtons:
            folder_path = os.path.join(base_dir, ICON_FOLDERS[name])
            page = self.createGridPage(name, folder_path)
            self.stack.addWidget(page)

        self.gridOuterFrame.setFixedSize(250, 520)
        self.rightLayout.addWidget(self.gridOuterFrame, alignment=QtCore.Qt.AlignCenter)

        # ---------------- Navigation Buttons ----------------
        self.navLayout = QtWidgets.QHBoxLayout()
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
                    border: 2px solid black;
                }
            ''')
        self.navLayout.addWidget(self.backBtn)
        self.navLayout.addWidget(self.nextBtn)
        self.rightLayout.addLayout(self.navLayout)

        # ---------------- Connect Events ----------------
        self.categoryGroup.buttons()[0].setChecked(True)
        self.categoryGroup.buttonClicked.connect(self.switchCategory)
        self.backBtn.clicked.connect(self.goBack)
        self.nextBtn.clicked.connect(self.goNext)
        self.updateNavButtons()

    # 🔸 สร้างหน้ารวมปุ่มไอคอน
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
                    border: 3px solid #a69ebf;
                    background-color: #f2e9ff;
                }
            ''')
            layout.addWidget(btn, i // 2, i % 2)

        return widget

    # 🔸 เปลี่ยนหน้าเมื่อเลือกหมวด
    def switchCategory(self, button):
        index = self.categoryGroup.id(button)
        self.stack.setCurrentIndex(index)
        self.updateNavButtons()

    # 🔸 ปุ่ม Next / Back
    def goNext(self):
        index = self.stack.currentIndex()
        if index < self.stack.count() - 1:
            self.stack.setCurrentIndex(index + 1)
            self.categoryGroup.buttons()[index + 1].setChecked(True)
        elif index == self.stack.count() - 1:
            QtWidgets.QMessageBox.information(self, "Let's Do Makeup !", "FINISH")
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


# 🔹 ฟังก์ชันเปิด UI ใน Maya
def run():
    global ui
    try:
        ui.close()
    except:
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MakeupUI(parent=ptr)
    ui.show()
