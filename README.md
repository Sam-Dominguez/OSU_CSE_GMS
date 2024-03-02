# Set UP

## Create Virtual Envrionment
Windows
`py -m venv OSU_CSE_GMS`

Mac
`python -m venv OSU_CSE_GMS`


## Activate VENV
Windows
`OSU_CSE_GMS\Scripts\activate.bat`

Mac
`source OSU_CSE_GMS/bin/activate`

## Clone the Project
`git clone https://github.com/Sam-Dominguez/OSU-CSE-GMS.git`

## Install django
Windows
`py -m pip install Django`

Mac
`python -m pip install Django`

## Run the Migrations
`python manage.py migrate && python manage.py migrate OSU_CSE_GMS`

# Post Set Up
Each time you revist the project:
1. Activate VENV
2. Pull latest from repository
3. Run the migrations
4. Run the server: `python manage.py runserver`

# Before Commit
1. Run the test cases: `python manage.py test OSU_CSE_GMS` and ensure all pass

# Database Commands

## Create Migrations
`python manage.py makemigrations OSU_CSE_GMS`

## Run the Migrations
`python manage.py migrate OSU_CSE_GMS`
