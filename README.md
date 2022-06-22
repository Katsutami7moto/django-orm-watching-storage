# Bank security console

This is an in-house repository for "Shining" bank's employees. If you accidentally stumbled upon this repository, you won't be able to run it, as you don't have access to the database, but you are free to use layout code or examine, how the requests to the database are implemented.

Security console is a website that can be connected to remote database containing visits and passcards of our bank's employees.

### How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Before you run the website, you will have to configure environmental variables:

1. Go to the downloaded repository directory and create a file with the name `.env` (yes, it has only the extension).
It is the file to contain environmental variables that usually store data unique to each user, thus you will need to create your own.
2. Copy and paste this to `.env` file:
```dotenv
DJANGO_DB_HOST='{db_host_url}'
DJANGO_DB_PORT='{db_port_number}'
DJANGO_DB_NAME='{db_name}'
DJANGO_DB_USER='{db_user_name}'
DJANGO_DB_PASSWORD='{db_user_password}'
DJANGO_DB_SECRET_KEY='{db_secret_key}'
DJANGO_DB_DEBUG=False
DJANGO_DB_ALLOWED_HOSTS='127.0.0.1, 0.0.0.0, localhost'
```
3. Replace all `{text}` parts with connection settings you have got from your system administrator.
4. Set `DJANGO_DB_DEBUG=True` if you are developer or if you may need debugging information.
5. Ensure the value of `DJANGO_DB_ALLOWED_HOSTS` with your system administrator.

### How to use

Open terminal from downloaded repository directory and execute this command to run the website:
```commandline
python3 manage.py runserver 0.0.0.0:8000
```

Then open the website with [this link](http://127.0.0.1:8000/) (or [this link](http://0.0.0.0:8000/), if former was invalid).

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
