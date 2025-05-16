from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{str(self.room)} - {self.sender}"