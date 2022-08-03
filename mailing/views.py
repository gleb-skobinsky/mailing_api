from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .celery_mailer import app, send
from django.utils.timezone import now
from django.db.models import Count
from .sender_util import check_current_time

class MailingApiView(APIView):
    def get(self, request):
        mailings_list = Mailing.objects.all().values()
        return Response({'mailings': MailingSerializer(mailings_list, many=True).data})

    def post(self, request):
        if "stats" in request.data:
            if request.data["stats"] == "all":
                message_groups = Message.objects.values('status').annotate(count=Count('id')).order_by()
                stats = [entry for entry in message_groups]
                return Response(stats)
            elif isinstance(request.data["stats"], int) or (isinstance(request.data["stats"], str) and request.data["stats"].isdigit()):
                searched_id = int(request.data["stats"])
                message_groups = Message.objects.filter(mailing_id=searched_id).values('status').annotate(count=Count('id')).order_by()
                stats = [entry for entry in message_groups]
                if len(stats) > 0:
                    return Response(stats)
                else:
                    return Response({"Error: no mailings found for the given id"})
            else:
                return Response({"Error: invalid request for mailing statistics"})
        serializer = MailingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mailing_to_send = serializer.save()
        starter = check_current_time(mailing_to_send.time_start, mailing_to_send.time_end)
        send.apply_async(kwargs={"mailing_id": mailing_to_send.pk,
                                "text": mailing_to_send.message_text, 
                                "code": mailing_to_send.mobile_code, 
                                "tag": mailing_to_send.tag}, 
                        eta=starter,
                        expires=mailing_to_send.time_end)
        return Response({'mailing': serializer.data})

    def put(self, request, *args, **kwargs):
        try:
            id = request.data.pop("id")
        except KeyError:
            return Response({"Error: method PUT not allowed"})
        try:
            instance = Mailing.objects.get(pk=id)
        except Mailing.DoesNotExist:
            return Response({"Error: object does not exist"})
        
        serializer = MailingSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"mailing": serializer.data})

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        if not id:
            return Response({"Error: Method DELETE not allowed"})
        try:
            delete_mailing = Mailing.objects.get(pk=id)
        except Mailing.DoesNotExist:
            return Response({"Error: object does not exist"})

        delete_mailing.delete()
        return Response({"mailing": f"Deleted mailing {id}"})

class ClientApiView(APIView):
    def get(self, request):
        clients_list = Client.objects.all().values()
        return Response({'clients': ClientSerializer(clients_list, many=True).data})

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'client': serializer.data})

    def put(self, request, *args, **kwargs):
        try:
            initial_number = request.data.pop("initial_number")
        except KeyError:
            return Response({"Error: method PUT not allowed"})
        try:
            instance = Client.objects.get(phone_number=initial_number)
        except Client.DoesNotExist:
            return Response({"Error: object does not exist"})
        
        serializer = ClientSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"client": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"Error: Method DELETE not allowed"})
        try:
            delete_client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"Error: object does not exist"})

        delete_client.delete()
        return Response({"client": f"Deleted client {pk}"})



        