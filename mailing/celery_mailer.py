from celery import Celery
from celery.utils.log import get_task_logger
from mailingapi.wsgi import *
from .models import Mailing, Client, Message
import backoff
import requests
import json
from mailingapi.settings import JWT_TOKEN
logger = get_task_logger(__name__)
app = Celery('tasks', broker='redis://localhost:6379//', backend='redis://')

@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=10,
    giveup=lambda e: e.response is not None and e.response.status_code < 500
    )
def send_sms(id, phone_number, message_text):
    response = requests.post(url='https://probe.fbrq.cloud/v1/send/' + str(id), 
                        headers={"Authorization": JWT_TOKEN,
                        'Content-Type': 'application/json',
                        'accept': 'application/json'},
                        data=json.dumps({"id": id, 
                        "phone": phone_number, 
                        "text": message_text}))
    return response

@app.task
def send(mailing_id, text, code, tag):
    mailing = Mailing.objects.get(pk=mailing_id)
    filtered_clients = Client.objects.filter(mobile_code = code, tag = tag)
    for client in filtered_clients:
        new_message = Message(mailing_id = mailing.id, client_id = client.id)
        new_message.save()
        response = send_sms(id=new_message.pk, phone_number=new_message.client.phone_number, message_text=new_message.mailing.message_text)
        print("Sent request:")
        print({'url': 'https://probe.fbrq.cloud/v1/send/' + str(new_message.id)})

        print("Outer API responded with status:")
        print(response.status_code)
        new_message.status = int(response.status_code)
        new_message.save()
    return text