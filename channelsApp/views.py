from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
from rest_framework.utils import json

from channelsApp.models import Room


def chatindex(request):
    return render(request, 'channelsApp/index.html', {})


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })


def room(request, room_name):
    return render(request, 'channelsApp/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
