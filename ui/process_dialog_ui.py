# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'process_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_ProcessDialog(object):
    def setupUi(self, ProcessDialog):
        if not ProcessDialog.objectName():
            ProcessDialog.setObjectName(u"ProcessDialog")
        ProcessDialog.resize(396, 290)
        self.verticalLayout = QVBoxLayout(ProcessDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.LbStatus = QLabel(ProcessDialog)
        self.LbStatus.setObjectName(u"LbStatus")
        font = QFont()
        font.setPointSize(18)
        self.LbStatus.setFont(font)

        self.verticalLayout.addWidget(self.LbStatus)

        self.TextProcessLog = QPlainTextEdit(ProcessDialog)
        self.TextProcessLog.setObjectName(u"TextProcessLog")

        self.verticalLayout.addWidget(self.TextProcessLog)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.BtnCancel = QPushButton(ProcessDialog)
        self.BtnCancel.setObjectName(u"BtnCancel")

        self.horizontalLayout.addWidget(self.BtnCancel)

        self.BtnAccept = QPushButton(ProcessDialog)
        self.BtnAccept.setObjectName(u"BtnAccept")

        self.horizontalLayout.addWidget(self.BtnAccept)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ProcessDialog)

        QMetaObject.connectSlotsByName(ProcessDialog)
    # setupUi

    def retranslateUi(self, ProcessDialog):
        ProcessDialog.setWindowTitle(QCoreApplication.translate("ProcessDialog", u"Procesando...", None))
        self.LbStatus.setText(QCoreApplication.translate("ProcessDialog", u"Cargando....", None))
        self.BtnCancel.setText(QCoreApplication.translate("ProcessDialog", u"Cancelar", None))
        self.BtnAccept.setText(QCoreApplication.translate("ProcessDialog", u"Aceptar", None))
    # retranslateUi

