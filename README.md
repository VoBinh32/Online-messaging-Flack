# Online Chat App

## Web Programming with Python and JavaScript

[Project Instructions](https://docs.cs50.net/web/2019/x/projects/2/project2.html)

## App Screenshots

![Login Page](https://github.com/VoBinh32/Online-messaging-Flack/blob/master/static/img/Capture.PNG)
![Login Page](https://github.com/VoBinh32/Online-messaging-Flack/blob/master/static/img/Capture1.PNG)
![Login Page](https://github.com/VoBinh32/Online-messaging-Flack/blob/master/static/img/Capture2.PNG)
![Login Page](https://github.com/VoBinh32/Online-messaging-Flack/blob/master/static/img/Capture3.PNG)
![Login Page](https://github.com/VoBinh32/Online-messaging-Flack/blob/master/static/img/Capture4.PNG)
![Login Page](https://github.com/VoBinh32/Online-messaging-Flack/blob/master/static/img/Capture5.PNG)

## Usage

1. Display Name, Channel Creation, and Channel List.
2. Messages View and Sending Messages.
3. Remembering the Channel.
4. Upload File Support
5. Logout

## Setup

```
# Clone repo
$ git clone https://github.com/VoBinh32/Online-messaging-Flack.git


# Install all dependencies
$ pip install -r requirements.txt

# ENV Variables
$ set FLASK_APP=application.py
$ set FLASK_DEBUG = 1

To run the application execute the command:
$ flask run
The flask application should now be running on http://127.0.0.1:5000/
```

## Architecture and Design

1. This application uses [Flask](https://flask.palletsprojects.com/en/1.1.x/), a Python micro-framework that helps with RESTful handling of data, application routing and template binding for rendering the data.
2. It also takes the use of SocketIO which allows 'asynchronous' communication between the server and client.
3. The front-end also makes use of a more basic form of asynchronous request known as an 'AJAX' request. Put simply, this is a standard HTTP request like those made by a browser when requesting a webpage, but made instead by the Javascript running in the client's browser while in use.
