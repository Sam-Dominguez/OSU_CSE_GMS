# Set Up Steps

Python Version 3.8 is the lowest version of Python tested. Recommend using Python Version >= 3.8

1. Create Virtual Envrionment

    a. Windows: `py -m venv OSU_CSE_GMS`

    b. Mac: `python -m venv OSU_CSE_GMS`


2. Activate VENV

    a. Windows: `OSU_CSE_GMS\Scripts\activate.bat`

    b. Mac: `source OSU_CSE_GMS/bin/activate`

3. Install the requirements

    a. Windows: `python -m pip install -r requirements.txt`

    b. Mac: `pip install -r requirements.txt`

4. Run the migrations: `python manage.py migrate && python manage.py migrate OSU_CSE_GMS`

5. Run the tests: `python manage.py test`

6. Start the server: `python manage.py runserver`

# Post Set Up
Each time you revist the project:
1. Activate VENV
2. Pull latest from repository
3. Run the migrations
4. Run the server: `python manage.py runserver`

# Before Commit
1. Run the test cases: `python manage.py test` and ensure all pass

# Database Commands

## Create Migrations
`python manage.py makemigrations OSU_CSE_GMS`

## Run the Migrations
`python manage.py migrate && python manage.py migrate OSU_CSE_GMS`
