# Django Library Management System

## Description

It is a library management system built with Django and primarily designed as a REST API with the Django REST framework. It allows users to reserve, cancel reservation, add to wishlist, and employees can check out books, add, update and delete books, genres and authors. The system also allows employees to view the history of a book or user.

While the core functionality is provided via a REST API, the project also includes some templates created for the front end to facilitate basic interaction with the system. The authentication system is built using Django's built-in authentication framework.

## Features

- **Genre Management**: Add, edit, and delete book genres.
- **Author Management**: Add, edit, and delete authors.
- **Book Management**: Add, edit, and delete books, including their genres and authors.
- **Reservation Management**: Reserve books, manage reservation status, and handle reservation expiration.
- **Borrow Management**: Borrow books, track borrowed status, and manage return dates.
- **Admin Interface**: Easily manage all aspects of the library through the Django admin interface.

## Admin Actions

- **Mark as Picked Up**: In the `BookReservation` admin, you can mark selected reservations as picked up. This changes the reservation status and creates a corresponding borrowing record automatically.
- **See history**: Can browse history of borrowing user or books.

## API Endpoints
The core functionality is accessible via REST API endpoints. To view the detailed API documentation, see the swagger documentation at
```python
http://127.0.0.1:8000/api/schema/swagger-ui/
```
## Installation

1. Clone the repository:
```shell
git clone https://github.com/offonyes/Library_Management
```
2. Install dependencies:
```shell
pip install -r requirements.txt
```
3. Apply migrations:
```shell
py manage.py migrate
```
4. Create SuperUser:
```shell
py manage.py migrate
```
5. Generate DataBase:
```shell
py manage.py generate_db
```
6. Run the development server:

```shell
py manage.py runserver
```

## Usage
- Navigate to the admin interface to manage genres, authors, books, reservations, and borrowings.
- Navigate to '/api/schema/swagger-ui/' to see swagger.








