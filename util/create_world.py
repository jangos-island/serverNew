from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
               description="You're on Outside Cave Entrance.")

r_foyer = Room(title="Foyer", description="You're on Foyer.")

r_overlook = Room(title="Grand Overlook", description="You're on Grand Overlook.")

r_narrow = Room(title="Narrow Passage", description="You're on Narrow Passage")

r_treasure = Room(title="Treasure Chamber", description="You're on Treasure Chambe.r")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")

r_foyer.connectRooms(r_overlook, "n")

r_foyer.connectRooms(r_narrow, "e")

r_narrow.connectRooms(r_treasure, "n")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()
