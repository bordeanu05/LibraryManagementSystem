from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

import sys
import db_Functions

def goToWindow(window):
    lastWindow = windowStack.currentWidget()
    windowStack.addWidget(window)
    windowStack.removeWidget(lastWindow)

class MenuWindow(QDialog):
    def __init__(self):
        super(MenuWindow, self).__init__()
        loadUi("UI_Files/menu.ui", self)
        
        self.viewBooksButton.clicked.connect(self.gotoViewBooks)
        self.addNewBookButton.clicked.connect(self.gotoAddNewBook)
        self.viewIssuedBooksButton.clicked.connect(self.gotoViewIssuedBooks)
        
    def gotoViewBooks(self):
        goToWindow(ViewBooksWindow())
        
    def gotoAddNewBook(self):
        goToWindow(AddWindow())
    
    def gotoViewIssuedBooks(self):
        goToWindow(ViewIssuedBooksWindow())
        
class AddWindow(QDialog):
    def __init__(self):
        super(AddWindow, self).__init__()
        loadUi("UI_Files/add.ui", self)
        
        self.addButton.clicked.connect(self.addBook)
        self.goBackButton.clicked.connect(self.goBack)
        
    def addBook(self):
        bookName = self.bookNameTextBox.text()
        authorName = self.authorNameTextBox.text()
        isbn = self.isbnTextBox.text()
        
        if len(bookName) == 0 or len(authorName) == 0 or len(isbn) == 0:
            self.errorLabel.setText("Please fill all the fields")
        else:
            try:
                db_Functions.AddBook(bookName, authorName, isbn)
                goToWindow(MenuWindow())
            except:
                self.errorLabel.setText("Error adding book")
    
    def goBack(self):
        goToWindow(MenuWindow())
        
class ViewBooksWindow(QDialog):
    def __init__(self):
        super(ViewBooksWindow, self).__init__()
        loadUi("UI_Files/viewBooks.ui", self)

        self.goBackButton.clicked.connect(self.goBack)
        self.deleteBookButton.clicked.connect(self.deleteBook)
        self.issueBookButton.clicked.connect(self.issueBook)
        
        self.loadBooks()
        
    def loadBooks(self):
        books = db_Functions.GetBooks()
        rowCount = 0
        self.booksTable.setColumnCount(4)
        self.booksTable.setHorizontalHeaderLabels(["Book Name", "Author Name", "ISBN", "Availability"])
        for book in books:
            self.booksTable.insertRow(rowCount)
            self.booksTable.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(book["bookName"]))
            self.booksTable.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(book["authorName"]))
            self.booksTable.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(book["isbn"]))
            self.booksTable.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(book["availability"]))
            rowCount += 1
        
    def deleteBook(self):
        selectedBook = self.booksTable.selectedItems()
        if len(selectedBook) > 0:
            isbn = selectedBook[2].text()
            try:
                db_Functions.DeleteBook(isbn)
                self.booksTable.removeRow(selectedBook[0].row())
            except:
                pass
            
    
    def issueBook(self):
        selectedBook = self.booksTable.selectedItems()
        if len(selectedBook) > 0:
            info = [selectedBook[0].text(), selectedBook[1].text(), selectedBook[2].text(), selectedBook[3].text()]
            if info[3] == "Available":
                goToWindow(IssueBookWindow(info))
    
    def goBack(self):
        goToWindow(MenuWindow())

class IssueBookWindow(QDialog):
    bookInfo = []
    
    def __init__(self, info):
        super(IssueBookWindow, self).__init__()
        loadUi("UI_Files/issue.ui", self)
        self.bookInfo = info
        self.cancelButton.clicked.connect(self.goBack)
        self.issueButton.clicked.connect(self.issueBook)
        self.bookName.setText("Book name: " + self.bookInfo[0])
        self.authorName.setText("Author name: " + self.bookInfo[1])
        self.isbn.setText("ISBN: " + self.bookInfo[2])
                
    def issueBook(self):
        if len(self.nameTextBox.text()) == 0 or len(self.emailTextBox.text()) == 0 or len(self.phoneTextBox.text()) == 0 or len(self.daysTextBox.text()) == 0:
            self.errorLabel.setText("Please fill all the fields")
        else:
            try:
                db_Functions.IssueBook(self.bookInfo[2], self.bookInfo[0], self.bookInfo[1], self.nameTextBox.text(), self.emailTextBox.text(), self.phoneTextBox.text(), self.daysTextBox.text())
                goToWindow(ViewBooksWindow())
            except:
                self.errorLabel.setText("Error issuing book")
        
    def goBack(self):
        goToWindow(ViewBooksWindow())
        
class ViewIssuedBooksWindow(QDialog):
    def __init__(self):
        super(ViewIssuedBooksWindow, self).__init__()
        loadUi("UI_Files/viewIssued.ui", self)
        self.loadIssuedBooks()
        self.goBackButton.clicked.connect(self.goBack)
        self.returnBookButton.clicked.connect(self.returnBook)
    
    def loadIssuedBooks(self):
        issuedBooks = db_Functions.GetIssuedBooks()
        rowCount = 0
        self.issuedBooksTable.setColumnCount(8)
        self.issuedBooksTable.setHorizontalHeaderLabels(["Book Name", "Author Name", "ISBN", "Borrower Name", "Borrower Email", "Borrower Phone", "Date Issued", "Date Due"])
        for issuedBook in issuedBooks:
            self.issuedBooksTable.insertRow(rowCount)
            self.issuedBooksTable.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(issuedBook["bookName"]))
            self.issuedBooksTable.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(issuedBook["authorName"]))
            self.issuedBooksTable.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(issuedBook["isbn"]))
            self.issuedBooksTable.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(issuedBook["name"]))
            self.issuedBooksTable.setItem(rowCount, 4, QtWidgets.QTableWidgetItem(issuedBook["email"]))
            self.issuedBooksTable.setItem(rowCount, 5, QtWidgets.QTableWidgetItem(issuedBook["phone"]))
            self.issuedBooksTable.setItem(rowCount, 6, QtWidgets.QTableWidgetItem(issuedBook["dateIssued"]))
            self.issuedBooksTable.setItem(rowCount, 7, QtWidgets.QTableWidgetItem(issuedBook["dateDue"]))
            rowCount += 1  
    
    def returnBook(self):
        selectedBook = self.issuedBooksTable.selectedItems()
        if len(selectedBook) > 0:
            isbn = selectedBook[2].text()
            try:
                db_Functions.ReturnBook(isbn)
                self.issuedBooksTable.removeRow(selectedBook[0].row())
            except:
                pass
        else:
            self.errorLabel.setText("Please select a row")
        
    def goBack(self):
        goToWindow(MenuWindow())
        
        
def main():
    app = QApplication(sys.argv)

    menu = MenuWindow()

    global windowStack

    windowStack = QtWidgets.QStackedWidget()
    windowStack.setWindowTitle("Library Management System")
    windowStack.setWindowIcon(QtGui.QIcon("imgs/icon.ico"))
    windowStack.setFixedSize(840, 460)
    windowStack.addWidget(menu)
    windowStack.show()

    app.exec_()
        
if __name__ == "__main__":
    main()