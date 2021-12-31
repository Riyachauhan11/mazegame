import turtle
import math
import random

import easygui

window = turtle.Screen()
window.bgcolor('black')
window.title("A Maze Game")
window.setup(700, 700)
window.tracer(0)

# register shapes
turtle.register_shape("wizard_right.gif")
turtle.register_shape("wizard_left.gif")
turtle.register_shape("treasure.gif")
turtle.register_shape("wall.gif")
turtle.register_shape("enemy.gif")
turtle.register_shape("splash.gif")

# class is a collection of info and using init helps us put the attributes/varaiables
# (mentioned in arguements ; self is a conventional first arguement) in required places


class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wizard_right.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        # calculating the spot to move to
        move_to_x = player.xcor()
        move_to_y = player.ycor()+24

        # check if spot has X or a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        # calculating the spot to move to
        move_to_x = player.xcor()
        move_to_y = player.ycor()-24

        # check if spot has X or a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        # calculating the spot to move to
        move_to_x = player.xcor()-24
        move_to_y = player.ycor()

        self.shape("wizard_left.gif")

        # check if spot has X or a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        # calculating the spot to move to
        move_to_x = player.xcor()+24
        move_to_y = player.ycor()

        self.shape("wizard_right.gif")

        # check if spot has X or a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collison(self, other):
        # self : player , other : treasure
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        # formula for finding distance between 2 points is used below
        distance = math.sqrt((a**2)+(b**2))

        # if dist<5 than player and threasure r prob colliding or overlapping with each other
        if distance < 5:
            return True
        else:
            return False


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()
# since we cant completely delete any element from our maze using turtle module , we'll put it to a point not
# present in maze


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        # check if player is close if so go in its direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        # calculate the spot to move to, self.xcor / ycor r the current coordinates took from the level1
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            # choose a different direction
            self.direction = random.choice(["up", "down", "left", "right"])

        # set timer to move enemy next time(keep it moving continuously)
        # to make enemy move randomly we use random module and make it move after 100 ms or more and 300 ms or less
        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 75:
            return True
        else:
            return False


def start_game():
    global game_state
    game_state = "game"


levels = []

level_1 = ["XXXXXXXXXXXXXXXXXXXXXXXXX",
           "XP  XXXXXXX         XXXXX",
           "X  XXXXXXX  XXXXXX  XXXXX",
           "X       XX  XXXXXX  XXXXX",
           "X       XX  XXX       EXX",
           "XXXXXX  XX  XXX        XX",
           "XXXXXX  XX  XXXXXX  XXXXX",
           "XXXXXX  XX    XXXX  XXXXX",
           "X  XXX        XXXXT XXXXX",
           "X  XXX  XXXXXXXXXXXXXXXXX",
           "X         XXXXXXXXXXXXXXX",
           "X                XXXXXXXX",
           "XXXXXXXXXXXX     XXXXX  X",
           "XXXXXXXXXXXXXXX  XXXXX  X",
           "XXX  XXXXXXXXXX         X",
           "XXXE                    X",
           "XXX         XXXXXXXXXXXXX",
           "XXXXXXXXXX  XXXXXXXXXXXXX",
           "XXXXXXXXXX              X",
           "XX   XXXXX              X",
           "XX   XXXXXXXXXXXXX  XXXXX",
           "XX    YXXXXXXXXXXX  XXXXX",
           "XXT         XXXX        X",
           "XXXXE                   X",
           "XXXXXXXXXXXXXXXXXXXXXXXXX"
           ]

# adding a treasure list
treasures = []

# adding a enemies list
enemies = []

# add level 1 to levels list
levels.append(level_1)


# creating level setup func
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            # mentioning the coordinates of each character in level 1 (whose first / top left block is at (0,0))
            character = level[y][x]
            # finding the coordinates that will be used as per the main screen/window dimensions
            # top left block : (-288,288) ; each block is 24 wide
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)

            # check if character/wall is an X which is representing wall in code
            if character == 'X':
                pen.goto(screen_x, screen_y)
                pen.shape("wall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))
            # check if character is represting player
            if character == 'P':
                player.goto(screen_x, screen_y)
            # check if character is reprensting treasure , the Treasure written below is class and in class we r putting x and y
            if character == 'T':
                treasures.append(Treasure(screen_x, screen_y))
            if character == 'E':
                enemies.append(Enemy(screen_x, screen_y))


pen = Pen()
player = Player()


# create walls coordinate list
walls = []

# setting up the level
setup_maze(levels[0])


# Keyboard Binding ; The "Left" represents left arrow key so the go_left is used with it and so on....
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")


# turn off screen updates/animation so that they can take place in the final loop
window.tracer(0)
# start moving enemies, telling enemy to move after 250 milisecond
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

while True:
    # check for player collision with threasure

    for treasure in treasures:
        if player.is_collison(treasure):
            p = treasure
            # add the treasure gold to player gold
            player.gold += treasure.gold
            print("Player Gold : {}".format(player.gold))
            # destroy/hide the turtle
            treasure.destroy()
            # remove the treasure from treasure list
            treasures.remove(treasure)

    # iterate through enemies list to see if the player has collided with any enemies
    for enemy in enemies:
        if player.is_collison(enemy):
            player.goto(-264, 264)
            yn = easygui.ynbox('You Lost')

    # update screen
    window.update()
