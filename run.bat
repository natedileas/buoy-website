start cmd /k celery -A app:celery worker -l info

start cmd /k redis-server

start cmd /k "cd flask_react && npm start"

env\Scripts\python.exe app.py
