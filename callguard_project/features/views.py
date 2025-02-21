import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Call
from .serializers import CallSerializer
from .spam_detection import check_spam  # Import spam detection function

# Twilio setup
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  # Replace with your Account SID
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "your_auth_token")  # Replace with your Auth Token
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+1234567890")  # Replace with your Twilio phone number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def home(request):
    return render(request, "features/home.html")

@csrf_exempt
def twilio_callback(request):
    if request.method == 'POST':
        response = VoiceResponse()
        response.say("Please leave a message after the beep.")
        response.record(transcribe=True, transcribe_callback='/transcription/')
        response.say("Thank you for your message.")

        return HttpResponse(str(response), content_type='application/xml')
    return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def transcription_callback(request):
    if request.method == 'POST':
        transcription_text = request.POST.get('TranscriptionText', '')

        # Check if the transcribed text is spam
        is_spam = check_spam(transcription_text)

        # Send an alert via WebSocket if spam is detected
        if is_spam:
            send_spam_alert(transcription_text)

        # Save the transcription to the database (optional)
        call_data = Call(message=transcription_text, label=is_spam)
        call_data.save()

        return HttpResponse('Transcription processed')
    return HttpResponse('Method not allowed', status=405)

def send_spam_alert(text):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "call_alerts",  # Channel group name
        {
            "type": "call_alert",  # Method to call on consumer
            "message": text,
        }
    )
