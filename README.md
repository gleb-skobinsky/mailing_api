API на Django REST Framework для рассылки SMS-сообщений

Для запуска сервера на Ubuntu 20.04.4 LTS выполните команды:
```
sudo apt install redis-server # если Redis еще не установлен
sudo service redis-server start
git clone https://github.com/gleb-skobinsky/mailing_api.git
cd mailing_api
virtualenv fabr_venv
source fabr_venv/bin/activate
pip install -r requirements.txt
celery -A mailing.celery_mailer worker --loglevel=INFO -P gevent --detach --logfile=celery.log
python manage.py runserver
```
