# MUGGLE NOTES

#### Video Demo: https://youtu.be/K-KDs54WGck

## Description:
This is **CS50: Introduction to computer science** final project in which we made a flask-based web application in cs50.ide environment. In this project, one can write/upload and store daily notes/file(s) systematically.


Technologies used:

- flask
- python
- javascript
- sqlite3
- HTML
- css
- bootstrap
- other small libraries or packages

### Files:

1. statics contains stylesheets, javascript(.js files), favicon icon, uploads (created to store all the uploaded files in the database ), fonts( for including glyphicons from bootstrap 3)
2. templates include all the necessary Html files used.
3. application.py
4. helpers.py
5. notes.db

### Routing

Each route checks if the user is authenticated. It means if correct mail and password were supplied and what role it has. So for example a teacher cannot enter /students/homeworks/1 route. The same is for student, he cannot enter teacher dashboard route.

### Sessions

The webpage uses sessions to confirm that user is registered.

### Database

Database stores users and uploads. The table users contains session id, unique username, unique user's email-id, hash password and the table uploads contains all the session id, uploaded files, and date.

### javascript localStorage

localStorage enable web browsers to store key-value pairs. It continues to store data after the browser is closed .i.e, locaStorage does not expires. We used it to store all the created notes with user specific keys- notes, titles, title of important note, date and times.

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- The reset passward link passed through emails only supports chrome which can be improved for other browsers.
- Notes stored in localStorage are only browser specific which can also be improved.


### Features:
1. Sign up & Sign in: Sign up allows users to first register in **MUGGLE NOTES** by providing a unique username and email-id. Whereas, if they already have a registered account they can directly log in by entering **username** and **password** as their login credentials.
2. Forget/reset password: This feature allows users to reset their login password by asking them to enter the registered email-id and send an auto-generated email (with the user's name mentioned on it). This mail contains a link that will redirect users to a page where they can create a new password that must contain at least 4 to 12 characters.
3. Delete account: It allows user to delete their account by providing the login credentials.
4. Created a homepage where users can see all the insights of this application in the carousel.
5. Note icon: This icon will redirect the user to a new page where they can add new titled notes with the date and time mentioned on it. It also allows users to delete the notes, mark them as important by changing the note color to red, and also a search bar to locate the notes by typing any keyword or characters from its content.
6. Upload icon: This icon will redirect the users to a new page where they can upload any files with extensions pdf, jpg, jpeg, gif, png. It also allows users to access all these uploaded files in the form of a table that stores the filename (with a clickable link to open these files.) and the upload date.
7. Each page of this web application contains a share button that allows users to share the current page via social platforms, Facebook, Twitter, LinkedIn, Whatsapp.

## How to launch application

1. Login to the environment `https://ide.cs50.io/`
2. Clone the code: `https://github.com/divyapathak99/cs50-final-project-fall-2021`
3. Once installed run command `!pip install flask`
4. Make a .env file which store the value of the field MAIL DEFAULT SENDER, MAIL PASSWORD, MAIL USERNAME to use MAIL(app).
5. On console run command `flask run`
6. You are ready to go!


#### About me:
My name is Divya Pathak, and I'm from India. I have recently completed my master's in physics.

