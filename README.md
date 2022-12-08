# Team *<Ibis>* Small Group project

## Team members
The members of the team are:
- William Lingard
- Mathew Tran
- Janet Thomas
- Parneet Johal

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of a single app `lessons` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at *<[https://lecturemonk.pythonanywhere.com/](https://lecturemonk.pythonanywhere.com/)>*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare any other sources here.*
Home Page Image: Kids Cartoon Png #1064763 License: Personal Use - http://clipart-library.com/clip-art/275-2755675_png-etsy-clip-art-and-school-music-kids.htm
