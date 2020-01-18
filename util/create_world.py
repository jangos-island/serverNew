from django.contrib.auth.models import User
from adventure.models import Player, Room
import random

Room.objects.all().delete()

size_x = 25
size_y = 10
room_count = 100
loop_count = 8

# Initialize the grid
grid = [None] * size_y
width = size_x
height = size_y
for i in range( len(grid) ):
    grid[i] = [None] * size_x

# Initialize the starting room
room_number = 1
initial_x = width // 2
initial_y = 0
initialRoom = Room(title = f"Island #{room_number}", description = f"You are on Island #{room_number}.", x = initial_x, y = initial_y)
initialRoom.save()
grid[initial_y][initial_x] = initialRoom

players=Player.objects.all()
for p in players:
    p.currentRoom=initialRoom.id
    p.save()

# # Start building and connecting more rooms
room_number += 1

# - keep track of connected coordinates (path)
path = set()
path.add((initial_x, initial_y))

# - keep track of possible coordinates to connect to
coords = set()
if (initial_x + 1 < width):
    coords.add((initial_x + 1, initial_y))
if (initial_x - 1 >= 0):
    coords.add((initial_x - 1, initial_y))
if (initial_y + 1 < height):
    coords.add((initial_x, initial_y + 1))
if (initial_y - 1 >= 0):
    coords.add((initial_x, initial_y - 1))

directions = ["n", "s", "w", "e"]

while len(coords) and room_number <= room_count:
    # - create a random room from the set
    coord = coords.pop()
    room = Room(title = f"Island #{room_number}", description = f"You are on Island #{room_number}", x = coord[0], y = coord[1])
    room.save()


    # - randomly connect the new room to existing path
    directions = ["n", "s", "w", "e"]
    random.shuffle(directions)

    coord = (room.x, room.y)
    connected = False

    i = 0
    while not connected and i < 4:
        direction = directions[i]

        if direction == "n" and room.n_to == 0 and coord[1] + 1 < height and grid[coord[1] + 1][coord[0]]:
            room.connectRooms(grid[coord[1] + 1][coord[0]], "n")
            connected = True
        elif direction == "s" and room.s_to == 0 and coord[1] - 1 >= 0 and grid[coord[1] - 1][coord[0]]:
            room.connectRooms(grid[coord[1] - 1][coord[0]], "s")
            connected = True
        elif direction == "e" and room.e_to == 0 and coord[0] + 1 < width and grid[coord[1]][coord[0] + 1]:
            room.connectRooms(grid[coord[1]][coord[0] + 1], "e")
            connected = True
        elif direction == "w" and room.w_to == 0 and coord[0] - 1 >= 0 and grid[coord[1]][coord[0] - 1]:
            room.connectRooms(grid[coord[1]][coord[0] - 1], "w")
            connected = True
        i += 1
    
    grid[coord[1]][coord[0]] = room
    path.add(coord)

    # update possible coordinates to connect to
    if coord[1] + 1 < height and grid[coord[1] + 1][coord[0]] is None:
        coords.add((coord[0], coord[1] + 1))
    if coord[1] - 1 >= 0 and grid[coord[1] - 1][coord[0]] is None:
        coords.add((coord[0], coord[1] - 1))
    if coord[0] + 1 < width and grid[coord[1]][coord[0] + 1] is None:
        coords.add((coord[0] + 1, coord[1]))
    if coord[0] - 1 >= 0 and grid[coord[1]][coord[0] - 1] is None:
        coords.add((coord[0] - 1, coord[1]))

    room_number += 1

if loop_count > 0 and loop_count < width:
    loop = 0
    while len(path) and loop < loop_count:
        coord = path.pop()
        room = grid[coord[1]][coord[0]]

        directions = ["n", "s", "w", "e"]
        random.shuffle(directions)

        i = 0
        has_new_loop = False
        while not has_new_loop and i < 4:
            direction = directions[i]

            if direction == "n" and room.n_to == 0 and coord[1] + 1 < height and grid[coord[1] + 1][coord[0]]:
                room.connectRooms(grid[coord[1] + 1][coord[0]], "n")
                has_new_loop = True
            elif direction == "s" and room.s_to == 0 and coord[1] - 1 >= 0 and grid[coord[1] - 1][coord[0]]:
                room.connectRooms(grid[coord[1] - 1][coord[0]], "s")
                has_new_loop = True
            elif direction == "e" and room.e_to == 0 and coord[0] + 1 < width and grid[coord[1]][coord[0] + 1]:
                room.connectRooms(grid[coord[1]][coord[0] + 1], "e")
                has_new_loop = True
            elif direction == "w" and room.w_to == 0 and coord[0] - 1 >= 0 and grid[coord[1]][coord[0] - 1]:
                room.connectRooms(grid[coord[1]][coord[0] - 1], "w")
                has_new_loop = True

            i += 1
        
        if has_new_loop:
            loop += 1 


# Add top border
str = "# " * ((3 + width * 5) // 2) + "\n"

# The console prints top to bottom but our array is arranged
# bottom to top.
#
# We reverse it so it draws in the right direction.
reverse_grid = list(grid) # make a copy of the list
reverse_grid.reverse()
for row in reverse_grid:
    # PRINT NORTH CONNECTION ROW
    str += "."
    for room in row:
        if room is not None and room.n_to != 0:
            str += "  |  "
        else:
            str += "     "
    str += ".\n"
    # PRINT ROOM ROW
    str += "."
    for room in row:
        if room is not None and room.w_to != 0:
            str += "-"
        else:
            str += " "
        if room is not None:
            str += f"{0}".zfill(3)
        else:
            str += "   "
        if room is not None and room.e_to != 0:
            str += "-"
        else:
            str += " "
    str += ".\n"
    # PRINT SOUTH CONNECTION ROW
    str += "."
    for room in row:
        if room is not None and room.s_to != 0:
            str += "  |  "
        else:
            str += "     "
    str += ".\n"

    # Add bottom border
    str += ". " * ((3 + width * 5) // 2) + "\n"

# Print string
print(str)
