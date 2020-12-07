# elearning
an e-learning website with recommender system.

## Components
1. list page of courses
2. detail page of course
4. info page of student
5. course progress of student
6. course recommendation for student
## Dependencies
- Save dependancies to a file
`pip freeze > requirement_file.txt`  
- Install all dependancies in the file
`pip install -r requirement_file.txt`  
- List of major dependencies
`pip install django`  
`pip install pandas`  
`pip install python-rake`  
`pip install scikit-learn`  
`pip install psycopg2`  
`pip install django-crispy-forms`  
`pip install pylint-django` [Link](https://stackoverflow.com/questions/45135263/class-has-no-objects-member)  
`pip install rake_nltk`  
## Initial project
`django startproject elearning`
## Initial Application
- course component `python -m django startapp course`
- users component `python -m django startapp users`
## run server
`python manage.py runserver`  
- debug: true => will reload automatically
## Database ORM
1. should add app into project's setting.py firstly
2. update modules.py
3. migrate models using commands as below  
`python manage.py makemigrations`  
`python manage.py migrate`  

## Administration
`python manage.py migrate`  
`python manage.py createsuperuser`

