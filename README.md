django Orders_API web app
    front   -> "django admin" based
    db      -> sqlite

before starting the app need to launch env:
    1. celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    2. celery_worker_command = celery -A core worker --loglevel=INFO
    3. (OPTIONAL) celery_flower_command = celery -A core flower

run app command:
    docker-compose -f docker-compose.yml up --build
