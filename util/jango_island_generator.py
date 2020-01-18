import random

class Room:
  def __init__(self, id, name, description, x, y):
    self.id = id
    self.name = name
    self.description = description
    self.n_to = None
    self.s_to = None
    self.e_to = None
    self.w_to = None
    self.x = x
    self.y = y

  def __repr__(self):
    if self.e_to is not None:
      return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
    return f"({self.x}, {self.y})"

  def connect_rooms(self, connecting_room, direction):
    '''
    Connect two rooms in the given n/s/e/w direction
    '''
<<<<<<< HEAD
    directions_dict = {
      "n": "North",
      "w": "West",
      "s": "South",
      "e": "East"
    }
    
=======
>>>>>>> add jango island generator
    reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
    reverse_dir = reverse_dirs[direction]
    
    setattr(self, f"{direction}_to", connecting_room)
<<<<<<< HEAD
    self.description = f"{self.description}\n- to your {directions_dict[direction]}: {connecting_room.name}"

    setattr(connecting_room, f"{reverse_dir}_to", self)
    connecting_room.description = f"{connecting_room.description}\n- to your {directions_dict[reverse_dir]}: {self.name}"

=======
    self.description = f"{self.description}\nTo your {direction}: {connecting_room.name}"

    setattr(connecting_room, f"{reverse_dir}_to", self)
    connecting_room.description = f"{connecting_room.description}\nTo your {reverse_dir}: {self.name}"

    print(self.name)
>>>>>>> add jango island generator
    print(self.description)

class World:
  def __init__(self):
    self.grid = None
    self.width = 0
    self.height = 0

  def connect_room_to_path(self, room):
    directions = ["n", "s", "w", "e"]
    random.shuffle(directions)

    coord = (room.x, room.y)
    connected = False

    i = 0
    while not connected and i < 4:
      direction = directions[i]
      
      if direction == "n" and room.n_to is None and coord[1] + 1 < self.height and self.grid[coord[1] + 1][coord[0]]:
        room.connect_rooms(self.grid[coord[1] + 1][coord[0]], "n")
        connected = True
      elif direction == "s" and room.s_to is None and coord[1] - 1 >= 0 and self.grid[coord[1] - 1][coord[0]]:
        room.connect_rooms(self.grid[coord[1] - 1][coord[0]], "s")
        connected = True
      elif direction == "e" and room.e_to is None and coord[0] + 1 < self.width and self.grid[coord[1]][coord[0] + 1]:
        room.connect_rooms(self.grid[coord[1]][coord[0] + 1], "e")
        connected = True
      elif direction == "w" and room.w_to is None and coord[0] - 1 >= 0 and self.grid[coord[1]][coord[0] - 1]:
        room.connect_rooms(self.grid[coord[1]][coord[0] - 1], "w")
        connected = True

      i += 1

    return connected

  
  def generate_rooms(self, size_x, size_y, room_count, loop_count=1):
    '''
    Fill up the grid, bottom to top, in a zig-zag pattern
    '''

    # Initialize the grid
    self.grid = [None] * size_y
    self.width = size_x
    self.height = size_y
    for i in range( len(self.grid) ):
      self.grid[i] = [None] * size_x

    # Initialize the starting room
    room_number = 1
    initial_x = self.width // 2
    initial_y = 0
<<<<<<< HEAD
    initialRoom = Room(room_number, f"Island #{room_number}", f"You are on Island #{room_number}.", initial_x, initial_y)
=======
    initialRoom = Room(room_number, f"Room #{room_number}", "Automatically gerated room", initial_x, initial_y)
>>>>>>> add jango island generator
    self.grid[initial_y][initial_x] = initialRoom
    
    # Start building and connecting more rooms
    room_number += 1

    # - keep track of connected coordinates (path)
    path = set()
    path.add((initial_x, initial_y))

    # - keep track of possible coordinates to connect to
    coords = set()
    if (initial_x + 1 < self.width):
      coords.add((initial_x + 1, initial_y))
    if (initial_x - 1 >= 0):
      coords.add((initial_x - 1, initial_y))
    if (initial_y + 1 < self.height):
      coords.add((initial_x, initial_y + 1))
    if (initial_y - 1 >= 0):
      coords.add((initial_x, initial_y - 1))

    directions = ["n", "s", "w", "e"]
    while len(coords) and room_number <= room_count:
      # - create a random room from the set
      coord = coords.pop()
<<<<<<< HEAD
      new_room = Room(room_number, f"Island #{room_number}", f"You are on Island #{room_number}", coord[0], coord[1])
=======
      new_room = Room(room_number, f"Room #{room_number}", "Automatically gerated room", coord[0], coord[1])
>>>>>>> add jango island generator

      # - randomly connect the new room to existing path
      self.connect_room_to_path(new_room)
      self.grid[coord[1]][coord[0]] = new_room
      path.add(coord)

      # update possible coordinates to connect to
      if coord[1] + 1 < self.height and self.grid[coord[1] + 1][coord[0]] is None:
        coords.add((coord[0], coord[1] + 1))
      if coord[1] - 1 >= 0 and self.grid[coord[1] - 1][coord[0]] is None:
        coords.add((coord[0], coord[1] - 1))
      if coord[0] + 1 < self.width and self.grid[coord[1]][coord[0] + 1] is None:
        coords.add((coord[0] + 1, coord[1]))
      if coord[0] - 1 >= 0 and self.grid[coord[1]][coord[0] - 1] is None:
        coords.add((coord[0] - 1, coord[1]))

      room_number += 1

    if loop_count > 0 and loop_count < self.width:
      loop = 0
      while loop < loop_count:
        coord = path.pop()
        new_room = self.grid[coord[1]][coord[0]]

        has_new_loop = self.connect_room_to_path(new_room)
        if has_new_loop:
          loop += 1 


  def print_rooms(self):
    '''
    Print the rooms in room_grid in ascii characters.
    '''

    # Add top border
    str = "# " * ((3 + self.width * 5) // 2) + "\n"

    # The console prints top to bottom but our array is arranged
    # bottom to top.
    #
    # We reverse it so it draws in the right direction.
    reverse_grid = list(self.grid) # make a copy of the list
    reverse_grid.reverse()
    for row in reverse_grid:
      # PRINT NORTH CONNECTION ROW
      str += "."
      for room in row:
        if room is not None and room.n_to is not None:
          str += "  |  "
        else:
          str += "     "
      str += ".\n"
      # PRINT ROOM ROW
      str += "."
      for room in row:
        if room is not None and room.w_to is not None:
          str += "-"
        else:
          str += " "
        if room is not None:
          str += f"{room.id}".zfill(3)
        else:
          str += "   "
        if room is not None and room.e_to is not None:
          str += "-"
        else:
          str += " "
      str += ".\n"
      # PRINT SOUTH CONNECTION ROW
      str += "."
      for room in row:
        if room is not None and room.s_to is not None:
          str += "  |  "
        else:
          str += "     "
      str += ".\n"

      # Add bottom border
      str += ". " * ((3 + self.width * 5) // 2) + "\n"

    # Print string
    print(str)

w = World()
<<<<<<< HEAD
w.generate_rooms(10, 10, 80, 10)
=======
w.generate_rooms(10, 10, 20, 2)
>>>>>>> add jango island generator

w.print_rooms()