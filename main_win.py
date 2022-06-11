from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlalchemy
from sqlalchemy import create_engine
import secrets
from city import CitiesWindow
from contacts import ContactsWindow

engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname))

from sqlalchemy.orm import declarative_base
Base=declarative_base()

from sqlalchemy import Column,Integer,LargeBinary,String,ForeignKey

class Cities(Base):
    __tablename__='cities'
    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    code=Column(Integer, nullable=False ,unique=True )

class Contacts(Base):
    __tablename__='contacts'
    id=Column(Integer, primary_key=True)
    first_name=Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    city_id=Column(Integer, ForeignKey('cities.id'))
    phone=Column(String, nullable=False)
    image=Column(String)
class Numbers(Base):
    __tablename__='numbers'
    id=Column(Integer, primary_key=True)
    contact_id=Column(Integer, nullable=False)
    number=Column(String )




Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
db = session()

class window(QMainWindow):
    def __init__(self):
       super().__init__()

       buttons_info=[('Contacts','Create or edit contacts ',"background-color : lavender",0,0,self.window1),
                     ('Cities','Define Cities ',"background-color : lavender",160, 0,self.window2)]
       for i in range(len(buttons_info)):
           self.b=QPushButton(buttons_info[i][0], self)
           self.b.setToolTip(buttons_info[i][1])
           self.b.setStyleSheet(buttons_info[i][2])
           self.b.setGeometry(200, 150, 150, 40)
           self.b.move(buttons_info[i][3],buttons_info[i][4])
           self.b.clicked.connect(buttons_info[i][5])
       self.main_window()

    def main_window(self):
        self.setStyleSheet("background-color: slategray;")
        self.setWindowTitle("Contact Book")
        self.setGeometry(0, 0,309, 150)
        self.show()

    def window1(self):

        self.w = ContactsWindow(db,Cities,Contacts,Numbers)
        self.w.show()

    def window2(self):

        self.w = CitiesWindow(db,Cities)
        self.w.show()

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)

if __name__ == "__main__":
    sys.excepthook=excepthook
    app = QApplication(sys.argv)
    window = window()
    sys.exit(app.exec_())