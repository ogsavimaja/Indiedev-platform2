# Indiedev-platform2

This app is a newer, more advanced version of the older Indiedev-platform. This version will have more advanced features such as ability to add pictures, fancier layout, better sorting of posts, csrf protection and usage of indexing of the database.


## Features
This improved app will share many of the basic functionalities of it's predecessor such as:
* Ability to create an account and use it to log in
* Ability to add, see, edit and delete posts
* Ability to search posts with a keyword or by other means
* The app has user pages which show statistics and project posts added by the user
* User can choose one or more classes for their project post. Possible classes are in the database
* User can send reviews/comments to other users's project posts which are shown in the app

## Why to use Indiedev
The reasons are all the same than with the older version but with added features :)

This app is intended to be used by indie game developers who can share their work in progress games on the platform to get & give feedback about their projects. This way indie game developers can get valuable game testing feedback in the work in progress state. This allows for discovery of potential bugs in the game way sooner when they are still easy to fix and don't ruin the imago of the game by being released all buggy. The game testing feedback also reveals what is good in the game and what parts of the game still need improving/rework.

The other good side of using this app is that it lets developers to comment each others projects, plan ideas and planned price of the game way before full release of their games. This helps the lauch of the game go as smoothly as possible with the best price, development roadmap and quality of the game possible.


## Current status
Currently in the app there are functionalities for the following tasks:
* Creating an account
* Logging in and out
* Creating, editing and deleting announcements
* Creating, editing and deleting comments on announcements
* Adding classes to announcements
* Inspecting announcements and comments added to the database trough the app
* Searching for announcements with a keyword
* Inspecting userpage

The app also has protection against CSRF-attacks, SQL-injection and XSS-attacks. All of the saved passwords stored in the database are salted before hashing for vastly added rainbow table attack resistance and slightly added dictionary/bruteforce attack resistance in case of database breach. On top of that there is also improved errorhandling for most common types of errors that could lead to the app "crashing". Errors regarding forms that user has filled are shown on the same page as the form where favorable.


## How to use
1. Download the repository.<br/>
   Use your desired method or download the .zip file from [Here](https://github.com/ogsavimaja/indiedev-platform/archive/refs/heads/main.zip).

2. Download Flask if you don't have it installed already.<br/>
   You can download Flask by using pip if you have pip added to your PATH by using the command shown below in terminal or download it from [pypi.org](https://pypi.org/project/Flask/).
 
```
pip install flask
```

3. Create database and tables.<br/>
   You can create database and tables in it to the folder containing this project by using commands listed below in your terminal if you are using Linux or on other platforms by creating a database.db file in the repository, opening it with SQLite and using commands `.read schema.sql` and `.read init.sql`.

```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

4. Run the program.<br/>
   You can run the program by running the command shown below in a terminal that has been opened inside the folder containing this application if you have Flask added to your PATH or alternatively by running app.py (launches the application in debug mode).

```
flask run
```

> [!NOTE]
> This "How to use" guide expects you have Python and SQLite downloaded.
> If you don't have [Python](https://www.python.org/downloads/) or [SQLite](https://www.sqlite.org/download.html) downloaded, you can use the links imbedded into this note to navigate to the corresponding download sites.

> [!TIP]
> This application can be run in VS Code (in debug mode) by running app.py in a basic VS Code enviromment
