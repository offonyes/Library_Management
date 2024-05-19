BORROWS_STATUS_TYPE = (
    ('borrowed', 'Borrowed a book'),
    ('returned', 'Returned a book'),
    ('overdue', 'Overdue borrowed'),
)

RESERVATION_STATUS_TYPE = (
    ('reserved', 'Reserved a book'),
    ('reservation_expired', 'Reservation expired'),
    ('reservation_canceled', 'Reservation canceled'),
    ('wishlist', 'Out of stock, added to wishlist'),
    ('picked_up', 'Picked up the book'),
)
