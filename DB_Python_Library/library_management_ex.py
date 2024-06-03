import sqlite3
from pathlib import Path
from datetime import date

ROOT_PATH = Path(__file__).parent
DB_PATH = ROOT_PATH / "libraryDB.sqlite"

def create_tables(connection, cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        author_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES Authors(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        loan_date DATE NOT NULL,
        return_date DATE,
        FOREIGN KEY (book_id) REFERENCES Books(id)
    )
    """)
    connection.commit()

def add_author(connection, cursor, name):
    cursor.execute("INSERT INTO Authors (name) VALUES (?);", (name,))
    connection.commit()

def add_book(connection, cursor, title, author_id):
    cursor.execute("INSERT INTO Books (title, author_id) VALUES (?, ?);", (title, author_id))
    connection.commit()

def add_loan(connection, cursor, book_id):
    today = date.today()
    cursor.execute("INSERT INTO Loans (book_id, loan_date) VALUES (?, ?);", (book_id, today))
    connection.commit()

def update_book(connection, cursor, book_id, title, author_id):
    cursor.execute("UPDATE Books SET title=?, author_id=? WHERE id=?;", (title, author_id, book_id))
    connection.commit()

def delete_book(connection, cursor, book_id):
    cursor.execute("DELETE FROM Books WHERE id=?;", (book_id,))
    connection.commit()

def get_books_by_author(cursor, author_id):
    cursor.execute("SELECT * FROM Books WHERE author_id=?;", (author_id,))
    return cursor.fetchall()

def get_active_loans(cursor):
    cursor.execute("SELECT * FROM Loans WHERE return_date IS NULL;")
    return cursor.fetchall()

def list_authors(cursor):
    cursor.execute("SELECT * FROM Authors;")
    return cursor.fetchall()

def list_books(cursor):
    cursor.execute("SELECT * FROM Books;")
    return cursor.fetchall()

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

create_tables(connection, cursor)

add_author(connection, cursor, "J.K. Rowling")
add_author(connection, cursor, "J.R.R. Tolkien")
add_author(connection, cursor, "George R.R. Martin")

print("Autores:")
for author in list_authors(cursor):
    print(author)

add_book(connection, cursor, "Harry Potter and the Philosopher's Stone", 1)
add_book(connection, cursor, "Harry Potter and the Chamber of Secrets", 1)
add_book(connection, cursor, "The Hobbit", 2)
add_book(connection, cursor, "The Lord of the Rings", 2)
add_book(connection, cursor, "A Game of Thrones", 3)

print("\nLivros:")
for book in list_books(cursor):
    print(book)

add_loan(connection, cursor, 1)
add_loan(connection, cursor, 3)

print("\nEmpréstimos Ativos:")
for loan in get_active_loans(cursor):
    print(loan)

connection.close()
