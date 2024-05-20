document.addEventListener('DOMContentLoaded', () => {
    const booksContainer = document.getElementById('books-container');

    function fetchBooks(url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                booksContainer.innerHTML = '';
                data.results.forEach(book => {
                    const bookCard = document.createElement('div');
                    bookCard.classList.add('book-card');

                    const img = document.createElement('img');
                    img.src = book.image_link;
                    img.alt = book.title;

                    const bookInfo = document.createElement('div');
                    bookInfo.classList.add('book-info');
                    const title = document.createElement('h3');
                    title.textContent = book.title;

                    const authors = document.createElement('p');
                    authors.textContent = `Authors: ${book.authors.map(author => author.name).join(', ')}`;

                    const publishedDate = document.createElement('p');
                    publishedDate.textContent = `Published Date: ${book.published_date}`;

                    bookInfo.appendChild(title);
                    bookInfo.appendChild(authors);
                    bookInfo.appendChild(publishedDate);

                    bookCard.appendChild(img);
                    bookCard.appendChild(bookInfo);

                    booksContainer.appendChild(bookCard);
                });

                if (data.previous) {
                    const loadPreviousButton = document.createElement('button');
                    loadPreviousButton.textContent = 'Load Previous';
                    loadPreviousButton.addEventListener('click', () => {
                        fetchBooks(data.previous);
                    });
                    booksContainer.appendChild(loadPreviousButton);
                }

                if (data.next) {
                    const loadNextButton = document.createElement('button');
                    loadNextButton.textContent = 'Load Next';
                    loadNextButton.addEventListener('click', () => {
                        fetchBooks(data.next);
                    });
                    booksContainer.appendChild(loadNextButton);
                }
            })
            .catch(error => {
                console.error('Error fetching books:', error);
            });
    }

    fetchBooks('/api/books');
});