start cmd /k "..\senv\Scripts\celery -A app:celery worker -l info"

start cmd /k redis-server

start cmd /k "cd flask_react && npm start"

..\senv\Scripts\python.exe app.py
