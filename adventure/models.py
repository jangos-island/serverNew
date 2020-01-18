from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def connectRooms(self, destinationRoom, direction):
        directions_dict = {
            "n": "North",
            "w": "West",
            "s": "South",
            "e": "East"
        }

        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        
        destinationRoomID = destinationRoom.id
        try:
            Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            self.description = f"{self.description}\n - to your {directions_dict[direction]}: {destinationRoom.title}"
            destinationRoom.description = f"{destinationRoom.description}\n - to your {directions_dict[reverse_dir]}: {self.title}"
         
            if direction == "n":
                self.n_to = destinationRoomID
<<<<<<< HEAD
                destinationRoom.s_to = self.id
            elif direction == "s":
                self.s_to = destinationRoomID
                destinationRoom.n_to = self.id
            elif direction == "e":
                self.e_to = destinationRoomID
                destinationRoom.w_to = self.id
            elif direction == "w":
                self.w_to = destinationRoomID
                destinationRoom.e_to = self.id
=======
                self.s_to = self.id
            elif direction == "s":
                self.s_to = destinationRoomID
                self.n_to = self.id
            elif direction == "e":
                self.e_to = destinationRoomID
                self.w_to = self.id
            elif direction == "w":
                self.w_to = destinationRoomID
                self.e_to = self.id
>>>>>>> update room model method to connect rooms
            else:
                print("Invalid direction")
                return

            self.save()
            destinationRoom.save()

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





