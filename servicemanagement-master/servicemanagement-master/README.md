# SERVICE MANAGEMENT PORTAL
![developer](https://img.shields.io/badge/Developed%20By%20%3A-TEAM%204A%20-red)

## FUNCTIONS
## User
- User will signup and login into system
- User can make request for service of their Employee by providing details (Project Information, Start Date, End Date, Work Location, Position Domain, Postion Role, Experience Level, Technology, Skills)
- After Request is created, user can check the status of service and delete request (Enquiry) if user change their mind (ONLY PENDING REQUEST WHOSE OFFER HAS NOT BE BEEN PROVIDED CAN BE DELETED )
- User can check status of Request(Enquiry) that is Pending, or Completed
- User can check the offers given by the provider
- User can see/edit their profile
---
### Other Features
- we can change theme of website day(white) and night(black)

## HOW TO RUN THIS PROJECT
- Install Python 3.10 and above (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
pip install django
pip install django-widget-tweaks
pip install -r requirements.txt

```
- Download This Project Zip Folder and Extract it
- Move to project folder (where manage.py is presnet) in your Terminal. Then run following Commands :
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```
## Drawbacks/LoopHoles
- When customer edit their profile then he/she must login again because their username/password is updated in db.

