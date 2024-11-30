# Gas Service Management Portal

A Django application designed to manage gas service requests efficiently. This portal allows **users** to raise requests for gas services and track them in real-time. Additionally, **admins** can view and update the status of these requests.

---

## Features

### User Features:
- Raise requests for services (e.g., new gas connection, maintenance, repairs).
- Track the status of their requests in real-time on the dashboard.

### Admin Features:
- View all user requests in an organized admin dashboard.
- Update the status of user requests (e.g., pending, approved, or rejected).

---

## Getting Started

### Prerequisites
- Python 3.x installed on your system.
- Django installed (will be managed through a virtual environment).


  ## Installation Steps

1. Clone this repository to your local machine: `git clone https://github.com/atharva020/Gas-service-CRM.git`.

2. Navigate to the project directory: `cd myproject`.

3. Create and activate a virtual environment: `python -m venv venv` and `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).

4. Apply the database migrations: `python manage.py migrate`.

6. Start the Django development server: `python manage.py runserver`.

7. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the application.
