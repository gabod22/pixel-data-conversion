# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(786, 542)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TextOSFilePath = QLineEdit(self.centralwidget)
        self.TextOSFilePath.setObjectName(u"TextOSFilePath")

        self.horizontalLayout.addWidget(self.TextOSFilePath)

        self.BtnSearchOSFile = QPushButton(self.centralwidget)
        self.BtnSearchOSFile.setObjectName(u"BtnSearchOSFile")

        self.horizontalLayout.addWidget(self.BtnSearchOSFile)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.TextOCFilePath = QLineEdit(self.centralwidget)
        self.TextOCFilePath.setObjectName(u"TextOCFilePath")

        self.horizontalLayout_2.addWidget(self.TextOCFilePath)

        self.BtnsSearchOCFile = QPushButton(self.centralwidget)
        self.BtnsSearchOCFile.setObjectName(u"BtnsSearchOCFile")

        self.horizontalLayout_2.addWidget(self.BtnsSearchOCFile)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.TextProductsFilePath = QLineEdit(self.centralwidget)
        self.TextProductsFilePath.setObjectName(u"TextProductsFilePath")

        self.horizontalLayout_3.addWidget(self.TextProductsFilePath)

        self.BtnSearchProductsFile = QPushButton(self.centralwidget)
        self.BtnSearchProductsFile.setObjectName(u"BtnSearchProductsFile")

        self.horizontalLayout_3.addWidget(self.BtnSearchProductsFile)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.TableServices = QTableWidget(self.centralwidget)
        self.TableServices.setObjectName(u"TableServices")

        self.verticalLayout_4.addWidget(self.TableServices)

        self.BtnProcessFiles = QPushButton(self.centralwidget)
        self.BtnProcessFiles.setObjectName(u"BtnProcessFiles")

        self.verticalLayout_4.addWidget(self.BtnProcessFiles)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 786, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ARCHIVO DE EXCEL DE LAS ORDENES DE SERVICIO", None))
        self.BtnSearchOSFile.setText(QCoreApplication.translate("MainWindow", u"Buscar documento", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"ARCHIVO DE EXEL DE LAS ORDENES DE COMRPA", None))
        self.BtnsSearchOCFile.setText(QCoreApplication.translate("MainWindow", u"Buscar documento", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ARCHIVO DE EXCEL DE LOS PRODUCTOS", None))
        self.BtnSearchProductsFile.setText(QCoreApplication.translate("MainWindow", u"Buscar documento", None))
        self.BtnProcessFiles.setText(QCoreApplication.translate("MainWindow", u"Procesar documentos", None))
    # retranslateUi

