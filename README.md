beat_command = celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery_worker_command = celery -A core worker --loglevel=INFO
celery_flower_command = celery -A core flower
db = sqlLite
run command = docker-compose -f docker-compose.yml up --build
