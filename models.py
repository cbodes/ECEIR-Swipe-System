from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import os
import datetime

class ButtonDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent, filepath):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.filepath = filepath

    def createEditor(self, parent, option, index):
        combo = QtWidgets.QPushButton(str(index.data()), parent)

        # self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        combo.clicked.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        # editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class BorrowedModel(QAbstractTableModel):
    def __init__(self, data = None, header_row = None, header_col = None, parent=None):
        QAbstractTableModel.__init__(self, parent=parent)
        self.header_col = header_col
        self.header_row = header_row
        self.data = data
        self.dataVisible = data

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            try:
                return self.header_row[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Vertical:
            try:
                return self.header_col[section]
            except (IndexError, ):
                return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole and (index.column() == 2 or index.column() == 1):
            return Qt.AlignCenter
        elif role == Qt.DisplayRole:
            if index.row() >= self.rowCount() or index.column() >= self.columnCount():
                return QVariant()
            return self.dataVisible[index.row()][index.column()]
        elif role == Qt.ForegroundRole:
            return QBrush(Qt.yellow)
        else:
            return QVariant()


    def setData(self, index, value, role):
        if role == Qt.EditRole and value != "":
            if index.column() == 2:
                self.dataVisible[index.row()][index.column()] = value
                try:
                    if int(value) == 0:
                        self.dataVisible[index.row()][index.column()] = "0"
                except:
                    self.dataVisible[index.row()][index.column()] = "0"
                if index.row() == 0 and self.dataVisible[index.row()][index.column()] != "0":
                    self.insertRow()
                self.data = self.dataVisible
                return True
            elif index.column() == 0:
                self.dataVisible[index.row()][index.column()] = value
                self.dataVisible[index.row()][2] = "1"
                if (index.row() == 0):
                    self.insertRow()
                self.data = self.dataVisible
                return True
        elif role == Qt.DisplayRole:
            self.dataVisible[index.row()][index.column()] = value
            self.data = self.dataVisible
            return True
        else:
            return False

    def insertRow(self):
        self.beginInsertRows(QModelIndex(), 0, 0)
        now = datetime.datetime.now()
        newRow = [[" ", "{}-{}-{}".format(now.year, now.month, now.day), "0"]]
        for r in range(self.rowCount()):
            newRow.append(self.dataVisible[r])
        self.dataVisible = newRow
        self.endInsertRows()

    def flags(self, index):
        if (index.column() ==  2 or index.column() == 0):
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.data[0])

    def getColumn(self, col_num):
        my_list = []
        for i in range(self.columnCount()):
            my_list.append(self.data[i][col_num])
        return my_list

    def setHeaderRow(self, header_row):
        self.header_row = header_row

    def setHeaderCol(self, header_col):
        self.header_col = header_col

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class QuickaddModel(QAbstractTableModel):
    def __init__(self, data = None, header_row = None, header_col = None, parent=None):
        QAbstractTableModel.__init__(self, parent=parent)
        self.header_col = header_col
        self.header_row = header_row
        self.data = data
        self.dataVisible = data

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            try:
                return self.header_row[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Vertical:
            try:
                return self.header_col[section]
            except (IndexError, ):
                return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.DisplayRole:
            if index.row() >= self.rowCount() or index.column() >= self.columnCount():
                return QVariant()
            return self.dataVisible[index.row()][index.column()]
        elif role == Qt.ForegroundRole:
            return QBrush(Qt.white)
        else:
            return QVariant()


    def setData(self, index, value, role):
        if role == Qt.EditRole and value != "":
            self.dataVisible[index.row()][index.column()] = value
            self.data = self.dataVisible
            return True
        elif role == Qt.DisplayRole:
            self.dataVisible[index.row()][index.column()] = value
            self.data = self.dataVisible
            return True
        else:
            return False

    def insertCompRow(self, component, value, quantity):
        now = datetime.datetime.now()
        newRow = [[component, value, "{}-{}-{}".format(now.year, now.month, now.day), quantity]]
        if self.rowCount() == 1 and self.dataVisible[0][0] == " ":
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self.dataVisible = []
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), 0, 0)
            self.dataVisible = newRow
            self.endInsertRows()

        else:
            for r in range(self.rowCount()):
                newRow.append(self.dataVisible[r])
            self.beginInsertRows(QModelIndex(), 0, 0)
            self.dataVisible = newRow
            self.endInsertRows()
        self.data = self.dataVisible

    def flags(self, index):
        return Qt.ItemIsTristate

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.data[0])

    def getColumn(self, col_num):
        my_list = []
        for i in range(self.columnCount()):
            my_list.append(self.data[i][col_num])
        return my_list

    def setHeaderRow(self, header_row):
        self.header_row = header_row

    def setHeaderCol(self, header_col):
        self.header_col = header_col

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class CurrentModel(QAbstractTableModel):
    def __init__(self, data = None, header_row = None, header_col = None, parent=None):
        QAbstractTableModel.__init__(self, parent=parent)
        self.header_col = header_col
        self.header_row = header_row
        self.dataVisible = data
        self.data = data
        self.first_column = self.getColumn(0)

    def searchText(self, text):
        self.beginRemoveRows(QModelIndex(), 0, len(self.dataVisible) - 1)
        self.dataVisible = []
        self.endRemoveRows()
        newData = []
        for i in range(self.rowCount()):
            if text in self.data[i][0]:
                self.beginInsertRows(QModelIndex(), 0, 0)
                self.dataVisible.append(self.data[i])
                self.endInsertRows()

    def launchDatasheet(self, row, col):
        try:
            os.system("start " + self.data[row][col])
        except:
            pass

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            try:
                return self.header_row[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Vertical:
            return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif index.column() == 2:
            if role == Qt.DisplayRole:
                if self.dataVisible[index.row()][index.column()] != "No Datasheet Available":
                    return "Datasheet"
                else:
                    return "No Datasheet Available"
            elif role == Qt.ForegroundRole:
                if self.dataVisible[index.row()][index.column()] != "No Datasheet Available":
                    return QBrush(Qt.green)
                else:
                    return QBrush(Qt.red)
        elif role == Qt.DisplayRole:
            if index.row() >= self.rowCount() or index.column() >= self.columnCount():
                return QVariant()
            return self.dataVisible[index.row()][index.column()]
        else:
            return QVariant()


    def setData(self, index, value, role):
        return False

    def flags(self, index):
        #if (index.column() == 1):
        #    return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.data[0])

    def getColumn(self, col_num):
        my_list = []
        for i in range(self.rowCount()):
            my_list.append(self.data[i][col_num])
        return my_list

    def setHeaderRow(self, header_row):
        self.header_row = header_row

    def setHeaderCol(self, header_col):
        self.header_col = header_col

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
