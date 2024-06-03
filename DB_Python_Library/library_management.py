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

def menu():
    connection_conect = sqlite3.connect(DB_PATH)
    cursor = connection_conect.cursor()
    
    create_tables(connection_conect, cursor)

    while True:
        print("\n--- Biblioteca Interativa ---")
        print("1. Adicionar Autor")
        print("2. Adicionar Livro")
        print("3. Registrar Empréstimo")
        print("4. Atualizar Livro")
        print("5. Deletar Livro")
        print("6. Listar Livros por Autor")
        print("7. Listar Empréstimos Ativos")
        print("8. Listar Todos os Autores")
        print("9. Listar Todos os Livros")
        print("0. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            name = input("Nome do Autor: ")
            add_author(connection_conect, cursor, name)
            print(f"Autor '{name}' adicionado com sucesso!")

        elif choice == "2":
            title = input("Título do Livro: ")
            author_id = int(input("ID do Autor: "))
            add_book(connection_conect, cursor, title, author_id)
            print(f"Livro '{title}' adicionado com sucesso!")

        elif choice == "3":
            book_id = int(input("ID do Livro: "))
            add_loan(connection_conect, cursor, book_id)
            print(f"Empréstimo do livro com ID {book_id} registrado com sucesso!")

        elif choice == "4":
            book_id = int(input("ID do Livro: "))
            title = input("Novo Título do Livro: ")
            author_id = int(input("Novo ID do Autor: "))
            update_book(connection_conect, cursor, book_id, title, author_id)
            print(f"Livro com ID {book_id} atualizado com sucesso!")

        elif choice == "5":
            book_id = int(input("ID do Livro: "))
            delete_book(connection_conect, cursor, book_id)
            print(f"Livro com ID {book_id} deletado com sucesso!")

        elif choice == "6":
            author_id = int(input("ID do Autor: "))
            books = get_books_by_author(cursor, author_id)
            print(f"Livros do autor com ID {author_id}:")
            for book in books:
                print(book)

        elif choice == "7":
            loans = get_active_loans(cursor)
            print("Empréstimos ativos:")
            for loan in loans:
                print(loan)

        elif choice == "8":
            authors = list_authors(cursor)
            print("Todos os autores:")
            for author in authors:
                print(author)

        elif choice == "9":
            books = list_books(cursor)
            print("Todos os livros:")
            for book in books:
                print(book)

        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

    connection_conect.close()

menu()