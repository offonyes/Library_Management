from admin_auto_filters.filters import AutocompleteFilter


class AuthorsFilter(AutocompleteFilter):
    title = 'Artist'
    field_name = 'authors'


class GenresFilter(AutocompleteFilter):
    title = 'Genre'
    field_name = 'genres'
