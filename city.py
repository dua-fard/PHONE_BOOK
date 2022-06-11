from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox

add_or_edit=[]
table_row=[]
id_holder=[]
type_edit=[]
class Add_city(QDialog):
    def __init__(self,db,Cities):
       super().__init__()
       self.db = db
       self.Cities=Cities
       if add_or_edit[0]==1:
           self.setWindowTitle("Add New Cities")
       elif add_or_edit[0]==2:
           self.setWindowTitle("Edit An Existing City")

       self.setGeometry(100, 100, 330, 400)
       self.setStyleSheet("background-color : cadetblue")
       self.formGroupBox = QGroupBox()
       self.formGroupBox.setStyleSheet("background-color : white")
       if add_or_edit[0] == 1:
                self.citynameLineEdit = QLineEdit()
                self.citycodeLineEdit = QLineEdit()
       elif add_or_edit[0] == 2:
                self.citynameLineEdit = QLineEdit(type_edit[0],self)
                self.citycodeLineEdit = QLineEdit(type_edit[1],self)

       self.createForm()

       self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
       self.buttonBox.setStyleSheet("background-color :lightgray")

       self.buttonBox.accepted.connect(self.getInfo)
       self.buttonBox.rejected.connect(self.reject)

       mainLayout = QVBoxLayout()

       mainLayout.addWidget(self.formGroupBox)
       mainLayout.addWidget(self.buttonBox)

       self.setLayout(mainLayout)
       self.exec_()


    def getInfo(self):

        name = self.citynameLineEdit.text()
        code = self.citycodeLineEdit.text()


        self.setStyleSheet("background-color :lightgray")
        if name == "" and code != "":
            QMessageBox.about(self, "Warning", " Enter City Name! ")
        elif code == "" and name != "":
            QMessageBox.about(self, "Warning", " Enter City Code!")
        elif name == "" and code == "":
            QMessageBox.about(self, "Warning", " Enter City Name And City Code!")
        else:

            if add_or_edit[0]==1:
                       records = self.db.query(self.Cities)
                       t=True

                       for record in records:

                           if record.name==name or record.code==int(code) :

                                       t=False
                                       self.setStyleSheet("background-color :lightgray")
                                       QMessageBox.about(self, "Warning", "This Record Already Exists! ")
                                       self.setStyleSheet("background-color : cadetblue")
                                       break
                       if t==True:
                                      city = self.Cities(name=name, code=code)
                                      self.db.add(city)
                                      self.db.commit()
            elif add_or_edit[0]==2:


                iid = []
                selected_id=id_holder[table_row[0]]
                iid.append(selected_id)
                records = self.db.query(self.Cities).order_by(self.Cities.name)
                for record in records:
                    if record.id == selected_id:
                        record.name=name
                        record.code=str(code)
                        self.db.commit()
                        break

                iid.clear()



        self.close()


    def createForm(self):

        layout = QFormLayout()

        layout.addRow(QLabel("City Name"), self.citynameLineEdit)
        layout.addRow(QLabel("City Code"), self.citycodeLineEdit)

        self.formGroupBox.setLayout(layout)

class CitiesWindow(QWidget):
    def __init__(self,db,Cities):
        super().__init__()

        self.db=db
        self.Cities=Cities

        self.title = "Cities"
        self.setStyleSheet("background-color: cadetblue;")
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 700
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.creatingTables()
        self.show()


    def creatingTables(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['                  City Name                  ',
                                                 '                  City Code                  '])
        self.tableWidget.setStyleSheet("background-color : white")


        pallete = self.tableWidget.palette()
        hightlight_brush = pallete.brush(QPalette.Highlight)
        hightlight_brush.setColor(QColor('dodgerblue'))
        pallete.setBrush(QPalette.Highlight, hightlight_brush)
        self.tableWidget.setPalette(pallete)
        self.vBoxLayout = QVBoxLayout()
        self.filter_bar = QLineEdit(self)
        self.filter_bar.setStyleSheet("background-color : white")
        self.button_Filter = QPushButton('Filter', self)
        self.button_Filter.setStyleSheet("background-color : lavender")
        self.button_Filter.clicked.connect(self.filterr)
        self.vBoxLayout.addWidget(self.filter_bar)
        self.vBoxLayout.addWidget(self.button_Filter)
        self.vBoxLayout.addWidget(self.tableWidget)


        buttons_info = [(' Add ', 'Add A New City ',"background-color : lavender", 50,self.add_new),
                        (' Edit ', 'Edit An Existing City ',"background-color : lavender", 100,self.edit_existing),
                        (' Delete ', 'Delete An Existing City ',"background-color : coral", 150,self.delete_existing)]
        for i in range(len(buttons_info)):
            self.b = QPushButton(buttons_info[i][0], self)
            self.b.setToolTip(buttons_info[i][1])
            self.b.setStyleSheet(buttons_info[i][2])
            self.b.setGeometry(200, 150, 150, 40)
            self.b.move(300, buttons_info[i][3])
            self.vBoxLayout.addWidget(self.b)
            self.b.clicked.connect(buttons_info[i][4])

        self.tableWidget.resizeColumnsToContents()
        self.setLayout(self.vBoxLayout)
        self.show_table()

    def filterr(self):
        value = self.filter_bar.text()
        id_holder.clear()
        self.tableWidget.setRowCount(0)

        records = self.db.query(self.Cities).filter(self.Cities.name.like('%' + value + '%')).order_by(self.Cities.name)
        self.tableWidget.setRowCount(1)
        print(records)
        i = 0
        for city in records:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.setItem(i, 0, QTableWidgetItem(city.name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(city.code)))
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.insertRow(rowPosition)
            id_holder.append(city.id)
            i += 1



    def add_new(self):
        add_or_edit.clear()
        add_or_edit.append(1)
        self.W = Add_city(self.db,self.Cities)
        self.show_table()

    def show_table(self):
                id_holder.clear()
                self.tableWidget.setRowCount(0)

                records = self.db.query( self.Cities).order_by(self.Cities.name)


                self.tableWidget.setRowCount(1)
                i=0
                for city in records:
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(city.name))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(city.code)))
                    self.tableWidget.horizontalHeader().setStretchLastSection(True)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch)
                    self.tableWidget.insertRow(rowPosition)
                    id_holder.append(city.id)
                    i+=1


    def edit_existing(self):

        s=self.tableWidget.currentRow()

        if s!=-1:
                            add_or_edit.clear()
                            type_edit.clear()
                            table_row.append(s)
                            add_or_edit.append(2)


                            selected_id = id_holder[table_row[0]]
                            records = self.db.query(self.Cities).order_by(self.Cities.name)
                            for record in records:
                                if record.id == selected_id:
                                               type_edit.append(record.name)
                                               type_edit.append(str(record.code))
                                               break


                            self.W = Add_city(self.db,self.Cities)
                            self.show_table()
                            table_row.clear()
        else:
            self.setStyleSheet("background-color :lightgray")
            QMessageBox.about(self, "Warning", "You Have To Make A Selection! ")
            self.setStyleSheet("background-color : cadetblue")
    def delete_existing(self):
        s = self.tableWidget.currentRow()

        if s != -1:
                self.setStyleSheet("background-color :lightgray")
                buttonReply = QMessageBox.question(self, 'Warning', "Do You Want To Permanently Delete Your Record?", QMessageBox.Yes | QMessageBox.No )


                if buttonReply == QMessageBox.Yes:
                    table_row.append(s)

                    selected_id = id_holder[table_row[0]]
                    records = self.db.query(self.Cities).order_by(self.Cities.name)
                    for record in records:
                        if record.id ==selected_id:
                            self.db.delete(record)
                            self.db.commit()
                            break


                    self.setStyleSheet("background-color : cadetblue")
                    self.show_table()
                    table_row.clear()
                else:
                    self.show()
                    self.setStyleSheet("background-color : cadetblue")
        else:
            self.setStyleSheet("background-color :lightgray")
            QMessageBox.about(self, "Warning", "You Have To Make A Selection! ")
            self.setStyleSheet("background-color : cadetblue")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CitiesWindow()
    sys.exit(app.exec_())