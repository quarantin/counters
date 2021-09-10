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
    ./manage.py runserver
