# Django Library Management System

## Description

It is a library management system built with Django and primarily designed as a REST API with the Django REST framework. It allows users to reserve, cancel reservation, add to wishlist, and employees can check out books, add, update and delete books, genres and authors. The system also allows employees to view the history of a book or user.

While the core functionality is provided via a REST API, the project also includes some templates created for the front end to facilitate basic interaction with the system. The authentication system is built using Django's built-in authentication framework.
Project has 2 main apps: accounts_app and library_app. There's also third app called front_app, which is just used front.
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

## Rules
- User cannot reserve a book if he has more than `5` borrowed or reserved books(`2` same books).
- User can reserve a book and has 24 hours to pick it up. By using the `check_reservation` command, if a person's reservation time has passed, then the reservation status will change to expired.
- User cann't borrow books more than `2 weeks`. By using the `check_borrow` command, a person will receive an email message that he is overdue for the return of the book.
- User can add to wishlist. By using the `check_wishlist` command, a person will receive a message by email (if he has books in his wishlist) that he can reserve this book.
- The admin using the admin panel can `issue as many books as he wants`.

## API Endpoints
The core functionality is accessible via REST API endpoints. To view the detailed API documentation, see the swagger documentation at
```python
http://127.0.0.1:8000/api/schema/swagger-ui/
```
## Installation
- Python 3.12
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








