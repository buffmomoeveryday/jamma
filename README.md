# Jamma
A simple proof of concept implementation of plausible analytics made using django django rest framework and celery


# How to Setup the Project
create a python virtual environment and activate it
  ```bash
python -m venv venv
source venv/bin/activate # different step is required for windows os for activation of venv
```

install the requirements file
```bash
pip install -r requirements.txt
```

make migrations and migrate
```bash
python manage.py makemigrations
python manage.py migrate 
```

start redis server
```bash
redis-server #different step is required for windows os
```

start celery worker
```bash
celery -A core worker -l info #different step is required for windows

```

run the development server
```bash
python manage.py runserver
```

