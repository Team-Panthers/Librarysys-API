### Library Management System


## Description

This API project is designed to manage a library. It allows the creation of multiple libraries in the database with each management and admin access of each library given to the users who created them. It also handles the borrowing of books from any library by users.

## Requirements

- Python
- Django
- Docker
- Redis

## Installation
    1. Clone the repository:

        ```bash
        git clone <repository-url>
        ```

    2. Change in to the project directory and create virtual environment

        ```bash
        cd librarysys-api
        python -m venv venv
        ```

    3. Activate the virtual environment

        ```bash
        venv\Scripts\activate
        ```
    
    4. Change into library_api directory and run migrations

        ```bash
        cd library_api
        python manage.py makemigrations library, book, user
        python manage.py migrate library, book, user
        ```
    
    5. Build and run the docker container

        ```bash
        docker-compose --build
        ```

    6. The development server is up and running. Access it at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) 