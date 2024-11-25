@echo off

REM Change the path to your Python virtual environment
set VENV_PATH=C:\Users\User\Documents\projects\homomorphic-encryption\venv

REM Activate the virtual environment
call %VENV_PATH%\Scripts\activate

REM Change the path to your Django project
set DJANGO_PROJECT_PATH=C:\Users\User\Documents\projects\homomorphic-encryption

REM Start the Django development server

cd %DJANGO_PROJECT_PATH%
python manage.py migrate
python manage.py runserver