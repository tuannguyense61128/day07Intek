import pyglet
import time
import vector
from random import randint



### Initialize Window
WIDTH = 1000
HEIGHT = 800
game_window = pyglet.window.Window(WIDTH, HEIGHT)

### Initialize varibles of ball
G = -800  # gravity
v_init = [0, 0]  # Initialize velocity ball
Vy = 0 # velocity y overtime
Vx = 0 # velocity x overtime
v_basket = [0, 0]
has_scored = False
has_colli = False
# motion timer
t = 0

# MOUSE
can_play = True
# Initialize position
START_POS = [WIDTH/2, 0]  # Start_position
score_point = [0,0]
# game time :
time_countback = 15
game_over = False
### Set center    print(colli_point)
center_x = WIDTH/2
center_y = HEIGHT/2

### Create OrderedGroup
back = pyglet.graphics.OrderedGroup(0)
mid = pyglet.graphics.OrderedGroup(1)
front = pyglet.graphics.OrderedGroup(2)


################# Create Batch
batch = pyglet.graphics.Batch()
ball_image = pyglet.image.load('resources/ball.png')
basket_image = pyglet.image.load('resources/basket.png')
board_image = pyglet.image.load('resources/board2.png')
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
ls = [ball_image,basket_image,board_image]
for image in ls:
    center_image(image)
###################



# Create ball sprite
ball = pyglet.sprite.Sprite(ball_image, batch = batch, x = center_x , y = 0, group = front)



# Create Basket
basket = [pyglet.sprite.Sprite(board_image, batch=batch, x = center_x, y = center_y, group = back ),
          pyglet.sprite.Sprite(basket_image, batch=batch, x = center_x , y = center_y-110, group = mid)]
global basket_patrol
can_patrol = False

#Create Label
time_label = pyglet.text.Label('Time :',
                          font_name='Times New Roman',
                          font_size=36,
                          x = 70, y=game_window.height-50,
                          anchor_x='center', anchor_y='center')
timer = pyglet.text.Label(str(time_countback),font_size=36,x=170, y=game_window.height-50,anchor_x='center', anchor_y='center')
score_label = pyglet.text.Label('Score :',
                          font_name='Times New Roman',
                          font_size=36,
                          x = WIDTH-200, y=game_window.height-50,
                          anchor_x='center', anchor_y='center')

score = pyglet.text.Label("0",font_size=36,x=WIDTH-100, y=game_window.height-50,anchor_x='center', anchor_y='center')
game_over_label = pyglet.text.Label('Game Over! Press Enter to play again!',
                          font_name='Times New Roman',
                          font_size=36,
                          x = WIDTH-550, y=HEIGHT/2,
                          anchor_x='center', anchor_y='center')

# Collision
colli_point = [[0,0],[0,0]]
def update_collision_point():
    half_x = basket_image.width/2
    half_y = basket_image.height/2
    global colli_point
    colli_point[0] = [basket[1].x - half_x+8, basket[1].y + half_y-8]
    colli_point[1] = [basket[1].x + half_x, basket[1].y + half_y-8]
def check_collision():
    global colli_point
    vecd0 = vector.sub(colli_point[0],[ball.x, ball.y])
    vecd1 = vector.sub(colli_point[1],[ball.x, ball.y])
    if vector.distance(colli_point[0], [ball.x,ball.y]) <= 60:
            return colli_point[0]
    elif vector.distance(colli_point[1], [ball.x,ball.y]) <= 60:
            return colli_point[1]
    else:
        return None
def update_score_point():
    global score_point, colli_point
    x = (colli_point[0][0] + colli_point[1][0])/2
    y = (colli_point[0][1] + colli_point[1][1])/2 - 20
    score_point = [x, y]
def update_order(Vx,Vy,dt):
    global t, v_init, has_scored, colli_point, START_POS, has_colli, score_point
    if v_init[1] > 0:
        if t > v_init[1]/abs(G): # is falling
            ball.group = mid     # change gourp
            basket[1].group = front
            #if check_collision() != None:   # if collide
                #reset_time()
                #reset_ball()
                #time.sleep(0.2)
            if check_collision() == colli_point[0]:
                has_colli = True
                reset_time()
                vec1 = vector.sub([ball.x, ball.y],colli_point[0])
                vec1 = vector.vec_x_float(vec1,2)
                v_init = vector.add(vec1,[Vx,Vy])
                v_init = vector.vec_x_float(v_init,5)
                START_POS[0] = ball.x
                START_POS[1] = ball.y
            elif check_collision() == colli_point[1]:
                has_colli = True
                reset_time()
                vec1 = vector.sub([ball.x, ball.y],colli_point[1])
                vec1 = vector.vec_x_float(vec1,2)
                v_init = vector.add(vec1,[Vx,Vy])
                v_init = vector.vec_x_float(v_init,5)
                START_POS[0] = ball.x
                START_POS[1] = ball.y
            if vector.distance([ball.x,ball.y],score_point) <= 50:
                has_scored = True
        else:
            ball.group = front
            basket[1].group = mid
def update_ball(dt):
    global t, v_init, can_play, Vx, Vy, has_colli, score_point, has_scored
    t += dt
    if has_colli is False:
        y = START_POS[1] + v_init[1]*t + 1/2*G*t*t
        if y < 0:
            y = 0
        x = START_POS[0] + v_init[0]*t
        ball.y = y
        ball.x = x
        if v_init[1] > 0:
            Vy = (v_init[1] + G*t)/4
            Vx = (v_init[0])/4
            update_order(Vx,Vy,dt)
        if t > 2*v_init[1]/abs(G) and v_init[1] > 0:
            reset_ball()
            reset_time()
    else:
        y = START_POS[1] + v_init[1]*t + 1/2*G*t*t
        if y < 0:
            y = 0
        x = START_POS[0] + v_init[0]*t
        ball.y = y
        ball.x = x
        if vector.distance([ball.x,ball.y],score_point) <= 50:
            has_scored = True
        if ball.y < 20 or t > 1.5:
            reset_ball()
            reset_time()
            has_colli = False

##### basket
def basket_random_location():
    x = randint(200,WIDTH-200)
    y = randint(500,HEIGHT-150)
    basket[0].x = x
    basket[0].y = y
    basket[1].x = x
    basket[1].y = y-110
def basket_patrol_location():
    x = randint(250, WIDTH - 100)   # 250 - 300
    y = randint(450, HEIGHT - 250)  # 450 - 550
    return [x - basket[0].x, y - basket[0].y]
patrol_location = []
### Mouse events
from pyglet.window import key
@game_window.event
def on_key_press(symbol, modifiers):
    global game_over
    if symbol == key.ENTER:
        game_over = False
        score.text = '0'
        reset_time()
        reset_ball()

@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global can_play
    if can_play is True:
        reset_time()
        if dy > 100:
            dy = 100
        if dy < 60:
            dy = 60
        if dy*15 + 100 < 1200:
            v_init[1] = dy*15 + 100
        else:
            v_init[1] = 1200
        v_init[0] = dx*10
@game_window.event
def on_mouse_release(x, y, buttons, modifiers):
    global can_play, has_scored
    can_play = False
    has_scored = False

i = 1
def basket_patrol():
    global patrol_location, can_patrol, hit_edge , i
    if can_patrol is True:
        vect = vector.nor(patrol_location)
        vect_opp = [vect[0]*-1,vect[1]*-1]
        basket[0].x += vect[0]*i
        basket[0].y += vect[1]*i
        basket[1].x += vect[0]*i
        basket[1].y += vect[1]*i
### Event loop  'game_window.on_mouse_release'
@game_window.event()
def event_loop(dt):
    global game_over
    if not game_over:
        basket_patrol()
        update_score_point()
        update_collision_point()
        update_ball(dt)



@game_window.event
def on_draw():
    global game_over
    if not game_over:
        game_window.clear()
        timer.draw()
        time_label.draw()
        score_label.draw()
        score.draw()
        ball.draw()
        batch.draw()
    else:
        game_window.clear()
        game_over_label.draw()
        player_score.draw()
player_score = pyglet.text.Label('Your score: ',
                          font_name='Times New Roman',
                          font_size=36,
                          x = WIDTH-500, y=HEIGHT/2 - 70,
                          anchor_x='center', anchor_y='center')
def clock(dt):
    global game_over
    if not game_over:
        timer.text = str(int(timer.text) - 1)
    half_x = basket_image.width/2
    half_y = basket_image.height/2
    global colli_point
    colli_point[0] = [basket[1].x - half_x+8, basket[1].y + half_y-8]
    colli_point[1] = [basket[1].x + half_x, basket[1].y + half_y-8]
    if int(timer.text) < 0:
        game_over = True
        timer.text = str(time_countback)
        player_score.text = 'Your score: ' + score.text
        basket[0].x = center_x
        basket[0].y = center_y
        basket[1].x = center_x
        basket[1].y = center_y - 110
def reset_time():
    global t
    t = 0
def reset_ball():
    global v_init, can_play, has_scored, can_patrol, patrol_location, game_over
    v_init = [0, 0]
    can_play = True
    START_POS[0] = WIDTH/2
    START_POS[1] = 0
    ball.x = START_POS[0]
    ball.y = START_POS[1]
    if has_scored is True:
        score.text = str(int(score.text) + 1)
        timer.text = str(time_countback)
        has_scored = False
        basket_random_location()
        if int(score.text) > 4:
            can_patrol = True
            patrol_location = basket_patrol_location()
    game_over = False
def reverse_patrol(dt):
    global i
    if i == 1:
        i = -1
    else:
        i = 1
pyglet.clock.schedule(event_loop)
pyglet.clock.schedule_interval(clock,1)
pyglet.clock.schedule_interval(reverse_patrol,3.5)
pyglet.app.run()
