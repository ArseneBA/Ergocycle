# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 20:42:44 2022

@author: Nicolas Pelletier-Côté
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QFont, QPixmap
# import time
# import sys

# from MainWindowMotor import MainWindowMotor
# from MotorParameters import MotorParameters
# from ActivityMenu import ActivityMenu
# from ErrorMenu import ErrorMenu
from SummaryMenu import SummaryMenu

SCREEN_WIDTH = 1920
SCREEN_HEIGTH = 1080

class StopMenu(QWidget):
    def __init__(self):
        super(StopMenu, self).__init__()
        
        self.setGeometry(750, 450, SCREEN_WIDTH/5, SCREEN_HEIGTH/4)
        self.setWindowTitle("Confirmation")
        self.setStyleSheet("background-color: white;")
        
        self.initUI()

    def initUI(self):        
        # self.logo_label = QtWidgets.QLabel(self)
        # self.pixmap = QPixmap('s2m_logo_resized.jpg') # Modifier la taille de l'image au besoin
        # self.logo_label.setPixmap(self.pixmap)
        # self.logo_label.resize(self.pixmap.width(), self.pixmap.height())
        
        self.menu_label = QtWidgets.QLabel(self)
        self.menu_label.setText("Confirmation")
        self.menu_label.move(130,30)
        self.menu_label.setFont(QFont('Arial', 15, weight = QFont.Bold))
        self.menu_label.adjustSize()
        
        self.confirmation_label = QtWidgets.QLabel(self)
        self.confirmation_label.setText("Voulez-vous vraiment mettre fin\n   à la séance d'entraînement?")
        self.confirmation_label.move(40,100)
        self.confirmation_label.setFont(QFont('Arial', 15, weight = QFont.Bold))
        self.confirmation_label.adjustSize()
        
        self.confirmation_button = QtWidgets.QPushButton(self)
        self.confirmation_button.setText("    Oui    ")
        self.confirmation_button.move(100, 200)
        self.confirmation_button.setFont(QFont('Arial', 14))
        self.confirmation_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.confirmation_button.adjustSize()
        self.confirmation_button.clicked.connect(lambda:self.stop_training())  
        
        self.continue_button = QtWidgets.QPushButton(self)
        self.continue_button.setText("    Non    ")
        self.continue_button.move(200, 200)
        self.continue_button.setFont(QFont('Arial', 14))
        self.continue_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.continue_button.adjustSize()
        self.continue_button.clicked.connect(lambda:self.close())
        
    def stop_training(self):
        # print("Séance terminée")
        self.summaryMenu = SummaryMenu()
        # super().close()
        self.close()
        self.summaryMenu.show()