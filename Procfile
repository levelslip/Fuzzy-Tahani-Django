# Procfile untuk deployment ke Railway/Render/Heroku

# Web process - menjalankan Gunicorn server
web: gunicorn tahani.wsgi:application --bind 0.0.0.0:$PORT

# Release process - migrasi database saat deploy
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
