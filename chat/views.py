from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Message

def HomeView(request):
    if request.method == "POST":
        username = request.POST["username"]
        room = request.POST["room"]

        # Save username in session
        request.session["username"] = username

        existing_room = Room.objects.filter(room_name__iexact=room).first()
        if not existing_room:
            Room.objects.create(room_name=room)

        return redirect("room", room_name=room)

    return render(request, "chat/home.html")


def RoomView(request, room_name):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    existing_room = Room.objects.filter(room_name__iexact=room_name).first()
    if not existing_room:
        messages.error(request, "Room does not exist.")
        return redirect("login")

    get_messages = Message.objects.filter(room=existing_room)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": existing_room.room_name,
    }
    return render(request, "chat/room.html", context)


def SignOutView(request):
    if request.method == "POST":
        request.session.flush()
        messages.success(request, "You have successfully logged out.")
    return redirect("login")
