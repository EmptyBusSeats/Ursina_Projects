from sys import set_coroutine_origin_tracking_depth
from typing import Sequence
from ursina import *

app = Ursina()
score = 0
lives = 3

#Build walls in the game.
ceiling = Entity(model = 'quad', color = color.black, scale = (14.1,0.1), position = (0,4,0), collider = 'box')
floor = Entity(model = 'quad', color = color.black, scale = (14.1,0.1), position = (0,-4,0), collider = 'box')
l_wall = Entity(model = 'quad', color = color.black, scale = (0.1,8), position = (-7,0,0), collider = 'box')
r_wall = Entity(model = 'quad', color = color.black, scale = (0.1,8), position = (7,0,0), collider = 'box')

#Create a ball
ball = Entity(model = 'circle', color = color.white, scale = (0.2, 0.2), position = (0,-1.5,0), rotation_z = 90, collider = 'box', speed = 7.5)

#Create a paddle
paddle = Entity(model = 'quad', color = color.orange, scale = (2,0.4), position = (0,-3.5,0), collider = 'box')

#Build some bricks to destroy
bricks = []
for x_pos in range(-65,75,10):
    for y_pos in range(3,8):
        brick = Entity(model = 'quad', x = x_pos/10, y = y_pos/3, color = color.red, scale = (0.8,0.3), collider = 'box')
        bricks.append(brick)


#Have an update function that handles all movement and collisions

def update():
    global score
    global lives
    ball.position += ball.right * ball.speed * time.dt
    paddle.x += (held_keys['right arrow'] - held_keys['left arrow']) * time.dt * 3.5

    hit_info = ball.intersects()
    if hit_info.hit:
        if hit_info.entity == paddle:
            delta = hit_info.entity.x - ball.x
            ball.rotation_z = 270 - delta * 55
            ball.speed += ball.speed * 0.05
        elif hit_info.entity == r_wall or hit_info.entity == l_wall:
            ball.rotation_z = 180 - ball.rotation_z
        elif hit_info.entity == ceiling:
            ball.rotation_z = -ball.rotation_z
        elif hit_info.entity in bricks:
            ball.rotation_z = -ball.rotation_z
            bricks.remove(hit_info.entity)
            destroy(hit_info.entity)
            score += 1

        if len(bricks) == 0:
            end_game("You Win!")

    if ball.y < paddle.y:
        end_game("You Lose, sucker! \n\nYour Score: " + str(score))

def end_game(user_message):
    message = Text(text = user_message, scale = 2, origin = (0,0), background = True, color = color.green)
    application.pause()

EditorCamera()
app.run()

