# SERVICE MANAGEMENT PORTAL
![developer](https://img.shields.io/badge/Developed%20By%20%3A-TEAM%204A%20-red)

## FUNCTIONS
## User
- User will signup and login into system
- User can make request for service of their Employee by providing details (Project Information, Start Date, End Date, Work Location, Position Domain, Postion Role, Experience Level, Technology, Skills)
- After Request is created, user can check the status of service and delete request (Enquiry) if user change their mind (ONLY PENDING REQUEST CAN BE DELETED )
- User can check status of Request(Enquiry) that is Pending, or Completed
- User can check the offers given by the provider
- User can see/edit their profile
---
### Other Features
- we can change theme of website day(white) and night(black)
- if customer is deleted by admin then their request(Enquiry) will be deleted automatically

## HOW TO RUN THIS PROJECT
- Install Python 3.9 and above (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
pip install django
pip install django-widget-tweaks
pip install -r requirements.txt

```
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

## CHANGES REQUIRED FOR CONTACT US PAGE
- In settings.py file, You have to give your email and password
```
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your email password'
EMAIL_RECEIVING_USER = 'youremail@gmail.com'
```
- Login to gmail through host email id in your browser and open following link and turn it ON
```
https://myaccount.google.com/lesssecureapps
```
## Drawbacks/LoopHoles
- When customer edit their profile then he/she must login again because their username/password is updated in db.

