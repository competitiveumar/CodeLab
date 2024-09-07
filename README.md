# eLearning App - Code Lab

## Introduction
This project is an eLearning application developed using Django (Python). The application covers various topics including single-page applications, database schemas, appropriate model design, forms and templates, RESTful web services, Django Channels, Web Sockets, and Authentication.

## Features
- **Single Page Applications**
- **Database Schemas**
- **Model Design**
- **Forms and Templates**
- **RESTful Web Services**
- **Django Channels**
- **Web Sockets**
- **User Authentication**

## User Registration Details and Login Credentials for Teachers and Students
Log in to the teacher/students account using the Username and Password.

### Students
1. **Ava Morgan**
   - Username: Ava
   - Email: avamorgan@gmail.com
   - Password: `@1b2c3d4`

2. **Jake Miller**
   - Username: Jake
   - Email: jakemiller@gmail.com
   - Password: `@1b2c3d4`

3. **Emma Collins**
   - Username: Emma
   - Email: emmacollins@gmail.com
   - Password: `@1b2c3d4`

### Teachers
1. **Lily Harper**
   - Username: Lily
   - Email: lilyharper@gmail.com
   - Password: `1@b2c3d4`

2. **Alex Watson**
   - Username: Alex
   - Email: alexwatson@gmail.com
   - Password: `1@b2c3d4`

3. **Ned Parker**
   - Username: Ned
   - Email: nedparker@gmail.com
   - Password: `1@b2c3d4`

## API Endpoints

- **List all courses:**  
  `http://127.0.0.1:8000/api/courses/`

- **List all user profiles:**  
  `http://127.0.0.1:8000/api/userprofiles/`

- **List all feedbacks:**  
  `http://127.0.0.1:8000/api/feedbacks/`

- **List of students and teachers:**  
  `http://127.0.0.1:8000/api/students-and-teachers/`

## Installation
To set up the project locally, follow these steps:

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the migrations:
   python3 manage.py makemigrations
   python3 manage.py migrate
4. Run the application: python3 manage.py runserver
5. Access the application at `http://127.0.0.1:8000`.

Unit Testing: python3 manage.py test

Operating System: Windows 11 (Ubuntu)
Python version: 3.12.4

## References
- Used Bootstrap template for HTML, CSS and JS.
