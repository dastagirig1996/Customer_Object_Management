# Customer Object Management

Customer Object Management is a RESTful API-based project built with Django and Django REST Framework (DRF). This project allows for the management of customer details through a series of CRUD operations (Create, Read, Update, and Delete). The API is secure, allowing only authenticated users to interact with the endpoints.

## Features

- Add, view, update, and delete customer details.
- Supports both single and multiple customer retrieval.
- Authentication and permissions are enforced to restrict access.
- Handles errors like missing customers or invalid data gracefully.
- JSON response format for all API endpoints.

## Technologies Used

- **Python**: Core programming language.
- **Django**: Web framework for rapid development.
- **Django REST Framework (DRF)**: For building the RESTful APIs.
- **SQLite**: Database for storing customer data (You can switch to other databases supported by Django).
- **Authentication**: Session-based or Token-based authentication.
- **RESTful Services**: Create, retrieve, update, and delete customer information via APIs.

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.x
- Django 3.x or above
- Django REST Framework
- SQLite

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/dastagirig1996/Customer_Object_Management.git
   
2. Change to Project directory
   ```bash
   cd Customer_Object_Management


3. Actiavte Vertual Envirinment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
4. Install Dependinces
   ```bash
   pip install -r requirements.txt
   
5. Makemigrations
   ```bash
   python manage.py makemigrations
   
6. Migrate
   ```bash
   python manage.py migrate


7. Run the server
   ```bash
   python manage.py runserver



