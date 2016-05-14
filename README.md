Web Development API Task
=
This demo RESTful API application is implemented in Python (2.7+) with no third-party libraries or frameworks used. I'm not a Python developer, but I find it to be a simple and really powerful general purpose language, so I decided to try if I can do this task in Python and learn a little bit more about it.

The application works with any WSGI-compatible web server. For the purpose of the demo, the *wsgiref.simple_server* Python module is used.
The persistence layer for the User model is implemented using the Repository Pattern which separates the business logic from the interactions with the underlying data source. This allows the concrete data storage mechanism to be easily changed. For this demo SQLite3 database is used.

The sample application can be started by running the following command in the project's root path:
> python main.py

Tests can be executed by running the following command in the project's root path:
> python -m unittest discover
