BORROWS_STATUS_TYPE = (
    ('borrowed', 'Borrowed a book'),  # Borrowed Book
    ('returned', 'Returned a book'),  # Returned in time
    ('overdue', 'Overdue book'),  # 2 weeks passed and didn't return yet
    ('overdue_returned', 'Returned overdue book'),  # Returned after 2 weeks
)

RESERVATION_STATUS_TYPE = (
    ('reserved', 'Reserved a book'),
    ('reservation_expired', 'Reservation expired'),
    ('reservation_canceled', 'Reservation canceled'),
    ('wishlist', 'Out of stock, added to wishlist'),
    ('picked_up', 'Picked up the book'),
)
