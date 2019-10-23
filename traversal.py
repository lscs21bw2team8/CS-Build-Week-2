import requests
import random
import time

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def reverse_dir(dir):
    if dir == "n":
        return "s"
    elif dir == "s":
        return "n"
    elif dir == "e":
        return "w"
    elif dir == "w":
        return "e"

token = "Token "

# api-endpoint
init = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
move = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
take = "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/"

# # location given here
# location = "delhi technological university"
# # defining a params dict for the parameters to be sent to the API
# PARAMS = {'address': location}
# # sending get request and saving the response as response object
# r = requests.get(url=URL, params=PARAMS)
# # extracting data in json format
# data = r.json()
# # extracting latitude, longitude and formatted address
# # of the first matching location
# latitude = data['results'][0]['geometry']['location']['lat']
# longitude = data['results'][0]['geometry']['location']['lng']
# formatted_address = data['results'][0]['formatted_address']


# Visit every room
# pickup items if there are any
# store room title, id, and coords

## for iter, see exits of every room
## set to hold all rooms with title and coords
## check each exit if visited
## pick random not visited room, go in save info
## backtrack if no rooms unvisited

visited_rooms = {}
moves = Stack()
r = requests.get(url = init,  headers = {"Authorization":token})
data = r.json()
#print(data)
room = f'room_id: {data["room_id"]}, title: {data["title"]}, coords: {data["coordinates"]}'
#print(room)
while len(visited_rooms) < 500:
    time.sleep(31)
    exits = data["exits"]
    unvisited = []
    x = int(f'{data["coordinates"][1]}{data["coordinates"][2]}')
    y = int(f'{data["coordinates"][4]}{data["coordinates"][5]}')
    print("room: " + room)
    items = data["items"]
    if len(items) > 0:
        for item in items:
            r = requests.post(url=take, headers={"Authorization": token}, json={'name': f'{item}'})
            time.sleep(31)
    for exit in exits:
        if exit == 'n':
            if f'({x},{y+1})' not in visited_rooms.keys():
                unvisited.append('n')
        elif exit == 's':
            if f'({x},{y-1})' not in visited_rooms.keys():
                unvisited.append('s')
        elif exit == 'e':
            if f'({x+1},{y})' not in visited_rooms.keys():
                unvisited.append('e')
        elif exit == 'w':
            if f'({x-1},{y})' not in visited_rooms.keys():
                unvisited.append('w')
    visited_rooms[data["coordinates"]] = room
    if len(unvisited) == 0:
        time.sleep(15)
        dir = moves.pop()
        rev_dir = reverse_dir(dir)
        r = requests.post(url=move, headers={"Authorization": token}, json={'direction': f'{rev_dir}'})
        data = r.json()
        room = f'room_id: {data["room_id"]}, title: {data["title"]}, coords: {data["coordinates"]}'
        print("newroom: " + room )
        continue

    random.shuffle(unvisited)
    dir = unvisited.pop()
    print(dir)
    r = requests.post(url=move, headers={"Authorization": token}, json={'direction': dir})
    print(r)
    print(r.content)
    print(data)

    if len(data["errors"]) > 0:
        print("cooldownaowdna")
        time.sleep(31)
        r = requests.post(url=move, headers={"Authorization": token}, json={'direction': dir})
        data = r.json()
        room = f'room_id: {data["room_id"]}, title: {data["title"]}, coords: {data["coordinates"]}'
        print("newroom: " + room)
        moves.push(dir)
        print(visited_rooms)
    else:
        time.sleep(15)
        data = r.json()
        room = f'room_id: {data["room_id"]}, title: {data["title"]}, coords: {data["coordinates"]}'
        print("newroom: " + room)
        moves.push(dir)
        print(visited_rooms)
print(visited_rooms)
