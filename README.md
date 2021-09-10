# Counters
Simple counters to count things manually.

# Setup
    git clone https://github.com/quarantin/counters
    cd counters
    virtualenv -p /usr/bin/python3.8 .venv
    . .venv/bin/activate
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py collectstatic
    ./manage.py runserver

# Usage
    Visit the following URL with your web browser:
    http://127.0.0.1:8000/admin/

    Login with your Django superuser account
    Add a new user
    Logout

    Login as the new user and visit this URL:
    http://127.0.0.1:8000/counters/
