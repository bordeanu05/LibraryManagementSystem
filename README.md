# Library Management System
This is a Library Management System application built with [Python](https://www.python.org/downloads/) and [Qt](https://wiki.python.org/moin/PyQt) framework for the GUI,
and [MongoDB](https://www.mongodb.com/) for the database.
The purpose of the application is to manage the library's collection and transacctins such as borrowing and returning books.

# Installation
Make sure you have [Python](https://www.python.org/downloads/) installed
1. Clone the repository:
```
git clone https://github.com/bordeanu05/LibraryManagementSystem.git
```
2. Install required packages:
```
pip install pyqt5
pip install pymongo
```
3. Create your MongoDB database and name it "LibraryDB". Also make sure to create
two collections: "books" and "issuedBooks"
4. Modify the connection string inside db_Functios.py with your own connection string
5. Finally, run ```python main.py``` and you should have the window open

# Features:
- Adding books into the database
- Deleting books from the database
- Viewing all existing books inside the database
- Issuing books to someone
- Viewing all the issued books and their due date

I made this project so i can learn the Qt framework, experiment with MongoDB and for upping my Python skills
