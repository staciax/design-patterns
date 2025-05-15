from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

# TODO: native iterator from python collections.abc


@dataclass
class Book:
    id: int
    title: str
    genre: str
    author: str


class Iterator[T](ABC):
    @abstractmethod
    def get_next(self) -> T: ...

    @abstractmethod
    def has_next(self) -> bool: ...


class Collection[T](ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator[T]: ...


class BookIterator(Iterator[Book]): ...


class AllBookIterator(BookIterator):
    def __init__(self, collection: BookCollection) -> None:
        self.books: list[Book] = collection.books.copy()
        self.index = 0

    @override
    def has_next(self) -> bool:
        return self.index < len(self.books)

    @override
    def get_next(self) -> Book:
        if not self.has_next():
            raise StopIteration('No more books')
        book = self.books[self.index]
        self.index += 1
        return book


class BookAuthorIterator(BookIterator):
    def __init__(self, collection: BookCollection, author: str) -> None:
        self.books: list[Book] = [book for book in collection.books.copy() if book.author == author if book]
        self.author = author
        self.index = 0

    @override
    def has_next(self) -> bool:
        return self.index < len(self.books)

    @override
    def get_next(self) -> Book:
        if not self.has_next():
            raise StopIteration('No more books')
        book = self.books[self.index]
        self.index += 1
        return book


class BookGenreIterator(BookIterator):
    def __init__(self, collection: BookCollection, genre: str) -> None:
        self.books: list[Book] = [book for book in collection.books.copy() if book.genre == genre if book]
        self.genre = genre
        self.index = 0

    @override
    def has_next(self) -> bool:
        return self.index < len(self.books)

    @override
    def get_next(self) -> Book:
        if not self.has_next():
            raise StopIteration('No more books')
        book = self.books[self.index]
        self.index += 1
        return book


class BookCollection(Collection[Book]):
    def __init__(self) -> None:
        self.books: list[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    @override
    def create_iterator(self) -> BookIterator:
        return AllBookIterator(self)

    def create_book_genre_iterator(self, genre: str) -> BookIterator:
        return BookGenreIterator(self, genre)

    def create_book_author_iterator(self, author: str) -> BookIterator:
        return BookGenreIterator(self, author)


def main() -> None:
    book_collection = BookCollection()
    book_collection.add_book(Book(1, '1', '1', '1'))
    book_collection.add_book(Book(2, '2', '2', '2'))
    book_collection.add_book(Book(3, '3', '3', '3'))
    book_collection.add_book(Book(4, '4', '4', '4'))
    book_collection.add_book(Book(5, '5', '5', '5'))

    all_book_iterator = book_collection.create_iterator()
    while all_book_iterator.has_next():
        print(all_book_iterator.get_next())

    author_iterator = book_collection.create_book_author_iterator('4')
    while author_iterator.has_next():
        print(author_iterator.get_next())

    genre_iterator = book_collection.create_book_genre_iterator('4')
    while genre_iterator.has_next():
        print(genre_iterator.get_next())


main()
