import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
import lib
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QLineEdit, QFileDialog, \
    QMessageBox, QTextEdit, QInputDialog
import math
from db_window import Window
import pickle


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis/main.ui', self)
        self.setFixedSize(945, 605)
        self.hexTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.extraSelections = []
        self.actionOpen.triggered.connect(self.openFileNameDialog)
        self.actionSave.triggered.connect(self.save_csv)
        self.actionExit_2.triggered.connect(self.exit)
        self.findPushButton.clicked.connect(self.find_word)
        self.hexTable.verticalHeader().setVisible(False)
        self.decodedTextEdit.setReadOnly(True)
        self.codeComboBox.addItems(lib.ENCODINGS)
        self.codeComboBox.activated.connect(self.change_codec)
        self.db_window = Window()
        self.actionDataBase.triggered.connect(self.show_db_window)
        self.actionSaveToDb.triggered.connect(self.save_to_db)
        self.old_codec = 'utf-8'
        self.openfile = None
        self.data = None

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Binares (*.bin);;"
                                                  "CSV-HEX Tabel (*.csv)", options=options)
        self.openfile = fileName
        try:
            if fileName[-4::] == '.csv':
                with open(fileName) as f:
                    f = [i.rstrip('\n').split(';') for i in f.readlines()]
                    self.load_to_table(f)
            elif fileName:
                data = lib.get_hex_table(fileName)
                self.load_to_table(data)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Something wrong")
            msg.setWindowTitle("Error")
            msg.exec_()

    def append_extra_selection(self, tc):
        ex = QTextEdit.ExtraSelection()
        ex.cursor = tc
        ex.format.setForeground(QBrush(Qt.blue))
        ex.format.setBackground(QBrush(Qt.yellow))
        self.extraSelections.append(ex)

    def find_word(self):
        self.extraSelections.clear()
        doc = self.decodedTextEdit.document()
        self.find_recursion(0)
        self.decodedTextEdit.setExtraSelections(self.extraSelections)

    def find_recursion(self, pos):
        doc = self.decodedTextEdit.document()
        tc = doc.find(self.findLineEdit.text(), pos)
        if not tc.isNull():
            self.append_extra_selection(tc)
            self.find_recursion(tc.selectionEnd())

    def change_codec(self, n: int):
        if len(self.decodedTextEdit.toPlainText()):
            codec = lib.ENCODINGS[n]
            if codec != 'Unicode':
                try:
                    text = self.text.encode('utf-8').decode(codec)
                    self.decodedTextEdit.clear()
                    self.decodedTextEdit.setPlainText(text)
                    self.old_codec = lib.ENCODINGS[n]
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(f"Can`t decode this with {codec}")
                    msg.setWindowTitle("Codec Error")
                    msg.exec_()
            else:
                self.decodedTextEdit.clear()
                self.decodedTextEdit.setPlainText(self.text)

    def save_csv(self):
        if self.openfile is None:
            pass
        else:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                      "Csv files (*.csv)", options=options)
            with open(fileName, 'w') as f:
                for i in lib.get_hex_table(self.openfile):
                    f.write(';'.join(i) + '\n')

    def save_to_db(self):
        if self.openfile is None:
            pass
        else:
            entry_name, ok = QInputDialog.getText(self, 'DB entry name', 'Enter DB entry name:')
            if len(entry_name) != 0:
                lib.add_to_db(entry_name, pickle.dumps(lib.get_hex_table(self.openfile)))

    def show_db_window(self):
        self.db_window.show()


    def load_to_table(self, data):
        self.hexTable.setRowCount(len(data))
        for row in range(len(data)):
            for column in range(1, len(data[row]) + 1):
                self.hexTable.setItem(row, column, QTableWidgetItem(data[row][column - 1]))
        tmp = 0
        max_len = int(math.log(len(data), 16) + 1)
        for column in range(len(data)):
            sym = '0' * (max_len - len(hex(tmp)[2::]) + 1) + str(hex(tmp)[2::])
            self.hexTable.setItem(column, 0, QTableWidgetItem(sym))
            tmp += 16
        self.data_one_dim = [a for b in data for a in b]
        self.text = ''.join([chr(int(i, 16)) for i in self.data_one_dim])
        self.decodedTextEdit.setPlainText(''.join([chr(int(i, 16)) for i in self.data_one_dim]))
        for row in range(len(data)):
            for column in range(1, len(data[row]) + 1):
                self.hexTable.item(row, 0).setBackground(QBrush(QColor('#bfbfe5')))
        for row in range(len(data)):
            for column in range(1, len(data[row]) + 1):
                self.hexTable.item(row, column).setBackground(QBrush(QColor('#e7cbbd')))

    def exit(self):
        sys.exit()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())