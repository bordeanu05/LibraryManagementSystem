import pymongo
from datetime import date, timedelta

connectionString = "mongodb+srv://user:pass@cluster0.qsuhjkv.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connectionString)
db = client["LibraryDB"]

def GetBooks():
    return db.books.find()

def GetIssuedBooks():
    return db.issuedBooks.find()

def AddBook(bookName, authorName, isbn):
    db.books.insert_one(
        {
            "bookName": bookName,
            "authorName": authorName,
            "isbn": isbn,
            "availability": "Available"
        }
    )

def DeleteBook(isbn):
    db.books.delete_one({"isbn": isbn})
    
def IssueBook(isbn, bookName, authorName, name, email, phone, days):
    dateIssued = date.today()
    dateDue = dateIssued + timedelta(days=int(days))
    
    db.issuedBooks.insert_one(
        {
            "bookName": bookName,
            "authorName": authorName,
            "isbn": isbn,
            "name": name,
            "email": email,
            "phone": phone,
            "dateIssued": dateIssued.strftime("%d/%m/%Y"),
            "dateDue": dateDue.strftime("%d/%m/%Y")
        }
    )
    
    db.books.update_one(
        {"isbn": isbn},
        {"$set": {"availability": "Issued"}}
    )
    
def ReturnBook(isbn):
    db.issuedBooks.delete_one({"isbn": isbn})
    db.books.update_one(
        {"isbn": isbn},
        {"$set": {"availability": "Available"}}
    )