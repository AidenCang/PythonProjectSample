from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
from rest_framework.utils import json


def index(request):
    return render(request, 'channelsApp/index.html', {})


def room(request, room_name):
    return render(request, 'channelsApp/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
