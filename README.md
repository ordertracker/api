# OrderTracker

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[<img src="https://img.shields.io/badge/slack-@ordertracker-yellow.svg?logo=slack">](https://ordertracker.slack.com)
![CI workflow](https://github.com/ordertracker/api/workflows/CI%20workflow/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/ordertracker/api/branch/master/graph/badge.svg)](https://codecov.io/gh/ordertracker/api)

### What is OrderTracker
Flask application for collecting and managing Magento orders, this app can help you to manage your orders directly in your store without updating inventory on the products. This is just the first part of the application which provides ability for managing the orders from the Ecommerce's API, getting them and making the available and prepared to the frontend application. There is also a user management model that offers authentication to the application and protect the application from unauthorized access.

The application produces RESTful Web Services available for the frontend application.

### Starting the applicatiom

Exporting ENV variables
```
$ export FLASK_APP=wsgi.py
$ source .env
$ export $(cut -d= -f1 .env)
```

Activating the Python virtualenv and starting the application
```
$ . venv/bin/activate
$ flask run
```

## Copying and License

The content is open and licensed under the GNU General Public License v3.0 whose full text may be found at:

https://www.gnu.org/licenses/gpl-3.0.en.html
