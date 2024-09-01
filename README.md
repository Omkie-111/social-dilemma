# Social Networking API

This is a Django-based social networking API that allows users to sign up, log in, search for other users, and manage friend requests. The API is built using Django Rest Framework and supports token-based authentication.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Development Server](#running-the-development-server)
  - [Admin Panel](#admin-panel)
  - [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
  - [User Signup](#user-signup)
  - [User Login](#user-login)
  - [Search Users](#search-users)
  - [Send Friend Request](#send-friend-request)
  - [Accept/Reject Friend Request](#acceptreject-friend-request)
  - [List Friends](#list-friends)
  - [List Pending Friend Requests](#list-pending-friend-requests)
- [Models](#models)
- [Custom Validations](#custom-validations)
- [Public Postman Collection Link](#public-postman-collection-link)
- [Conclusion](#conclusion)

## Features

- User Signup and Login
- Search Users by Name or Email
- Send, Accept, and Reject Friend Requests
- List Friends
- List Pending Friend Requests
- Token-based Authentication

## Requirements

- Python 3.8+
- Django 4.0+
- Django Rest Framework 3.13+
- PostgreSQL (or any other supported database)
- Docker (optional, for containerized setup)

## Project Structure
```
social-dilemma/
│
├── backend/
│   ├── socialdilemma/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │
│   ├── socialApp/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └──  migrations/
│   │
│   ├── db.sqlite3
│   │
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Omkie-111/social-dilemma.git
   cd social-dilemma
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for accessing the admin panel):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### Running the Development Server

To start the development server, run:

```bash
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000/`.

### Admin Panel

You can access the Django admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials you created during installation.

### Running with Docker

If you prefer to run the application using Docker, follow these steps:

1. **Build the Docker images**:
   ```bash
   docker-compose build
   ```

2. **Run the containers**:
   ```bash
   docker-compose up -d
   ```

3. **Apply migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**:
   - The API will be accessible at `http://localhost:8000/`.
   - The admin panel will be accessible at `http://localhost:8000/admin/`.

To stop the containers, run:

```bash
docker-compose down
```

## API Endpoints

### User Signup

- **Endpoint**: `/signup/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```
- **Response**:
  - `201 Created` on successful signup.
  - `400 Bad Request` if the email is already registered or if the email format is invalid.

### User Login

- **Endpoint**: `/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```
- **Response**:
  - `200 OK` with the authentication token.
  - `400 Bad Request` if the email or password is incorrect.

### Search Users

- **Endpoint**: `/search/`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Token <user_token_at_login>`
- **Parameters**:
  - `search`: The keyword to search by name or email.
  - `page`: The page number for pagination.
- **Response**:
  - `200 OK` with a list of users matching the search keyword.
  - Users are paginated, with up to 10 results per page.

### Send Friend Request

- **Endpoint**: `/friend-request/`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: `Token <user_token_at_login>`
- **Request Body**:
  ```json
  {
    "receiver_id": 2
  }
  ```
- **Response**:
  - `201 Created` on successful friend request.
  - `400 Bad Request` if the request is invalid.
  - `403 Forbidden` if more than 3 requests are sent within a minute.

### Accept/Reject Friend Request

- **Endpoint**: `/friend-request-action/<int:pk>/`
- **Method**: `PATCH`
- **Headers**:
  - `Authorization`: `Token <receiver_token_at_login>`
- **Request Body**:
  ```json
  {
    "action": "accept"  # or "reject"
  }
  ```
- **Response**:
  - `200 OK` on successful acceptance.
  - `204 No Content` on successful rejection.
  - `403 Forbidden` if the sender tries to accept their own request.

### List Friends

- **Endpoint**: `/friends/`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Token <user_token_at_login>`
- **Response**:
  - `200 OK` with a list of friends (users who have accepted the friend request).

### List Pending Friend Requests

- **Endpoint**: `/pending-requests/`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Token <user_token_at_login>`
- **Response**:
  - `200 OK` with a list of pending friend requests received by the user.

## Models

### User Model

The `User` model is a custom user model with an email field as the unique identifier.

### FriendRequest Model

The `FriendRequest` model manages friend requests between users, with fields for the sender, receiver, and request status (accepted or pending).

## Custom Validations

### Friend Request Validation

- Users cannot send more than 3 friend requests within a minute, for this throttling is used.
- Only the receiver can accept a friend request; the sender cannot.

## Public Postman Collection Link

This is the public link to my postman collection [Postman](https://elements.getpostman.com/redirect?entityId=33676825-13e46c12-c634-4aa8-89fe-701db5e7b0e4&entityType=collection)

## Conclusion

This README provides a comprehensive guide to setting up and using the Social Networking API, including Docker setup for containerized deployment.