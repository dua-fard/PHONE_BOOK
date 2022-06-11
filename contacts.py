from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
from PyQt5 import QtCore


add_or_edit=[]
table_row=[]
id_holder=[]
type_edit=[]
combo_title = []
city_id_combo = []
combo_id_holder = []
picture=[]
phone_id=[]
selected=[]
show=[]
class Show_contact(QDialog):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("Info On "+str(show[0])+' '+str(show[1]))
       self.setGeometry(100, 100, 330, 400)
       self.setStyleSheet("background-color : cadetblue")
       self.formGroupBox = QGroupBox()
       self.createForm()
       self.formGroupBox.setStyleSheet("background-color : white")

       self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok )
       self.buttonBox.setStyleSheet("background-color : lightgray")
       self.buttonBox.accepted.connect(self.reject)
       mainLayout = QVBoxLayout()

       mainLayout.addWidget(self.formGroupBox)
       mainLayout.addWidget(self.buttonBox)

       self.setLayout(mainLayout)
       self.exec_()

    def createForm(self):

        layout = QFormLayout()

        layout.addRow(QLabel(str(show[0])+"'s Image:"))
        label = QLabel(self)
        layout.addRow(label)
        pixmap = QPixmap(str(show[6]))
        pixmap_resized = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap_resized)
        label.show()
        layout.addRow(QLabel("First Name:"), QLabel(str(show[0])))
        layout.addRow(QLabel("Last Name:"), QLabel(str(show[1])))
        layout.addRow(QLabel("City :"),QLabel(str(show[2])))
        layout.addRow(QLabel("Phone Number : "), QLabel(str(show[3])))
        if show[4]!="":
                 layout.addRow(QLabel("Phone 2:"), QLabel(str(show[4])))
        if show[5] != "":
                 layout.addRow(QLabel("Phone 3:"), QLabel(str(show[5])))





        self.formGroupBox.setLayout(layout)


class Add_contact(QDialog):
    def __init__(self,db,Cities,Contacts,Numbers):
       super().__init__()
       self.db = db
       self.Cities = Cities
       self.Contacts = Contacts
       self.Numbers = Numbers


       if add_or_edit[0] == 1:
           self.setWindowTitle("Add New Contacts")
       elif add_or_edit[0] == 2:
           self.setWindowTitle("Edit An Existing Contact")

       self.setGeometry(100, 100, 330, 400)
       self.setStyleSheet("background-color : cadetblue")
       self.formGroupBox = QGroupBox()
       self.formGroupBox.setStyleSheet("background-color : white")
       self.cityComboBox = QComboBox()
       self.cityComboBox.setStyleSheet("background-color :light gray")

       records = self.db.query(self.Cities).order_by(self.Cities.name)


       combo_title.clear()
       city_id_combo.clear()
       combo_id_holder.clear()
       for city in records:
           combo_title.append(city.name)
           city_id_combo.append(city.id)
       self.cityComboBox.addItems(combo_title)

       if add_or_edit[0] == 1:
           self.firstnameLineEdit = QLineEdit()
           self.lastnameLineEdit = QLineEdit()
           self.phoneLineEdit = QLineEdit()
           self.phone2LineEdit = QLineEdit()
           self.phone3LineEdit = QLineEdit()
           self.button_pic = QPushButton(self)

           picture.clear()
           picture.append('C:/Users/pc sys/Desktop/PHONE_BOOK/anonymous.jpg')
           def pic():
               file,check= QFileDialog.getOpenFileName(None,'Open file',
                                                                'c:\\',"Image files (*.jpg )")

               if check:
                   picture.clear()
                   picture.append(file)


           self.button_pic.clicked.connect(pic)




       elif add_or_edit[0] == 2:
           self.firstnameLineEdit = QLineEdit(type_edit[0], self)
           self.lastnameLineEdit = QLineEdit(type_edit[1], self)
           self.phoneLineEdit = QLineEdit(str(type_edit[3]), self)
           self.phone2LineEdit = QLineEdit(str(type_edit[4]), self)
           self.phone3LineEdit = QLineEdit(str(type_edit[5]), self)
           self.button_pic = QPushButton(self)
           picture.clear()

           picture.append(type_edit[6])

           def pic():
               file, check = QFileDialog.getOpenFileName(None, 'Open file',
                                                         'c:\\', "Image files (*.jpg )")

               if check:
                   picture.clear()
                   picture.append(file)


           self.button_pic.clicked.connect(pic)


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

        name = self.firstnameLineEdit.text()
        last = self.lastnameLineEdit.text()
        city = self.cityComboBox.currentText()
        combo_id_holder.append(self.cityComboBox.currentIndex())
        phone = self.phoneLineEdit.text()
        phone2 = self.phone2LineEdit.text()
        phone3 = self.phone3LineEdit.text()
        selected.clear()
        selected.append( city_id_combo[combo_id_holder[0]])

        self.setStyleSheet("background-color :lightgray")
        if name == "" and phone != "":
            QMessageBox.about(self, "Warning", " Enter First Name! ")
        elif phone == "" and name != "":
            QMessageBox.about(self, "Warning", " Enter Phone Number !")
        elif name == "" and phone == "":
            QMessageBox.about(self, "Warning", " Enter First Name And Phone Number!")
        else:
            if add_or_edit[0] == 1:

               records = self.db.query(self.Contacts)
               phone_id.clear()
               phone_id.append(1)
               for record in records:
                                          id=record.id
                                          id+=1
                                          phone_id.clear()
                                          phone_id.append(id)

               p=True
               phone_num=[phone,phone2,phone3]
               for i in range(len(phone_num)):
                  if p==True:
                         if phone_num[i] != "":
                                          nums=self.db.query(self.Numbers)
                                          for num in nums:
                                                if num.number == phone_num[i]:

                                                       self.setStyleSheet("background-color :lightgray")
                                                       QMessageBox.about(self, "Warning", "This Number Already Exists! ")
                                                       self.setStyleSheet("background-color : cadetblue")
                                                       p=False
                                                       break
                                          if p == True:
                                               numbersss = self.Numbers(contact_id=phone_id[0], number=phone_num[i])
                                               self.db.add(numbersss)
                         elif phone_num[i] == "":
                            self.db.query(self.Numbers)
                            numbersss = self.Numbers(contact_id=phone_id[0], number="")
                            self.db.add(numbersss)

               if p==True:
                        contact = self.Contacts(first_name=name, last_name=last,city_id=str(selected[0]),phone=phone_id[0],image=picture[0])
                        self.db.add(contact)
                        self.db.commit()


            elif add_or_edit[0] == 2:

                iid = []
                selected_id = id_holder[table_row[0]]
                iid.append(selected_id)
                records = self.db.query(self.Contacts).order_by(self.Contacts.first_name)
                for record in records:
                    if record.id == selected_id:
                        record.first_name = name
                        record.last_name =last
                        record.city_id = str(selected[0])
                        nums = self.db.query(self.Numbers)
                        i=0
                        phone_d=[phone,phone2,phone3]
                        for num in nums:
                                if record.phone==num.contact_id :
                                    num.number=phone_d[i]
                                    i+=1
                        record.image = picture[0]
                        self.db.commit()
                        break

        self.close()

    def createForm(self):

        layout = QFormLayout()

        layout.addRow(QLabel("First Name"), self.firstnameLineEdit)
        layout.addRow(QLabel("Last Name"), self.lastnameLineEdit)
        if add_or_edit[0] == 2:
                    layout.addRow(QLabel("Previously Selected City :"),QLabel(str(type_edit[2])))
        layout.addRow(QLabel("City"), self.cityComboBox)
        layout.addRow(QLabel("Phone *"), self.phoneLineEdit)
        layout.addRow(QLabel("Phone "), self.phone2LineEdit)
        layout.addRow(QLabel("Phone "), self.phone3LineEdit)
        if add_or_edit[0] == 2:
            layout.addRow(QLabel("Previously Selected Image :"))

            label=QLabel(self)
            layout.addRow(label)
            pixmap = QPixmap(str(type_edit[6]))
            pixmap_resized = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
            label.setPixmap(pixmap_resized)
            label.show()
        layout.addRow(self.button_pic)
        if add_or_edit[0] == 1:
            self.button_pic.setText("Add A Picture")
        if add_or_edit[0] == 2:
            self.button_pic.setText("Add Another Picture")
        self.button_pic.setStyleSheet("background-color: paleturquoise;")

        self.formGroupBox.setLayout(layout)



class ContactsWindow(QWidget):
    def __init__(self,db,Cities,Contacts,Numbers):
        super().__init__()

        self.db=db
        self.Cities=Cities
        self.Contacts=Contacts
        self.Numbers = Numbers

        self.title = "Contacts"
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
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['                                           Name                                           ',
                                                 ''])
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

        records = self.db.query(self.Contacts).filter(self.Contacts.first_name.like('%' + value + '%')).order_by(self.Contacts.first_name)
        self.tableWidget.setRowCount(1)
        i = 0
        for record in records:
            rowPosition = self.tableWidget.rowCount()
            info = record.first_name + "   " + record.last_name
            self.tableWidget.setItem(i, 0, QTableWidgetItem(info))
            btn = QPushButton(self.tableWidget)
            btn.setText('More')
            btn.setToolTip("See More Details Of Your Contact,Add More Phone Numbers,Remove Contact, Edit Contact")
            btn.setStyleSheet("background-color : lavender")
            self.tableWidget.setCellWidget(i, 1, btn)
            self.tableWidget.horizontalHeader()
            btn.clicked.connect(self.more)
            self.tableWidget.insertRow(rowPosition)
            id_holder.append(record.id)
            i += 1



    def add_new(self):
        add_or_edit.clear()
        add_or_edit.append(1)
        self.W = Add_contact(self.db, self.Cities, self.Contacts, self.Numbers)
        self.show_table()

    def show_table(self):
                id_holder.clear()
                self.tableWidget.setRowCount(0)

                records = self.db.query( self.Contacts).order_by(self.Contacts.first_name)


                self.tableWidget.setRowCount(1)
                i=0
                for record in records:
                    rowPosition = self.tableWidget.rowCount()
                    info = record.first_name + "   " + record.last_name
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(info))
                    btn = QPushButton(self.tableWidget)
                    btn.setText('More')
                    btn.setToolTip("See More Details Of Your Contact,Add More Phone Numbers,Remove Contact, Edit Contact")
                    btn.setStyleSheet("background-color : lavender")
                    self.tableWidget.setCellWidget(i, 1, btn)
                    self.tableWidget.horizontalHeader()
                    btn.clicked.connect(self.more)
                    self.tableWidget.insertRow(rowPosition)
                    id_holder.append(record.id)
                    i+=1
    def more(self):
        s = self.tableWidget.currentRow()

        if s != -1:
            add_or_edit.clear()
            show.clear()
            table_row.append(s)
            add_or_edit.append(2)

            selected_id = id_holder[table_row[0]]
            records = self.db.query(self.Contacts).order_by(self.Contacts.first_name)
            for record in records:
                if record.id == selected_id:
                    show.append(record.first_name)
                    show.append(record.last_name)
                    citys = self.db.query(self.Cities).order_by(self.Cities.name)

                    for city in citys:
                        if record.city_id == city.id:
                            show.append(city.name)

                    nums = self.db.query(self.Numbers)
                    for num in nums:
                        if num.contact_id == record.phone and num.number != "":
                            show.append(num.number)
                    for num in nums:
                        if num.contact_id == record.phone and num.number == "":
                            show.append(num.number)

                    show.append(record.image)
                    break

            self.W = Show_contact()
            self.show_table()
            table_row.clear()

    def edit_existing(self):

        s=self.tableWidget.currentRow()

        if s!=-1:
                            add_or_edit.clear()
                            type_edit.clear()
                            table_row.append(s)
                            add_or_edit.append(2)


                            selected_id = id_holder[table_row[0]]
                            records = self.db.query(self.Contacts).order_by(self.Contacts.first_name)
                            for record in records:
                                if record.id == selected_id:
                                               type_edit.append(record.first_name)
                                               type_edit.append(record.last_name)
                                               citys = self.db.query(self.Cities).order_by(self.Cities.name)

                                               for city in citys:
                                                        if record.city_id == city.id :
                                                            type_edit.append(city.name)

                                               nums= self.db.query(self.Numbers)
                                               for num in nums:
                                                   if num.contact_id==record.phone and num.number!="" :
                                                       type_edit.append(num.number)
                                               for num in nums:
                                                   if num.contact_id==record.phone and num.number=="" :
                                                       type_edit.append(num.number)

                                               type_edit.append(record.image)
                                               break


                            self.W = Add_contact(self.db, self.Cities, self.Contacts, self.Numbers)
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
                    records = self.db.query(self.Contacts).order_by(self.Contacts.first_name)
                    for record in records:
                        if record.id ==selected_id:
                            self.db.delete(record)
                            nums = self.db.query(self.Numbers)
                            for num in nums:
                                if record.phone==num.contact_id:
                                    self.db.delete(num)

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
    window = ContactsWindow()
    sys.exit(app.exec_())