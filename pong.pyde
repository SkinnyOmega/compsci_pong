add_library('minim')
Paddle = None
Score = None
Wall = None

def setup():
    #ball variables
    global ball_x, ball_y, ball_xspeed, ball_yspeed
    ball_x = 400
    ball_y = 300
    ball_xspeed = 10
    ball_yspeed = 0
    
    #paddle1 variables
    global P1pos, P2pos, P1speed, P2speed, Pspeed
    P1pos = 280
    P2pos = 280
    P1speed = 0
    P2speed = 0
    Pspeed = 7
    
    #Points
    global P1p, P2p, winner
    P1p = 0
    P2p = 0
    winner = 0
    
    #game states
    global menu, playing, score_pause, win, instructions
    menu = True
    playing = False
    score_pause = False
    win = False
    instructions = False
    
    #counter 
    global counter
    counter = 0
    
    #images
    global menuImg, instructionsImg, endImg
    menuImg = loadImage("Menu.png")
    instructionsImg = loadImage("Instructions.png")
    endImg = loadImage("End.png")
    
    #sounds 
    minim = Minim(this)
    global Paddle, Score, Wall
    Paddle = minim.loadSample("Paddle.mp3")
    Score = minim.loadSample("Score.mp3")
    Wall = minim.loadSample("Wall.mp3")

    
    #text font
    FFFFORWA = createFont("FFFFORWA.TTF", 64)
    textFont(FFFFORWA)

    size(800,600)
    stroke(255)
    
def draw():
    global menu, playing, score_pause, win, instructions
    global P1p, P2p, winner
    global counter
    
    if counter > 0:
        counter -= 1
    
    if counter == 0 and score_pause == True:
        playing = True
        score_pause = False
    
    if (menu == True):
        image(menuImg, 0, 0)
    
    if (menu == False and instructions == True):
        image(instructionsImg, 0, 0)
        
    if P1p == 5:
        win = True
        playing = False
        winner = 1
    
    if P2p == 5:
        win = True
        playing = False
        winner = 2
    
    if win == True:
         game_end()
        
    if (playing == True):
        game()
    
    if (playing == False and score_pause == True and counter > 0):
        game_pause()
    
def game():
    background()
    ball()
    paddle()
    score()

def game_pause():
    global counter
    background()
    paddle()
    score()
    
def game_end():
    global winner
    text1 = "Player " + str(winner) + " won"
    image(endImg, 0, 0)
    text(text1, 150, 200)
    text(P1p, 200, 400)
    text(P2p, 600, 400)

def background():
    fill(0)
    rect(0,0,800,600)
    fill(255)
    #dotted middle line
    for i in range(30):
        rect(398, 5 + i * 30, 4, 10)
    
def ball():
    global ball_x, ball_y, ball_xspeed, ball_yspeed
    global P1pos, P2pos
    global P1p, P2p
    global menu, playing, score_pause, win, instructions
    global counter
    
    
    ball_x += ball_xspeed
    ball_y += ball_yspeed
    #ball top/bottom collison
    if (ball_y <= 0 or ball_y >= 590):
        ball_yspeed *= -1
        Wall.trigger()
        
    #ball paddle1 collision
    if (ball_x <= 50 and ball_x >= 48):
        for i in range(5):
            if (ball_y > P1pos - 10 + i* 10 and ball_y <= P1pos + i * 10):
                ball_xspeed *= -1
                ball_yspeed = -2*(2 - i)
                Paddle.trigger()
                
    #ball paddle2 collision
    if (ball_x >= 740 and ball_x <= 748):
        for i in range(5):
            if (ball_y > P2pos - 10 + i* 10 and ball_y <= P2pos + i * 10):
                ball_xspeed *= -1
                ball_yspeed = -2*(2 - i)
                Paddle.trigger()
                
   
    #ball out of bounds check
    if ball_x <= 0:
        ball_x = 400
        ball_y = 300 
        ball_yspeed = 0
        P2p += 1
        playing = False
        score_pause = True
        counter = 100
        Score.trigger()

    if ball_x >= 800:
        ball_x = 400
        ball_y = 300
        ball_yspeed = 0
        P1p += 1
        playing = False
        score_pause = True
        counter = 100
        Score.trigger()
        
    fill(255)
    rect(ball_x, ball_y, 10, 10)
         
def paddle():
    global P1pos, P2pos, P1speed, P2speed, Pspeed
    fill(255)
    P1pos += P1speed
    P2pos += P2speed
    rect(50,P1pos,10,40)
    rect(740,P2pos,10,40)
    
    #paddle out of bounds check
    if P1pos >= 580:
        P1pos = -20   
    elif P1pos <= -20:
        P1pos = 580
        
    if P2pos >= 580:
        P2pos = -20   
    elif P2pos <= -20:
        P2pos = 580
    
def score():
    text(P1p, 200, 120)
    text(P2p, 600, 120)
    
def keyPressed():
    global P1pos, P2pos, P1speed, P2speed, Pspeed
    global P1p, P2p
    global menu, playing, score_pause, win, instructions
    if  ((key == 'w') or (key == 'W')):
        P1speed = -Pspeed
    if  ((key == 's') or (key == 'S')):
        P1speed = Pspeed

    if  (keyCode == UP):
        P2speed = -Pspeed
    if  (keyCode == DOWN):
        P2speed = Pspeed
        
    if (key == ' ' and win == True):
        win = False
        P1p = 0
        P2p = 0
        menu = True
        playing = False
        score_pause = False
        instructions = False
        
def keyReleased():
    global P1pos, P2pos, P1speed, P2speed, Pspeed
    if  ((key == 'w') or (key == 'W')):
        P1speed = 0
    if  ((key == 's') or (key == 'S')):
        P1speed = 0

    if  (keyCode == UP):
        P2speed = 0
    if  (keyCode == DOWN):
        P2speed = 0
        
def mousePressed():
    global menu, playing, score_pause, win, instructions
    global counter
    if (mouseX > 240 and mouseX < 560 and mouseY > 240 and mouseY < 300 and menu == True):
        counter = 100
        menu = False
        score_pause = True
        
    if (mouseX > 220 and mouseX < 580 and mouseY > 340 and mouseY < 420 and menu == True):
        menu = False
        instructions = True
    
    if (mouseX > 60 and mouseX < 320 and mouseY > 470 and mouseY < 540 and instructions == True):
        menu = True
        instructions = False
