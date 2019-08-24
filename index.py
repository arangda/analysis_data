import subprocess
import sys,os
from os import path

from config import basedir

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QMessageBox, QLabel


class WindowClass(QWidget):
    def __init__(self,parent=None):
        super(WindowClass,self).__init__(parent)
        self.setWindowTitle("启动程序")
        self.resize(400, 300)
        #self.move(150,100)
        self.btn_1=QPushButton(self)
        self.btn_1.setGeometry(140,50,120,30)
        self.btn_1.setText("启动")
        self.btn_1.clicked.connect(self.run)
        self.lab_1 = QLabel(self)
        self.lab_1.setGeometry(60,180,280,30)
        self.lab_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_1.setOpenExternalLinks(True)

    def run(self):

        self.btn_1.setText('已启动')
        self.lab_1.setText("<a href='http://127.0.0.1:5000'>浏览器打开127.0.0.1:5000访问系统</a>")
        self.lab_1.setStyleSheet(
                                 "QLabel{color:#fff;height:30px;"
                                 "font-size:15px;font-weight:bold;"
                                 "font-family:宋体;}"
                                 )
        QMessageBox.about(self, '程序', '已经启动了')
        #do()


        filepath = os.path.join(basedir, 'run.py')
        cmd = 'python -i ' + filepath
        subprocess.call(cmd,shell=True)




if __name__ == '__main__':

    # 创建应用程序和对象
    appp = QApplication(sys.argv)
    myWin = WindowClass()
    myWin.show()
    sys.exit(appp.exec_())