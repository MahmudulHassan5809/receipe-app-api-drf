## Project Description


## Project Setup
	1. git clone https://github.com/MahmudulHassan5809/recipe-app-api-drf.git
    2. create virtual env using this command
        -> python3 -m venv ./venv 
        -> python -m venv ./venv (for windows)
    3. activate virtual env 
    	1.venv\Scripts\activate (windows)
    	2.source venv/bin/activate (Linux)
    4. Istall all the requirements using this commans -> pip install -r requirements.txt
    5. cd app (enter the app directory)
    5. Run python manage.py migrate
    6  Run python manage.py createsuperuser (for superuser creation)
    7. Run python manage.py runserver
    8. project will run in http://127.0.0.1:8000/
    9. To test run python manage.py test




## Api Documentation (swagger)
    http://127.0.0.1:8000/swagger/
    
## API Doc
    You can get all the endpoints with request method, request body, request response
    http://127.0.0.1:8000/redoc/



## Your Task 
    1. Implement the API related To Account Section
        1. User create (http://127.0.0.1:8000/api/accounts/create/) POST request
        2. Get User Profile (http://127.0.0.1:8000/api/accounts/me/) GET request
        3. Update User Profile (http://127.0.0.1:8000/api/accounts/me/) PUT/PATCH request
        4. User (Login) Token Create http://127.0.0.1:8000/api/accounts/token/) POST request (You need to store the token in somewhere link local storage so that you can send it later for private api)
    
    2. Implement the API related To Recipe Section
        Please check the doc (http://127.0.0.1:8000/redoc/) for this api section
    
    
    		     
   