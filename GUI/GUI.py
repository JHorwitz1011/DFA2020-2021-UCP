from PyQt5.QtWidgets import (QDesktopWidget, QMessageBox, QLabel, QWidget, QPushButton, QGridLayout, QApplication, QMainWindow)
from PyQt5 import QtCore
import sys
import RunnablePong



class PyQtLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        Label1 = QLabel('Computer Vision Games')
        Label1.adjustSize()
        Label1.setAlignment(QtCore.Qt.AlignCenter)

        playBtn = QPushButton('Play')
        playBtn.clicked.connect(self.runPong)

        settingsBtn = QPushButton('Settings',self)
        settingsBtn.clicked.connect(self.openSettings)
         
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(Label1, 0, 1)
        grid.addWidget(playBtn, 1, 0)
        grid.addWidget(settingsBtn, 1, 2)
 
        self.setLayout(grid)

        self.resize(500,500)
        self.center()

        self.setWindowTitle('Aruco Pong')
        self.show()

    def openSettings(self):
        print("Settings")
        

    def runPong(self):
        print("Start game")
        RunnablePong.main()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            RunnablePong.quit()
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    GUI = PyQtLayout()
 
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



