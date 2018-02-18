import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_window import Ui_MainWindow
import csv
import datetime
import os
from pdfrw import PdfReader
from models import *
import re

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.title = 'ECE Instrument Room Inventory Tool'
        self.label_puid.setText("XXXXX-XXXXX")
        self.label_puid.setMinimumWidth(500)
        self.initTables()
        self.text_search.textChanged.connect(self.searchTextChanged)
        self.initUI()
        self.initText()
        self.button_inductoradd.clicked.connect(self.buttonClicked)
        self.button_resistoradd.clicked.connect(self.buttonClicked)
        self.button_capadd.clicked.connect(self.buttonClicked)
        self.button_icadd.clicked.connect(self.buttonClicked)

    def initText(self):
        self.text_icquantity.setText("0")
        self.text_icname.setText("")

        self.text_resistorvalue.setText("")
        self.text_resistorquantity.setText("0")

        self.text_inductorquantity.setText("0")
        self.text_inductorvalue.setText("")

        self.text_capquantity.setText("0")
        self.text_capvalue.setText("")

    def getPrefix(self):
        if self.sender() == self.button_inductoradd:
            preText = re.search(r'\((.)\)', self.combo_inductor.currentText())

        if self.sender() == self.button_capadd:
            preText = re.search(r'\((.)\)', self.combo_cap.currentText())

        if self.sender() == self.button_resistoradd:
            preText = re.search(r'\((.)\)', self.combo_resistor.currentText())

        if preText == None:
            return ""
        return preText.group(1)

    def buttonClicked(self):
        if self.sender() == self.button_inductoradd:
            valueText = self.text_inductorvalue.toPlainText() + " " + self.getPrefix() + "H"
            self.model_quick.insertCompRow("Inductor", valueText, self.text_inductorquantity.toPlainText())
            self.text_inductorquantity.setText("0")
            self.text_inductorvalue.setText("")

        if self.sender() == self.button_capadd:
            valueText = self.text_capvalue.toPlainText() + " " + self.getPrefix() + "F"
            self.model_quick.insertCompRow("Capacitor", valueText, self.text_capquantity.toPlainText())
            self.text_capquantity.setText("0")
            self.text_capvalue.setText("")

        if self.sender() == self.button_resistoradd:
            valueText = self.text_resistorvalue.toPlainText() + " " + self.getPrefix() + "Ω"
            self.model_quick.insertCompRow("Resistor", valueText, self.text_resistorquantity.toPlainText())
            self.text_resistorvalue.setText("")
            self.text_resistorquantity.setText("0")

        if self.sender() == self.button_icadd:
            self.model_quick.insertCompRow("IC", self.text_icname.toPlainText(), self.text_icquantity.toPlainText())
            self.text_icname.setText("")
            self.text_icquantity.setText("0")

    def searchTextChanged(self):
        print(self.text_search.toPlainText())
        self.compList.searchText(self.text_search.toPlainText())

    def compListChanged(self, current, previous):
        if (current.column() == 2):
            self.compList.launchDatasheet(current.row(), current.column())


    def initTables(self):
        current_data = []
        with open("ICs_7400d.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header_row = next(reader)
            for line in reader:
                current_data.append(line)
        self.compList = CurrentModel(current_data, header_row)
        #self.table_current.horizontalHeader().setStretchLastSection(True)
        self.table_current.verticalHeader().setVisible(False)
        self.table_current.setModel(self.compList)
        self.compListSelection = QItemSelectionModel()
        self.compListSelection.setModel(self.compList)
        self.compListSelection.currentChanged.connect(self.compListChanged)
        self.table_current.setSelectionModel(self.compListSelection)
        self.table_current.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_current.setColumnWidth(0, 120)
        self.table_current.setColumnWidth(2, 160)
        #self.table_current.setRowHeight(0, self.table_current.fontMetrics().height() * 3)

        now = datetime.datetime.now()
        current_data = [[" ", "{}-{}-{}".format(now.year, now.month, now.day), "0"]]
        header_row = ['Item', 'Date Issued', 'Quantity']
        self.model_borrowed = BorrowedModel(current_data, header_row)
        self.table_borrowed.horizontalHeader().setStretchLastSection(True)
        self.table_borrowed.verticalHeader().setVisible(False)
        self.table_borrowed.setModel(self.model_borrowed)
        self.table_borrowed.setColumnWidth(0, 600)

        current_data = [[" ", " ", "{}-{}-{}".format(now.year, now.month, now.day), "0"]]
        header_row = ['Item', 'Value / Part No.', 'Date Issued', 'Quantity']
        self.model_quick = QuickaddModel(current_data, header_row)
        self.table_quick.horizontalHeader().setStretchLastSection(True)
        self.table_quick.verticalHeader().setVisible(False)
        self.table_quick.setModel(self.model_quick)
        self.table_quick.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_current.setColumnWidth(0, 60)

        now = datetime.datetime.now()
        current_data = [[" ", "{}-{}-{}".format(now.year, now.month, now.day), "0"]]
        header_row = ['Item', 'Date Issued', 'Quantity']
        self.model_requested = BorrowedModel(current_data, header_row)
        self.table_requested.horizontalHeader().setStretchLastSection(True)
        self.table_requested.verticalHeader().setVisible(False)
        self.table_requested.setModel(self.model_requested)
        self.table_requested.setColumnWidth(0, 600)

    def initUI(self):
        self.setWindowTitle(self.title)
      #  self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex.show()
    sys.exit(app.exec_())