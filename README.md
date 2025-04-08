# School API - Django REST Framework

A RESTful API built with Django REST Framework to manage communication and content sharing between teachers and students in a school environment. Teachers can create and manage assignments and news; students can submit their answers and track updates.

## Features

### Authentication & Roles
- JWT-based authentication
- Separate roles for Teacher and Student

### Teacher Capabilities
- Register and log in
- Complete/edit personal profile
- Add students by national ID
- Create and manage:
  - News (title + body)
  - Assignments (with optional file upload and deadlines)
- Upload files in .pdf or .zip
- Edit/delete created content
- View students added to the system

### Student Capabilities
- Register and log in
- Complete/edit personal profile
- View news and assignments from teachers
- Submit assignment answers (text or file)
- Edit answers before the deadline
- Only see assignments assigned by their teachers

## Tech Stack

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- PostgreSQL / SQLite  
- Simple JWT for authentication

## Installation

```bash
git clone https://github.com/yourusername/school-api.git
cd school-api
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
