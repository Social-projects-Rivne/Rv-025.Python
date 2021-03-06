# Rv-025.Python

### Version
0.0.1

### Installation

1) For installing required libs and frameworks execute next commands:
```
pip install -r requirements.txt
```

2) Copy and rename file `backend/restaurant/local_settings.py.example` to `backend/restaurant/local_settings.py`.

3) Copy and rename file `config.ini.example` to `config.ini`. Write in `config.ini` your credentials.

4) Then you have to let Django make its migrations
```
python backend/manage.py makemigrations
python backend/manage.py migrate
```

5) Load fixtures data:
```
python backend/manage.py loaddata backend/fixtures/**
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
