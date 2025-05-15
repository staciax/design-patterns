class Book:
    def __init__(self, id: int, title: str, author_id: int, publisher_id: int) -> None:
        self.id = id
        self.title = title
        self.author_id = author_id
        self.publisher_id = publisher_id

    def __repr__(self) -> str:
        return f'Book(id={self.id!r}, title={self.title!r})'


class Author:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'Author(id={self.id!r}, name={self.name!r})'


class Publisher:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'Publisher(id={self.id!r}, name={self.name!r})'


class BookAPI:
    data = [
        Book(1, 'book 1', 1, 1),
        Book(2, 'book 2', 1, 1),
        Book(3, 'book 3', 2, 2),
    ]

    def read_all(self) -> list[Book]:
        return self.data

    def read(self, id: int) -> Book | None:
        for book in self.data:
            if book.id == id:
                return book
        return None

    def add(self, title: str, authod_id: int, publisher_id: int) -> Book:
        max_id = max(book.id for book in self.data)
        new_book = Book(id=max_id + 1, title=title, author_id=authod_id, publisher_id=publisher_id)
        self.data.append(new_book)
        return new_book


class AuthorAPI:
    data = [
        Author(1, 'author 1'),
        Author(2, 'author 2'),
        Author(3, 'author 3'),
    ]

    def read_all(self) -> list[Author]:
        return self.data

    def read(self, id: int) -> Author | None:
        for author in self.data:
            if author.id == id:
                return author
        return None

    def add(self, name: str) -> None:
        max_id = max(author.id for author in self.data)
        self.data.append(Author(id=max_id + 1, name=name))


class PublisherAPI:
    data = [
        Publisher(1, 'publisher 1'),
        Publisher(2, 'publisher 2'),
        Publisher(3, 'publisher 3'),
    ]

    def read_all(self) -> list[Publisher]:
        return self.data

    def read(self, id: int) -> Publisher | None:
        for publisher in self.data:
            if publisher.id == id:
                return publisher
        return None

    def add(self, name: str) -> None:
        max_id = max(publisher.id for publisher in self.data)
        self.data.append(Publisher(id=max_id + 1, name=name))


class BookStoreAPIFacade:
    def __init__(
        self,
        book_api: BookAPI | None = None,
        author_api: AuthorAPI | None = None,
        publisher_api: PublisherAPI | None = None,
    ) -> None:
        self.book_api: BookAPI = book_api or BookAPI()
        self.author_api: AuthorAPI = author_api or AuthorAPI()
        self.publisher_api: PublisherAPI = publisher_api or PublisherAPI()

    def create_book(
        self,
        title: str,
        author_id: int,
        publisher_id: int,
    ) -> Book:
        author = self.author_api.read(id=author_id)
        if author is None:
            raise ValueError(f'Author not found with id: {author_id}')

        publisher = self.publisher_api.read(id=publisher_id)
        if publisher is None:
            raise ValueError(f'Publisher not found with id: {publisher_id}')

        new_book = self.book_api.add(
            title=title,
            authod_id=author_id,
            publisher_id=publisher_id,
        )
        print(f'Add new book: {new_book}')
        return new_book


def main() -> None:
    book_store_facade = BookStoreAPIFacade()

    books = book_store_facade.book_api.read_all()
    print('books:', books)

    book_store_facade.create_book(
        title='new book',
        author_id=1,
        publisher_id=1,
    )

    # book_store_facade.create_book(
    #     title='new book',
    #     author_id=5,
    #     publisher_id=1,
    # )


if __name__ == '__main__':
    main()
