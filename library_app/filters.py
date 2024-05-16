from admin_auto_filters.filters import AutocompleteFilter


class AuthorsFilter(AutocompleteFilter):
    title = 'Artist'
    field_name = 'authors'


class GenresFilter(AutocompleteFilter):
    title = 'Genre'
    field_name = 'genres'


class BooksFilter(AutocompleteFilter):
    title = 'Book'
    field_name = 'book'


class BorrowersFilter(AutocompleteFilter):
    title = 'Borrower'
    field_name = 'borrower'
