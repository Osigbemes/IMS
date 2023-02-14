import requests
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import jwt
from django.core.mail import EmailMessage, send_mail

class Util:
    @staticmethod
    def sendMail(emailBody):
        
        send_mail(emailBody['subject'], emailBody['email_body'], emailBody['email_from'], emailBody['to_email'])


class UtilEmail:
    @staticmethod

    def sendEmail(data):
        
        user=data['user']
        request=data['request']
        token = data['token']
        appointmentId = data['appointmentId']

        currentSite = get_current_site(request).domain
        ims_site = f'https://intelligent-monitoring-system.netlify.app/confirm/{appointmentId}'
        reverseSite = reverse('ims:accept_or_reject', args=[appointmentId])

        urlPath = ims_site  #'?token=' + str(token)
        emailBody = 'Hi '+ str(user.username) + ', ' + 'use the link below to confirm your appointment \n'+ urlPath

        subject = 'Confirm Appointment!'
        message = emailBody
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]


        data = {'email_body':message, 'email_from':email_from, 'to_email':recipient_list, 'subject':subject}
        #send email
        Util.sendMail(data) 

def GetPatientInfo():
    response = requests.get('https://youngancient.000webhostapp.com/fetch-data-gbemi.php')
    return response.json()


# print (type(response.json()))
# print ((response.json()))