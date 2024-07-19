import json
import os
import re
import random
from typing import List

class Book:
    """Class represents Book"""

    def __init__(self, title: str, author: str, year: int, status: str = "в наличии", id : int = -1):
        """
        Initialize Book

        Args:
            title: Название книги.
            author: Автор книги.
            year: Год издания.
            status: Статус книги ("в наличии" или "выдана").
        """
        self.id = self._generate_id() if id == -1 else id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def _generate_id(self) -> int:
        return random.randint(1, 100000)

    def __str__(self) -> str:
        """String representation of Book"""
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"

class Library:
    """Class represents Library"""

    def __init__(self, file_name : str):
        """
        Initialize Library

        Args:
            file_name: имя файла для сохранения.
        """
        self.books = self.load_library()

    def load_library(self) -> List[Book]:
        """Load books from file on startup"""
        if os.path.exists("library.json"):
            with open("library.json", "r") as f:
                data = json.load(f)
                return [Book(**{k: v for k, v in book.items()}) for book in data]
        return []

    def save_library(self) -> None:
        """Saves book to file"""
        data = [book.__dict__ for book in self.books]
        with open("library.json", "w") as f:
            json.dump(data, f, indent=4)

    def add_book(self) -> None:
        """Adds book to library"""
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = input("Введите год издания: ")
        if not self.isYear(year):
        	print(f"Год '{year}' не является валидным.")
        	return
        new_book = Book(title, author, year)
        self.books.append(new_book)
        print(f"Книга '{title}' добавлена в библиотеку.")

    def isYear(self, string: str) -> bool:
        match = re.match(r'.*([1-3][0-9]{3})', string)
        return match

    def delete_book(self) -> None:
        """Deletes book from library"""
        book_id = int(input("Введите ID книги для удаления: "))
        for i, book in enumerate(self.books):
            if book.id == book_id:
                del self.books[i]
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_book(self) -> None:
        """Finds book by field"""
        search_term = input("Введите название, автора или год издания: ")
        found = False
        for book in self.books:
            if search_term.lower() in book.title.lower() or \
               search_term.lower() in book.author.lower() or \
               str(book.year) == search_term:
                print(book)
                found = True
        if not found:
            print("Книги, соответствующие запросу, не найдены.")

    def display_books(self) -> None:
        """Shows all books"""
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(book)

    def change_book_status(self) -> None:
        """Changes book status"""
        book_id = int(input("Введите ID книги: "))
        for book in self.books:
            if book.id == book_id:
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                if new_status.lower() in ("в наличии", "выдана"):
                    book.status = new_status
                    print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
                    return
                else:
                    print("Некорректный статус.")
                    return
        print(f"Книга с ID {book_id} не найдена.")

    def edit_book(self) -> None:
        """Changes book's fields"""
        book_id = int(input("Введите ID книги для редактирования: "))
        for book in self.books:
            if book.id == book_id:
                new_title = input(f"Введите новое название (текущее: {book.title}): ")
                new_author = input(f"Введите нового автора (текущий: {book.author}): ")
                new_year = int(input(f"Введите новый год издания (текущий: {book.year}): "))
                book.title = new_title
                book.author = new_author
                book.year = new_year
                print(f"Информация о книге с ID {book_id} обновлена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

if __name__ == "__main__":
    file_name = "library.json"
    library = Library(file_name)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Редактировать книгу")
        print(f"7. Выход (Сохранить библиотеку в файл {file_name})")

        choice = input("Выберите действие: ")

        if choice == '1':
            library.add_book()
        elif choice == '2':
            library.delete_book()
        elif choice == '3':
            library.search_book()
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            library.change_book_status()
        elif choice == '6':
            library.edit_book()
        elif choice == '7':
            library.save_library()
            break
        else:
            print("Такого варианта нет.")
