from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import calendar
from PyQt5.QtCore import QDate
import sys,os
import sqlite3
from PyQt5 import QtPrintSupport

person_id = None
con = sqlite3.connect('batra.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS employee (id integer PRIMARY KEY AUTOINCREMENT,
 name text, phone text, salary text, address text )''')
con.commit()

class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management")
        self.setGeometry(400, 150, 1050, 800)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.Layouts()
        self.getEmp()
        self.displayRecord()

        self.show()

    def getEmp(self):
        query = "SELECT id,name FROM employee"
        emp = cur.execute(query).fetchall()
        for employees in emp:
            self.empList.addItem(str(employees[0]) +"-"+employees[1])

    def displayRecord(self):
        try:
            query = "SELECT * FROM employee ORDER BY ROWID ASC LIMIT 1"
            emp = cur.execute(query).fetchone()

            name = QLabel(emp[1])
            phone = QLabel(emp[2])
            salary = QLabel(emp[3])
            address = QLabel(emp[4])
        
            self.leftLayout.setVerticalSpacing(22)

            self.leftLayout.addRow("Name :",name)
            self.leftLayout.addRow("Phone :",phone)
            self.leftLayout.addRow("Salary :",salary)
            self.leftLayout.addRow("Address :",address)
        except:
            QMessageBox.information(self,"Information","No Records")

    def mainDesign(self):

        self.setStyleSheet("font-size:14pt;font-family:Times Bold;background-color:#ffdb85")
        self.empList = QListWidget()
        self.empList.itemClicked.connect(self.singleClicked)
        self.empList.itemDoubleClicked.connect(self.doubleClicled)
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmp)
        self.btnNew.setStyleSheet("background-color:#8B4513")

        self.btnUpdate = QPushButton("Update")
        self.btnUpdate.clicked.connect(self.updateEmployee)
        self.btnUpdate.setStyleSheet("background-color:#8B4513")

        self.btnDelete = QPushButton("Delete")
        self.btnDelete.clicked.connect(self.deleteEmployee)
        self.btnDelete.setStyleSheet("background-color:#8B4513")

        self.img = QLabel()
        self.img.setPixmap(QPixmap("images/user.png"))

    def Layouts(self):
        #################Total Layouts###################
        self.mainLayout = QHBoxLayout()
        self.leftTopLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.leftMainLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightTopLayout = QVBoxLayout()
        self.rightBottomLayout = QHBoxLayout()

        ################Adding layouts#####################

        self.leftMainLayout.addLayout(self.leftTopLayout)
        self.leftMainLayout.addLayout(self.leftLayout)

        self.mainRightLayout.addLayout(self.rightTopLayout)
        self.mainRightLayout.addLayout(self.rightBottomLayout)



        ###################Adding widgets###################

        self.rightTopLayout.addWidget(self.empList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)
        self.leftTopLayout.addStretch()
        self.leftTopLayout.addWidget(self.img)
        self.leftTopLayout.addStretch()

        self.mainLayout.addLayout(self.leftMainLayout, 45)
        self.mainLayout.addLayout(self.mainRightLayout, 55)

        self.setLayout(self.mainLayout)

    def updateEmployee(self):
        global person_id
        if self.empList.selectedItems():
            person = self.empList.currentItem().text()
            person_id = person.split("-")[0]
            self.updateWindow = updateEmployee()
            self.close()

        else:
            QMessageBox.information(self, "Information", "Please select a Employee to update")

    def deleteEmployee(self):
        if self.empList.selectedItems():

            person = self.empList.currentItem().text()
            id = person.split("-")[0]
            mbox = QMessageBox.question(self,"Warninig","Are you sure you want to delete ??",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM employee WHERE id=?"
                    cur.execute(query,(id,))
                    con.commit()
                    QMessageBox.information(self,"Information","Employee has been deleted")
                    self.close()
                    self.main = Main()
                except:
                    QMessageBox.information(self,"Information","Employee cannot be deleted")
        else:
            QMessageBox.information(self, "Information", "Please select a Employee to delete")

    def doubleClicled(self):
        global person_id
        if self.empList.selectedItems():
            person = self.empList.currentItem().text()
            person_id = person.split("-")[0]
            self.records = recordEmp()
            self.close()

    def singleClicked(self):
        for i in reversed(range(self.leftLayout.count())):
            widget = self.leftLayout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()


        employee = self.empList.currentItem().text()
        id = employee.split("-")[0]
        query = "SELECT * FROM employee WHERE id = ?"
        person = cur.execute(query,(id,)).fetchone() #single item tuple

        name = QLabel(person[1])
        phone = QLabel(person[2])
        salary = QLabel(person[3])
        address = QLabel(person[4])
        self.leftLayout.setVerticalSpacing(22)
        self.leftLayout.addRow("Name :", name)
        self.leftLayout.addRow("Phone :", phone)
        self.leftLayout.addRow("Salary :", salary)
        self.leftLayout.addRow("Address :", address)




    def addEmp(self):
        self.newEmp = addEmployee()
        self.close()


class recordEmp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Records")
        self.setGeometry(600, 150, 400, 400)
        self.UI()
        self.show()

    def UI(self):

        self.mainDesign()
        self.layout()

    def closeEvent(self, event):
        self.main = Main()


    def mainDesign(self):
        global person_id


        query = "SELECT * FROM employee WHERE id = ?"
        emp = cur.execute(query, (person_id,)).fetchone()


        self.setStyleSheet("font-size :12pt;font-family:times Italic")
        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLabel(emp[1])
        self.salaryLbl = QLabel("Salary :")
        self.salaryEntry = QLabel(emp[3])
        self.presentedDaysLbl = QLabel("Presented/Working Days :")
        self.workDaysEntry = QLineEdit()
        self.netSalaryLbl = QLabel("Net Salary :")
        self.salaryToBeGiven = QLabel()
        #self.salaryToBeGiven.setText(self.r)
        #self.calenderLbl = QLabel("Show Record :")
        self.calBtn = QPushButton("Calculate")
        self.calBtn.clicked.connect(self.calc)
        self.printBtn = QPushButton("Print")
        self.printBtn.clicked.connect(self.printFun)

    def calc(self):
        self.x = float(self.salaryEntry.text())
        self.y = float(self.workDaysEntry.text())

        if self.y <= 30:
            self.r = (self.x*self.y)/30
        #print(self.y)
            self.salaryToBeGiven.setText(str(self.r))
        else:
            QMessageBox.information(self, "Warning", "Days cannot be more than 30")

    def printFun(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.mainDesign.document(),print_(dialog.printer())

    def layout(self):
        self.layout = QFormLayout()

        self.layout.addRow(self.nameLbl, self.nameEntry)
        self.layout.addRow(self.salaryLbl, self.salaryEntry)
        self.layout.addRow(self.presentedDaysLbl, self.workDaysEntry)
        self.layout.addRow(self.netSalaryLbl, self.salaryToBeGiven)
        #self.layout.addRow(self.calenderLbl, self.calBtn)
        self.layout.addRow(self.printBtn, self.calBtn)
        self.layout.setVerticalSpacing(22)
        self.setLayout(self.layout)


class updateEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Employee")
        self.setGeometry(400, 150, 450, 800)
        self.UI()
        self.show()

    def UI(self):
        self.getPerson()
        self.mainDesign()
        self.layout()

    def closeEvent(self, event):
        self.main = Main()

    def getPerson(self):
        global person_id
        query = "SELECT * FROM employee WHERE id = ?"
        emp = cur.execute(query,(person_id,)).fetchone()
        self.name = emp[1]
        self.phone = emp[2]
        self.salary = emp[3]
        self.address = emp[4]
    def mainDesign(self):
        self.setStyleSheet("font-size:14pt;font-family:Arial")
        self.title = QLabel("Update Employee")
        self.title.setStyleSheet("font-family:tahoma Bold;font-size:22pt")
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("images/images.png"))
        self.nameLabel = QLabel("Name")

        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.name)
        self.phoneLabel = QLabel("Phone")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phone)
        self.salaryLabel = QLabel("Salary")
        self.salaryEntry = QLineEdit()
        self.salaryEntry.setText(self.salary)
        self.addressLabel = QLabel("Address")
        self.addressEntry = QTextEdit()
        self.addressEntry.setText(self.address)
        self.addBtn = QPushButton("Update")
        self.addBtn.clicked.connect(self.updateEmp)
        self.addBtn.setStyleSheet("background-color:pink")


    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

        ##########################################################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)

        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(110, 10, 10, 50)
        self.bottomLayout.addRow(self.nameLabel, self.nameEntry)
        self.bottomLayout.addRow(self.phoneLabel, self.phoneEntry)
        self.bottomLayout.addRow(self.salaryLabel, self.salaryEntry)
        self.bottomLayout.addRow(self.addressLabel, self.addressEntry)
        self.bottomLayout.addRow("", self.addBtn)

    def updateEmp(self):
        global person_id
        self.name = self.nameEntry.text()
        self.phone = self.phoneEntry.text()
        self.salary = self.salaryEntry.text()
        self.address = self.addressEntry.toPlainText()

        if(self.name and self.phone !=""):
            try:
                query = "UPDATE employee set name = ?,phone = ?,salary = ?,address = ? WHERE id = ?"
                cur.execute(query,(self.name,self.phone,self.salary,self.address,person_id))
                con.commit()
                QMessageBox.information(self,"Success","Employee updated successfully")
                self.close()
                self.main = Main()

            except:
                QMessageBox.information(self, "Warning", "Employee cannot be updated")
                    
        else:
            QMessageBox.information(self, "Warning", "Fields cannot be empty")



class addEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(400, 150, 450, 800)
        self.UI()
        self.show()



    def UI(self):
        self.mainDesign()
        self.layout()

    def closeEvent(self, event):
        self.main = Main()


    def mainDesign(self):
        self.setStyleSheet("font-size:14pt;font-family:Arial")
        self.title = QLabel("Add Employee")
        self.title.setStyleSheet("font-family:tahoma Bold;font-size:22pt")
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("images/images.png"))
        self.nameLabel = QLabel("Name")
        self.nameEntry = QLineEdit()
        self.phoneLabel = QLabel("Phone")
        self.phoneEntry = QLineEdit()
        self.salaryLabel = QLabel("Salary")
        self.salaryEntry = QLineEdit()
        self.addressLabel = QLabel("Address")
        self.addressEntry = QTextEdit()
        self.addBtn = QPushButton("Add")
        self.addBtn.setStyleSheet("background-color:aqua")
        self.addBtn.clicked.connect(self.addEmp)




    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

        ##########################################################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)

        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(110,10,10,50)
        self.bottomLayout.addRow(self.nameLabel, self.nameEntry)
        self.bottomLayout.addRow(self.phoneLabel, self.phoneEntry)
        self.bottomLayout.addRow(self.salaryLabel, self.salaryEntry)
        self.bottomLayout.addRow(self.addressLabel, self.addressEntry)
        self.bottomLayout.addRow("", self.addBtn)

    def addEmp(self):
        self.name = self.nameEntry.text()
        self.phone = self.phoneEntry.text()
        self.salary = self.salaryEntry.text()
        self.address = self.addressEntry.toPlainText()

        if(self.name and self.phone !=""):
            try:
                query = "INSERT INTO employee (name,phone,salary,address) VALUES(?,?,?,?)"
                cur.execute(query,(self.name,self.phone,self.salary,self.address))
                con.commit()
                QMessageBox.information(self,"Success","Employee added successfully")
                self.close()
                self.main = Main()

            except:
                QMessageBox.information(self, "Warning", "Employee cannot be added")

        else:
            QMessageBox.information(self, "Warning", "Fields cannot be empty")






def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
