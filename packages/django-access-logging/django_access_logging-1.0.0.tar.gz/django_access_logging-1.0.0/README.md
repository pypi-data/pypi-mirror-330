# django-access-logging
Django middleware to log all requests and responses to a database.

<a id="installation"></a>
## Installation
Using `pip`
```commandline
pip install django-access-logging
```

In your project's `settings.py` file, add `django_access_logging`to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    "django_access_logging",
]
```
Then, create the database tables by running ```migrate```:
```commandline
python manage.py migrate
```

## Usage
### Viewing logged data
After installing and restarting the server, logged data can be viewed within `Access log entries` 
section of Django admin interface. See screenshots below:

[<img src="https://github.com/ross-sharma/django-access-logging/blob/master/img/admin.jpg" width="200"/>](https://github.com/ross-sharma/django-access-logging/blob/master/img/admin.jpg)
[<img src="https://github.com/ross-sharma/django-access-logging/blob/master/img/detail.jpg" width="200"/>](https://github.com/ross-sharma/django-access-logging/blob/master/img/detail.jpg)

### Ignoring specific IP prefixes
To ignore logging for specific IP addresses, add them to the `Ignored Ip Prefixes` model in the Django admin interface.
For example, adding `192.`, will ignore all IP addresses starting with `192.`.
