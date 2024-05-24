const booksContainer = document.getElementById('books-container');
const buttonContainer = document.createElement('div');
buttonContainer.classList.add('button-container');
document.body.appendChild(buttonContainer);


function fetchBooks(url) {

    const accessToken = localStorage.getItem('accessToken');

    fetch(url, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
        }).then(response => response.json())
        .then(data => {
            if (!url.includes('page=')){
                booksContainer.innerHTML = '';
            }

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

                const genres = document.createElement('p');
                genres.textContent = `Genres: ${book.genres.map(genre => genre.name).join(', ')}`;

                const publishedDate = document.createElement('p');
                publishedDate.textContent = `Published Date: ${book.published_date}`;

                bookInfo.appendChild(title);
                bookInfo.appendChild(authors);
                bookInfo.appendChild(genres);
                bookInfo.appendChild(publishedDate);

                bookCard.appendChild(img);
                bookCard.appendChild(bookInfo);

                booksContainer.appendChild(bookCard);
            });

            buttonContainer.innerHTML = ''; // Clear previous button

            if (data.next) {
                const loadNextButton = document.createElement('button');
                loadNextButton.textContent = 'Load Next';
                loadNextButton.addEventListener('click', () => {
                    fetchBooks(data.next);
                });
                buttonContainer.appendChild(loadNextButton);
            }
        })
        .catch(error => {
            console.error('Error fetching books:', error);
        });
}

export { fetchBooks }