# Rv-025.Python

### Version
0.0.1

### Installation

For installing required libs and frameworks execute next commands:
```
  pip install -r requirements.txt
```

Copy and rename file `restaurant/local_settings.example` to `restaurant/local_settings.py`.

Next step you need to create *config.ini* file in the root of project.
*config.ini* should contain next lines with yours setting:
```
  [RDB]
  ENGINE = django.db.backends.postgresql
  NAME = db_name
  USER = db_user
  PASSWORD = db_password
  HOST = 127.0.0.1
  PORT = 5432
```

Then you have to let Django make its migrations
```
    python manage.py makemigrations
    python manage.py migrate
```

To load fixtures data:
```
  python manage.py loaddata fixtures/roles.json
```

### Project role responsibilities

| Role | Responsibility |
| ------ | ------ |
| Techlead | Code review, communication with tech expert |
| Requirement Manager | Writing Requirement specification, communication with Product Owner |
| SCRUM Master | Default responsibilities fo SCRUM Master role |
| QC | Writing Unit tests, communication with PO, Tech Expert |
| DevOps | Deploying application on to cloud service, continuous integration |
| Knowledge Lead | Sharing knowledge |

License
----

MIT
