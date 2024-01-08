from PyQt5 import uic, QtWidgets
import sqlite3



class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/db.ui", self)
        self.setWindowTitle("DB Form")
        self.setFixedSize(640, 480)
        self.add_names_to_widget()
        self.namesListWidget.itemClicked.connect(self.click_item)
        self.deletePushButton.clicked.connect(self.delete_db_entry)
        self.name = None

    def add_names_to_widget(self):
        db = sqlite3.connect('dbs/database.db')
        curs = db.cursor()
        names = curs.execute("SELECT name FROM main").fetchall()
        for i in names:
            self.namesListWidget.addItem(i[0])
        db.close()

    def click_item(self, item):
        self.dbEntryName.setText(item.text())
        self.name = item.text()
        db = sqlite3.connect('dbs/database.db')
        curs = db.cursor()
        date = curs.execute(f"SELECT date FROM main WHERE name = '{item.text()}'").fetchall()
        db.close()
        self.dbEntryDate.setText(date[0][0])

    def delete_db_entry(self):
        if self.name == None:
            pass
        else:
            db = sqlite3.connect('dbs/database.db')
            curs = db.cursor()
            curs.execute('DELETE FROM main WHERE name=(?)', (self.name,))
            db.commit()
            db.close()
            db = sqlite3.connect('dbs/database.db')
            curs = db.cursor()
            names = curs.execute("SELECT name FROM main").fetchall()
            for i in names:
                self.namesListWidget.addItem(i[0])
            db.close()






