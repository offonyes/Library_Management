function fetchBooks(url) {
    const booksContainer = document.getElementById('books-container');
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');
    document.body.appendChild(buttonContainer);

    const accessToken = localStorage.getItem('accessToken');

    fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        }
    }).then(response => response.json())
      .then(data => {
          if (!url.includes('page=')) {
              booksContainer.innerHTML = '';
          }

          data.results.forEach(data => {
              const bookCard = document.createElement('div');
              bookCard.classList.add('book-card');

              const img = document.createElement('img');
              img.src = data.book.image_link;
              img.alt = data.book.title;

              const bookInfo = document.createElement('div');
              bookInfo.classList.add('book-info');
              const title = document.createElement('h3');
              title.textContent = data.book.title;
              bookInfo.appendChild(title);

              if (url.includes('reservation')) {
                  const reservedDate = document.createElement('p');
                  reservedDate.textContent = `Reservation Date: ${data.reserved_date}`;

                  const expirationDate = document.createElement('p');
                  expirationDate.textContent = `Expiration Date: ${data.expiration_date}`;

                  const reservationStatus = document.createElement('p');
                  reservationStatus.textContent = `Reservation Status: ${data.reservation_status}`;

                  bookInfo.appendChild(reservationStatus);
                  bookInfo.appendChild(reservedDate);
                  bookInfo.appendChild(expirationDate);
                  if (!url.includes('history')){
                  const cancelButton = document.createElement('button');
                  cancelButton.textContent = 'Cancel Reservation';
                  cancelButton.addEventListener('click', () => {
                      cancelReservation(data.id);
                  });
                  bookInfo.appendChild(cancelButton);
              }
              }

              if (url.includes('borrow')) {
                  const borrowedDate = document.createElement('p');
                  borrowedDate.textContent = `Borrowed Date: ${data.borrowed_date}`;

                  const returnDate = document.createElement('p');
                  returnDate.textContent = `Return Date: ${data.return_date}`;

                  const borrowedStatus = document.createElement('p');
                  borrowedStatus.textContent = `Borrowed Status: ${data.borrowed_status}`;

                  bookInfo.appendChild(borrowedStatus);
                  bookInfo.appendChild(borrowedDate);
                  bookInfo.appendChild(returnDate);
              }

              bookCard.appendChild(img);
              bookCard.appendChild(bookInfo);

              booksContainer.appendChild(bookCard);
          });

          buttonContainer.innerHTML = ``; // Clear previous button
          console.log(data.next)
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

function cancelReservation(reservationId) {
    const accessToken = localStorage.getItem('accessToken');

    fetch(`/api/reservations/${reservationId}/cancel/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            return response.json().then(data => {
                throw new Error(data.detail || 'Error cancelling reservation');
            });
        }
    })
    .catch(error => {
        alert('Failed to cancel reservation');
    });
}

export { fetchBooks }
