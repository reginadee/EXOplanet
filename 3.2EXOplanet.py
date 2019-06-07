#This program was developed by the following authors: Jitdao Daocharatsaengchai, Lucy Lu, Pritha Sharma, Regina D'souza, Lisa Truong
#This program is a game, designed to simulate the invasion of aliens on earth.
#The game was developed in order to meet the specifications of Macquarie Fields Gaming Company and was submitted for stage 2 on the 5th of June 2019.
#Verision 3.1

#Initialising the game
import pygame
import random
import time
pygame.init()
#Sound effects utilised in the program
pygame.mixer.music.load("Main_game_song.wav")
lose_sound = pygame.mixer.Sound("Lose_song.wav")
win_sound = pygame.mixer.Sound("Cheer.wav")
gunshot = pygame.mixer.Sound("Gun.wav")
hit_sound = pygame.mixer.Sound("Hit.wav")

#The dimensions of the window and title
width = 800
height = 600
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("ExOplanet")

#defining colours
black    = [0,0,0]
white    = [255,255,255]
green    = [0,255,0]
red      = [255,0,0]
silver   = [192,192,192]

#loading images 
bg = pygame.image.load('1729.png')
char = pygame.image.load('standing.png')
clock = pygame.time.Clock()

#Loading the images for the man 1 to walk left and right
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'),
             pygame.image.load('R3.png'), pygame.image.load('R4.png'),
             pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'),
             pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'),
            pygame.image.load('L3.png'), pygame.image.load('L4.png'),
            pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'),
            pygame.image.load('L9.png')]
#Loading the images for the man 2(2 players) to walk left and right
Right = [pygame.image.load('S1.png'), pygame.image.load('S2.png'),
             pygame.image.load('S3.png'), pygame.image.load('S4.png'),
             pygame.image.load('S5.png'), pygame.image.load('S6.png'),
             pygame.image.load('S7.png'), pygame.image.load('S8.png'),
             pygame.image.load('S9.png')]
Left = [pygame.image.load('T1.png'), pygame.image.load('T2.png'),
            pygame.image.load('T3.png'), pygame.image.load('T4.png'),
            pygame.image.load('T5.png'), pygame.image.load('T6.png'),
            pygame.image.load('T7.png'), pygame.image.load('T8.png'),
            pygame.image.load('T9.png')]
#Images for bullets to shoot left and right (Player 1)
bullet_right = pygame.image.load('bullet.png')
bullet_left = pygame.image.load('bullet left.png')
#Images for swords to throw left and right (Player2)
sword_right = pygame.image.load('swordright1.png')
sword_left = pygame.image.load('swordleft1.png')

#Ground 
ground = pygame.image.load('ground.png')
ground_rect_position = ground.get_rect()
#position of rect
ground_rect_position.topleft = (0,560)

#PLATFORMS IN THE GAME
#Platform 1 
Plat = pygame.image.load('Block.pur.png')
Plat_rect_position = Plat.get_rect()
#position of rect
Plat_rect_position.topleft = (200,400)

#Platform 2
Plat1 = pygame.image.load('Block.pur1.png')
Plat_rect_position1 = Plat1.get_rect()
Plat_rect_position1.topleft = (320,350)

#Platform 3
Plat2 = pygame.image.load('Block.pur1.png')
Plat2_rect_position2 = Plat2.get_rect()
Plat2_rect_position2.topleft = (100,460)

#Platform 4 (long)
Long_Plat = pygame.image.load('Longblock3.png')
Long_Plat_rect_position = Long_Plat.get_rect()
Long_Plat_rect_position.topleft = (-30,170)

#Platform 5 (long)
Long_Plat2 = pygame.image.load('Longblock2.png')
Long_Plat2_rect_position = Long_Plat2.get_rect()
Long_Plat2_rect_position.topleft = (547,250)

#moving platform
M_Plat = pygame.image.load('Block.two.png')
M_Plat_rect_position = M_Plat.get_rect()
M_Plat_rect_position.topleft = (500,150)

#Platform 6
Plat3 = pygame.image.load('Block.pur1.png')
Plat_rect_position3 = Plat3.get_rect()
Plat_rect_position3.topleft = (300,100)

#Platform 7
Plat4 = pygame.image.load('block.one.png')
Plat_rect_position4 = Plat4.get_rect()
Plat_rect_position4.topleft = (450,255)

#door
door = pygame.image.load('door.png')
door_rect_position =  door.get_rect()
door_rect_position.topleft = (25,125)


#define speed of rect
speed = [-2, 0.5]

# set the score to zero
score = 0
endgame = 0
keys = pygame.key.get_pressed()
restart = False
pause = False
#functions todisplay text 
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((width/2),(height/2))
    win.blit(TextSurf, TextRect)
    pygame.display.update()


class player(object):
#define the attributes of the player
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 8
        self.life = 10
        self.standing = True
        self.hitbox = (self.x +17, self.y + 11, 29, 52)
        self.health = 10
        self.visible = True
#How the man walks       
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 

        if not (self.standing):
            if self.left:#If player is walking left,increment walkcount
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:#If player is walking right, increment walkcount
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:#Player remains in the direction he stands in 
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))
        
        man = player(0, 500, 64,64)
        #health box of the player
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
#Collision involving player
    def collide(self,xVel,yVel,platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i):
                if xVel > 0:
                    self.rect.right = i.rect.left
                if xVel < 0:
                    self.rect.left = i.rect.right
                if yVel > 0:
                    self.rect.bottom = i.rect.top
                if yVel < 0:
                    self.rect.top = i.rect.bottom

    def keys(self):
        keys = pygame.key.get_pressed()
        shootLoop = 0
        global facing
        #When the space bar key is pressed the bullet will shoot correspondingly 

        if keys[pygame.K_SPACE] and shootLoop == 0:
            gunshot.play()
            if man.left:
                facing = -1
            else:
                facing = 1
                
            if len(bullets) < 20:
                bullets.append(projectile(round(man.x + man.width //2),
                                          round(man.y + man.height//2),
                                          6, (0,0,0), facing))
            
            shootLoop = 1

    #Keys for the movement of man
        if keys[pygame.K_LEFT] and man.x > man.vel:#When he is walking left
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
            
        elif keys[pygame.K_RIGHT] and man.x < 800 - man.width - man.vel:#when is he walking right
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0

        
#Function to decrement the health bar of the man
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def do(self):
        self.draw(win)
        self.keys()
        
#============================= Player two ======================#
class player_two(object):
#define the attributes of the man
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 8
        self.life = 10 
        self.standing = True
        self.hitbox = (self.x +17, self.y + 11, 29, 52)
        self.health = 10
        self.visible = True
#How the man walks       
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 

        if not (self.standing):
            if self.left:
                win.blit(Left[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(Right[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(Right[0], (self.x, self.y))
            else:
                win.blit(Left[0], (self.x, self.y))
                
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
#collision invovling player 2
    def collide(self,xVel,yVel,platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i):
                if xVel > 0:
                    self.rect.right = i.rect.left
                if xVel < 0:
                    self.rect.left = i.rect.right
                if yVel > 0:
                    self.rect.bottom = i.rect.top
                if yVel < 0:
                    self.rect.top = i.rect.bottom

    def keys(self):
        keys = pygame.key.get_pressed()
        shootLoop = 0
        global facing
        #When the space bar key is pressed the bullet will shoot correspondingly 

        if keys[pygame.K_f] and shootLoop == 0:
            gunshot.play()
            if man2.left:
                facing = -1
            else:
                facing = 1
                
            if len(bullets) < 5:
                bullets.append(projectile_two(round(man2.x + man2.width //2),
                                              round(man2.y + man2.height//2),
                                              6, (0,0,0), facing))

            shootLoop = 1

    #Keys for the movement of man
        if keys[pygame.K_a] and man2.x > man2.vel:#left
            man2.x -= man.vel
            man2.left = True
            man2.right = False
            man2.standing = False
            
        elif keys[pygame.K_d] and man2.x < 800 - man2.width - man2.vel:#right
            man2.x += man.vel
            man2.right = True
            man2.left = False
            man2.standing = False
        else:
            man2.standing = True#standing
            man2.walkCount = 0

        
#Function to decrement the health bar of the man
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def do(self):
        self.draw(win)
        self.keys()
        
#================== Bullets ==========================#
class projectile(object):
#Defining the attributes of the projectiles
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
#Drawing the bullets
    def draw(self,win):
        if man.left:
            win.blit(bullet_left, (self.x, self.y))
        else:
            win.blit(bullet_right, (self.x, self.y))


class projectile_two(object):
#Defining the variables of the projectiles
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
#Draw the bullets
    def draw(self,win):
        if man2.right:
            win.blit(sword_right, (self.x, self.y))
        else:
            win.blit(sword_left, (self.x, self.y))


class enemy(object):
#Loading the images of of the sprite to walk left or right
    def __init__(self, x, y, width, height, end, normal):
        self.walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),
                 pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),
                 pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),
                 pygame.image.load('R9E.png'), pygame.image.load('R10E.png'),
                 pygame.image.load('R11E.png')]
        self.walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'),
                pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),
                pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'),
                pygame.image.load('L9E.png'), pygame.image.load('L10E.png'),
                pygame.image.load('L11E.png')]
#attributes of the aliens
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        self.normal = normal
#Speed of the alien
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
#health bar of enemy 
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

#How fast the alien moves
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
#When the health bar of the alien decrements               
    def hit(self):
        if self.health > 0: # Checks his hp
            # Enemy is still alive, minus 1 hp
            self.health -= 1
        else: # He's dead
            if self.normal == 0: # If the enemy can morph (Not normal alien)
                # Change to other form- slime
                self.walkRight = [pygame.image.load('R1A.png'), pygame.image.load('R2A.png'),
                             pygame.image.load('R3A.png'), pygame.image.load('R4A.png'),
                             pygame.image.load('R5A.png'), pygame.image.load('R6A.png'),
                             pygame.image.load('R7A.png'), pygame.image.load('R8A.png'),
                             pygame.image.load('R9A.png'), pygame.image.load('R10A.png'),
                             pygame.image.load('R11A.png'),pygame.image.load('R12A.png')]
                self.walkLeft = [pygame.image.load('L1A.png'), pygame.image.load('L2A.png'),
                             pygame.image.load('L3A.png'), pygame.image.load('L4A.png'),
                             pygame.image.load('L5A.png'), pygame.image.load('L6A.png'),
                             pygame.image.load('L7A.png'), pygame.image.load('L8A.png'),
                             pygame.image.load('L9A.png'), pygame.image.load('L10A.png'),
                             pygame.image.load('L11A.png'),pygame.image.load('L12A.png')]
                self.health = 10 # Put hp back to 10
                self.normal = 1 # Set him to normal so he dies after next death
            else: # He is normal
                self.kill()

    def kill(self):
        self.visible = False # Make him no longer invisible
        self.x = -100 # Put him off the screen
        self.y = -100

#================================= Lose Page ===============#
def lose():
    #sound files
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(lose_sound)
    
    #Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
                pygame.quit()
                quit()
#background               
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
#Title
        largeText = pygame.font.Font('space_invaders.ttf',100) # This displays the title of the game on the start menu
        TextSurf, TextRect = text_objects("You Lose!", largeText)
        TextRect.center = (400,300)
        win.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None
#Quit Button

        pygame.draw.rect(win, silver,(400,400,100,50))#Turns grey when not hovered on
#This is the interactive feature, where if you hover over the button it will light up        
        if 400+100 > mouse[0] > 400 and 400+50 > mouse[1] > 400:
            pygame.draw.rect(win, black,(400,400,100,50))#Turns white when hovered on
            action = "Quit"
            if click[0] == 1 and action != None:#when action does not equal to none and is clicked, it will call the start menu function
                pygame.mixer.Sound.stop(lose_sound)#Sound is played when clicked
                startmenu()

        else:
            pygame.draw.rect(win, silver,(400,400,100,50))#Turns grey when not hovered on
#Text to display on the button             
        smallText = pygame.font.Font("space_invaders.ttf",10)
        textSurf, textRect = text_objects("Quit", smallText)
        textRect.center = ( (400+(100/2)), (400+(50/2)) )
        win.blit(textSurf, textRect)
#Again
        pygame.draw.rect(win, silver,(200,400,100,50))#Turns grey when not hovered on
        #This is the interactive feature, where if you hover over the button it will light up        
        if 200+100 > mouse[0] > 200 and 400+50> mouse[1] > 400:
            pygame.draw.rect(win, black,(200,400,100,50))#Turns white when hovered on
            action = "howef"
            if click[0] == 1 and action != None:#when action does not equal to none and is clicked, it will call the start menu function
              chooseplayers()#calls the chooseplayer function and displays the players page
        else:
            pygame.draw.rect(win, silver,(200,400,100,50))#Turns grey when not hovered on
 #Text to display the "again" text on the button            
        smallText = pygame.font.Font("space_invaders.ttf",10)
        textSurf, textRect = text_objects("Again", smallText)
        textRect.center = ( (200+(100/2)), (400+(50/2)) )
        win.blit(textSurf, textRect)
        
        

#Update screen
        pygame.display.update()
        clock.tick(15)

#=========================== Win page =======================#
def win_page():
#Sound files
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(win_sound)
    #Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
                pygame.quit()
                quit()
#background               
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
#Title
        largeText = pygame.font.Font('space_invaders.ttf',100) # This displays the title of the game on the start menu
        TextSurf, TextRect = text_objects("You Won!", largeText)
        TextRect.center = (400,300)
        win.blit(TextSurf, TextRect)
#Back Button
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None
#Quit
        pygame.draw.rect(win, silver,(400,400,100,50))#Turns grey when not hovered on
        #This is the interactive feature, where if you hover over the button it will light up        
        if 400+100 > mouse[0] > 400 and 400+50 > mouse[1] > 400:
            pygame.draw.rect(win, black,(400,400,100,50))#Turns white when hovered on
            action = "How to play"
            if click[0] == 1 and action != None:
                startmenu()#calls the startmenu function when quit is clicked

        else:
            pygame.draw.rect(win, silver,(400,400,100,50))#Turns grey when not hovered on
#Text to display "quit" on the button
        smallText = pygame.font.Font("space_invaders.ttf",10)
        textSurf, textRect = text_objects("Quit", smallText)
        textRect.center = ( (400+(100/2)), (400+(50/2)) )
        win.blit(textSurf, textRect)
#Again
        pygame.draw.rect(win, silver,(200,400,100,50))#Turns grey when not hovered on
        #This is the interactive feature, where if you hover over the button it will light up        
        if 200+100 > mouse[0] > 200 and 400+50> mouse[1] > 400:
            pygame.draw.rect(win, black,(200,400,100,50))#Turns white when hovered on
            action = "howef"
            if click[0] == 1 and action != None:
              chooseplayers()#calls players function to display the players pages
        else:
            pygame.draw.rect(win, silver,(200,400,100,50))#Turns grey when not hovered on
 #Text to display "again" on the button
           
        smallText = pygame.font.Font("space_invaders.ttf",10)
        textSurf, textRect = text_objects("Again", smallText)
        textRect.center = ( (200+(100/2)), (400+(50/2)) )
        win.blit(textSurf, textRect)
        
        

#update screen
        pygame.display.update()
        clock.tick(15)

#======================== Start Page ===============================#
#function for "How to play" page
def Instructions():
#Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
#Background of the window               
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
# This displays the title of the game on the start menu
        largeText = pygame.font.Font('regular.ttf',50) 
        TextSurf, TextRect = text_objects("How to play!", largeText)
        TextRect.center = ((width/2),(height/5))
        win.blit(TextSurf, TextRect)

#Back Button
        pygame.draw.rect(win, silver,(50,50,100,50))# Silver button

#Gathers the position of the mouse                            
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None

#This is the interactive feature: if you hover over the button it turns black and when clicked it will return to the home screen       
        if 50+100 > mouse[0] > 50 and 50+50 > mouse[1] > 50:
            pygame.draw.rect(win, black,(50,50,100,50))#Turns white when hovered on
            action = "How to play"
            if click[0] == 1 and action != None:
              done = True # Flag that we are done so we exit this loop
        else:
            pygame.draw.rect(win, silver,(50,50,100,50))#Remains silver when not hovered on
# Text indicating "back"
        smallText = pygame.font.Font("lioncub.ttf",30) 
        textSurf, textRect = text_objects("Back", smallText)
        textRect.center = ( (50+(100/2)), (50+(50/2)) )
        win.blit(textSurf, textRect)
        
#Instructions               
        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("1.Use arrows - P1/WASD- P2 to move", smallText)
        textRect.center = ( (400, 230) )
        win.blit(textSurf, textRect)
        
        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("2. Avoid aliens - if aliens hit you, you will lose a life", smallText)
        textRect.center = ( (400, 280) )
        win.blit(textSurf, textRect)

        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("3.Kill all aliens by using the space bar - P1 or F key - P2", smallText)
        textRect.center = ( (400, 330) )
        win.blit(textSurf, textRect)

        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("4.To pause the game use the P key. To quit the game use the Q key", smallText)
        textRect.center = ( (400, 380) )
        win.blit(textSurf, textRect)

        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("5.Exit to the door when all aliens are killed", smallText)
        textRect.center = ( (400, 430) )
        win.blit(textSurf, textRect)

        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("6. Check if your score made the scoreboard", smallText)
        textRect.center = ( (400, 480) )
        win.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(15)

#Function for the players page
def chooseplayers():
    #Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
        
#Background               
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
# This displays the title of the game on the start menu        
        largeText = pygame.font.Font('regular.ttf',50) 
        TextSurf, TextRect = text_objects("Players", largeText)
        TextRect.center = ((width/2),(height/5))
        win.blit(TextSurf, TextRect)


#Gathers mouse positon                             
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None
#Buttons for 1 or 2 Player
#This is the interactive feature, where if you hover over the button it will turn black and when clicked on willl direct you to the game
#Player 1 Button
        if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(win, black,(150,450,100,50))#Turns black when hovered on
            action = "Player 1"
            if click[0] == 1 and action != None:
                    Main_one()
        else:
            pygame.draw.rect(win, silver,(150,450,100,50))#Remains grey when not hovered on
            
        smallText = pygame.font.Font("lioncub.ttf",30)# Text
        textSurf, textRect = text_objects(" 1 Player ", smallText)
        textRect.center = ( (150+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)
#Player 2 Button
        
        if 550+100 > mouse[0] > 550 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(win, black,(550,450,100,50))#Turns black when hovered on
            action = "Player 2"
            if click[0] == 1 and action != None:#when the button is clicked on, the button will go it its coressponding function
                Main_two()
        else:
            pygame.draw.rect(win, silver,(550,450,100,50))#Turns silver when not hovered on
        smallText = pygame.font.Font("lioncub.ttf",30) # This print the text on top of the button
        textSurf, textRect = text_objects("2 Players ", smallText)#Text- "Leadership"
        textRect.center = ( (550+(100/2)), (450+(50/2)) )#The text is centred
        win.blit(textSurf, textRect)

#Back Button
        pygame.draw.rect(win, silver,(50,50,100,50))#Turns grey when not hovered on
        #This is the interactive feature, where if you hover over the button it will light up        
        if 50+100 > mouse[0] > 50 and 50+50 > mouse[1] > 50:
            pygame.draw.rect(win, black,(50,50,100,50))#Turns white when hovered on
            action = "How to play"
            if click[0] == 1 and action != None:
              done = True # Flag that we are done so we exit this loop
        else:
            pygame.draw.rect(win, silver,(50,50,100,50))#Turns grey when not hovered on
            
        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("Back", smallText)
        textRect.center = ( (50+(100/2)), (50+(50/2)) )
        win.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)
#Function to display leasership page 
def leadership():
#Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
#Background                
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
#Title
        largeText = pygame.font.Font('regular.ttf',30) # This displays the title of the game on the start menu
        TextSurf, TextRect = text_objects("Leadership", largeText)
        TextRect.center = (400,50)
        win.blit(TextSurf, TextRect)
#Reads the text file from the score1.txt and sorts the array- for player 1
        scoreArr = []
        f1 = open("scores1.txt", "r")
        for x in f1: # For every line in the text file
            #print(x) # This is the score for each line
            if x.strip().isdigit():
                #print("Number", x)
                scoreArr.append(int(x.strip()))
        scoreArr = sorted(scoreArr, reverse = True) # Sort array

        f1.close()

# Reads the text file from the score2.txt and sorts the array- for  Two players
        scoreArr2 = []
        f2 = open("scores2.txt", "r")
        for x in f2: # For every line in the text file
            #print(x) # This is the score for each line
            if x.strip().isdigit():
                scoreArr2.append(int(x.strip()))
        scoreArr2 = sorted(scoreArr2, reverse = True) # Sort array

          
        f2.close()
#Text displayed on leadership board
#one player
        smallText = pygame.font.Font("lioncub.ttf",50)
        textSurf, textRect = text_objects("One player", smallText)
        textRect.center = ( (200+(100/2)), (90+(50/2)) )
        win.blit(textSurf, textRect)
#first
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("1st", smallText)
        textRect.center = ( (100+(100/2)), (150+(50/2)) )
        win.blit(textSurf, textRect)
#2nd
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("2nd", smallText)
        textRect.center = ( (100+(100/2)), (250+(50/2)) )
        win.blit(textSurf, textRect)
#3rd
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("3rd", smallText)
        textRect.center = ( (100+(100/2)), (350+(50/2)) )
        win.blit(textSurf, textRect)
#4th
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("4th", smallText)
        textRect.center = ( (100+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)
#5th
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("5th", smallText)
        textRect.center = ( (100+(100/2)), (540+(50/2)) )
        win.blit(textSurf, textRect)
#score 1
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr[0]), smallText)
        textRect.center = ( (290+(100/2)), (150+(50/2)) )
        win.blit(textSurf, textRect)
#score 2
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr[1]), smallText)
        textRect.center = ( (290+(100/2)), (250+(50/2)) )
        win.blit(textSurf, textRect)

#score 3
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr[2]), smallText)
        textRect.center = ( (290+(100/2)), (350+(50/2)) )
        win.blit(textSurf, textRect)

#score 4
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr[3]), smallText)
        textRect.center = ( (290+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)

#score 5
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr[4]), smallText)
        textRect.center = ( (290+(100/2)), (540+(50/2)) )
        win.blit(textSurf, textRect)

#two player title
        smallText = pygame.font.Font("lioncub.ttf",50)
        textSurf, textRect = text_objects("Two players", smallText)
        textRect.center = ( (510+(100/2)), (90+(50/2)) )
        win.blit(textSurf, textRect)
#first
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("1st", smallText)
        textRect.center = ( (400+(100/2)), (150+(50/2)) )
        win.blit(textSurf, textRect)
#2nd
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("2nd", smallText)
        textRect.center = ( (400+(100/2)), (250+(50/2)) )
        win.blit(textSurf, textRect)
#3rd
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("3rd", smallText)
        textRect.center = ( (400+(100/2)), (350+(50/2)) )
        win.blit(textSurf, textRect)
#4th
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("4th", smallText)
        textRect.center = ( (400+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)
#5th
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects("5th", smallText)
        textRect.center = ( (400+(100/2)), (540+(50/2)) )
        win.blit(textSurf, textRect)
#score 1
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr2[0]), smallText)
        textRect.center = ( (590+(100/2)), (150+(50/2)) )
        win.blit(textSurf, textRect)
#score 2
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr2[1]), smallText)
        textRect.center = ( (590+(100/2)), (250+(50/2)) )
        win.blit(textSurf, textRect)

#score 3
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr2[2]), smallText)
        textRect.center = ( (590+(100/2)), (350+(50/2)) )
        win.blit(textSurf, textRect)

#score 4
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr2[3]), smallText)
        textRect.center = ( (590+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)

#score 5
        smallText = pygame.font.Font("lioncub.ttf",50)#Text-"back"
        textSurf, textRect = text_objects(str(scoreArr2[4]), smallText)
        textRect.center = ( (590+(100/2)), (540+(50/2)) )
        win.blit(textSurf, textRect)        
                
                
#Back Button
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None

        pygame.draw.rect(win, silver,(50,50,100,50))#Rectangle

        if 50+100 > mouse[0] > 50 and 50+50 > mouse[1] > 50:
            pygame.draw.rect(win, black,(50,50,100,50))#Turns black when hovered on
            action = "How to play"
            if click[0] == 1 and action != None:
               done = True # Flag that we are done so we exit this loop
        else:
            pygame.draw.rect(win, silver,(50,50,100,50))#Remains grey when not hovered on
#Text-"back"
        smallText = pygame.font.Font("lioncub.ttf",30)
        textSurf, textRect = text_objects("Back", smallText)
        textRect.center = (100,75)
        win.blit(textSurf, textRect)
#Update the screen
        pygame.display.update()
        clock.tick(15)

        
def startmenu():
#Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
                pygame.quit()
#The background of the startmenu
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
#Buttons that will be on the start menu                             
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None

#This is the interactive feature, where if you hover over the button it will light up

#How to play Button
        if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(win, black,(150,450,100,50))#Turns black when hovered on
            action = "How to play"
            if click[0] == 1 and action != None:
                Instructions()#displays the instructions page when clicked on 
        else:
            pygame.draw.rect(win, silver,(150,450,100,50))#Remains silver when not hovered on
            
        smallText = pygame.font.Font("lioncub.ttf",25)#Text
        textSurf, textRect = text_objects("How to play", smallText)
        textRect.center = ( (150+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)
#Play Button
        if 350+100 > mouse[0] > 350 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(win, black,(350,450,100,50))#Turns black when hovered on
            action = "Play!"
            if click[0] == 1 and action != None:
                chooseplayers()#displays the players page when clicked on
        else:
            pygame.draw.rect(win, silver,(350,450,100,50))#Remains silver when not hovered on
#Text to display text 
        smallText = pygame.font.Font("lioncub.ttf",30)#Text
        textSurf, textRect = text_objects("Play!", smallText)
        textRect.center = ( (350+(100/2)), (450+(50/2)) )
        win.blit(textSurf, textRect)
#Leadership Button
        if 550+100 > mouse[0] > 550 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(win, black,(550,450,100,50))#Turns black when hovered on
            action = "Leadership"
            if click[0] == 1 and action != None:#when the button is clicked on, the button will go it its coressponding function
                leadership()#displays the leadership page
        else:
            pygame.draw.rect(win, silver,(550,450,100,50))#Remains silver when not hovered on
        smallText = pygame.font.Font("lioncub.ttf",25) # This print the text on top of the button
        textSurf, textRect = text_objects("Leadership", smallText)#Text will say "Leadership"
        textRect.center = ( (550+(100/2)), (450+(50/2)) )#The text is centred
        win.blit(textSurf, textRect)
#title of the game 
        largeText = pygame.font.Font('LKT.ttf',80) # This displays the title of the game on the start menu
        TextSurf, TextRect = text_objects("ExOplanet", largeText)
        TextRect.center = ((width/2),(height/2))
        win.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

            
# Go ahead and update the screen with what we've drawn.
#Update screen
    pygame.display.flip()
    clock.tick(20)
#===================================================================#
#Page when the game is paused 
def paused():
    keys = pygame.key.get_pressed()
    pygame.mixer.music.stop()
    #Loop until the user clicks the close button.
    done = False
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
                pygame.quit()
                quit()          
            
#background               
        bg = pygame.image.load("stars2.jpeg")
        win.blit(bg, (0, 0))
#Title
        largeText = pygame.font.Font('space_invaders.ttf',100) # This displays the title of the game on the start menu
        TextSurf, TextRect = text_objects("Paused!", largeText)
        TextRect.center = (400,300)
        win.blit(TextSurf, TextRect)
#Back Button
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        action = None
#Quit
        pygame.draw.rect(win, silver,(400,400,100,50))#Turns grey when not hovered on
        #This is the interactive feature, where if you hover over the button it will light up        
        if 400+100 > mouse[0] > 400 and 400+50 > mouse[1] > 400:
            pygame.draw.rect(win, black,(400,400,100,50))#Turns white when hovered on
            action = "How to play"
            if click[0] == 1 and action != None:
                startmenu()#calls the start menu page 

        else:
            pygame.draw.rect(win, silver,(400,400,100,50))#Turns grey when not hovered on
#Text to display quit           
        smallText = pygame.font.Font("space_invaders.ttf",10)
        textSurf, textRect = text_objects("Quit", smallText)
        textRect.center = ( (400+(100/2)), (400+(50/2)) )
        win.blit(textSurf, textRect)
#Again
        pygame.draw.rect(win, silver,(200,400,100,50))#Turns grey when not hovered on
        #This is the interactive feature, where if you hover over the button it will light up        
        if 200+100 > mouse[0] > 200 and 400+50> mouse[1] > 400:
            pygame.draw.rect(win, black,(200,400,100,50))#Turns white when hovered on
            action = "howef"
            if click[0] == 1 and action != None:
                  unpaused()
        else:
            pygame.draw.rect(win, silver,(200,400,100,50))#Turns grey when not hovered on
#text displaying "continue"         
        smallText = pygame.font.Font("space_invaders.ttf",10)
        textSurf, textRect = text_objects("Continue", smallText)
        textRect.center = ( (200+(100/2)), (400+(50/2)) )
        win.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)

def unpaused():
    global paused
    pygame.mixer.music.play(-1)
    pause = False
    
def restart():
    restart = True
    if restart:
        Main_one()

    else:
        pygame.exit()

#Draws the sprites, window, score       
def redrawGameWindow():
    win.blit(bg, (0,0))#setting the screen at 0, 0
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (650, 10))
    man.draw(win)
 #bliting the platforms onto the screen   
    win.blit(ground,ground_rect_position)
    win.blit(Plat,Plat_rect_position)
    win.blit(Plat1,Plat_rect_position1)
    win.blit(Plat2,Plat2_rect_position2)
    win.blit(Long_Plat,Long_Plat_rect_position)
    win.blit(Long_Plat,Long_Plat2_rect_position)
    win.blit(M_Plat,M_Plat_rect_position)
    win.blit(door,door_rect_position)
    win.blit(Plat3,Plat_rect_position3)
    win.blit(Plat4,Plat_rect_position4)
    goblin.draw(win)
    goblin2.draw(win)
    goblin3.draw(win)
    goblin4.draw(win)
    #pygame.image.load("door.png")
    
    
    for bullet in bullets:
        bullet.draw(win)
        
#mainloop
#assigning players/ enemys on screen through classes defined before
font = pygame.font.SysFont('arial', 30, True)
man = player(0, 500, 64,64)
man2 = player_two(710,500,64,64)
goblin = enemy(100, 510, 64, 64, 450, 0)
goblin2 = enemy(0, 114, 64, 64, 200, 1)
goblin3 = enemy(300, 292, 64, 64, 400, 1)
goblin4 = enemy(550, 194, 64, 64, 750, 0)
font = pygame.font.SysFont('arial', 30, True)
bullets = []

#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- ONE PLAYER -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def Main_one():
#global variables
    global score
    global M_Plat_rect_position
    global M_Plat
    global endgame
    global pause
    global keys
    shootLoop = 0
    pygame.mixer.music.play(-1)
    
    run = True 

    while run:
        clock.tick(50)    
        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0
 #loop for quit       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.music.stop()
                startmenu()
 #When p is pressed, the game will be paused               
            if keys[pygame.K_p]:
                paused()
#When the key q is pressed the game will quit 
            if keys[pygame.K_q]:
                pygame.quit()
                quit()
           
        man.do()
        
    #When the bullets hit the enemies the score will increment
    #sound will play when hit
    #the goblin's health bar will decrement 
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hit_sound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))


            if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
                if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                    hit_sound.play()
                    goblin2.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    
            if bullet.y - bullet.radius < goblin3.hitbox[1] + goblin3.hitbox[3] and bullet.y + bullet.radius > goblin3.hitbox[1]:
                if bullet.x + bullet.radius > goblin3.hitbox[0] and bullet.x - bullet.radius < goblin3.hitbox[0] + goblin3.hitbox[2]:
                    hit_sound.play()
                    goblin3.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
            if bullet.y - bullet.radius < goblin4.hitbox[1] + goblin4.hitbox[3] and bullet.y + bullet.radius > goblin4.hitbox[1]:
                if bullet.x + bullet.radius > goblin4.hitbox[0] and bullet.x - bullet.radius < goblin4.hitbox[0] + goblin4.hitbox[2]:
                    hit_sound.play()
                    goblin4.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    
                    
            if bullet.x < 800 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
                
    #To decrease the health bar of the man and decrement the score when player touches the alien
    #When the player's health bar is less than zero the lose screen will pop up
    #For goblin 1
        if goblin.y > man.y > goblin.y-60:
            if (goblin.vel > 0 and goblin.x-25 < man.x < goblin.x) or  (goblin.vel < 0 and goblin.x < man.x < goblin.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                   #end screen
    #For the second goblin
        if goblin2.y > man.y > goblin2.y-60:
            if (goblin2.vel > 0 and goblin2.x-25 < man.x < goblin2.x) or  (goblin2.vel < 0 and goblin2.x < man.x < goblin2.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                    # end screen
    #For the third goblin
        if goblin3.y > man.y > goblin3.y-60:
            if (goblin3.vel > 0 and goblin3.x-25 < man.x < goblin3.x) or  (goblin3.vel < 0 and goblin3.x < man.x < goblin3.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                    # end screen
     #For the fourth goblin
        if goblin4.y > man.y > goblin4.y-60:
            if (goblin4.vel > 0 and goblin4.x-25 < man.x < goblin4.x) or  (goblin4.vel < 0 and goblin4.x < man.x < goblin4.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                    # end screen

    #If the man stands at the door
        if (door_rect_position.left-20 < man.x < door_rect_position.right-25) and (door_rect_position.top-50 < man.y< door_rect_position.bottom+40):
            if goblin.health <= 0 and  goblin2.health <= 0 and  goblin3.health <= 0 and  goblin4.health <= 0:
                if endgame == 0:
                    endgame = 1
                    score = score
                    # Writing tothe text file score.txt to record the player's score
                    f = open("scores1.txt", "a")
                    f.write("\n"+str(score))
                    f.close()
                    win_page()
                # won screen is displayed as the game has finished 
            
        keys = pygame.key.get_pressed()
        #print(pygame.mouse.get_pos())

        #moving picture
        M_Plat_rect_position = M_Plat_rect_position.move(speed)
        #through vel variable assigns value to position variable
        if M_Plat_rect_position.left < 400 or M_Plat_rect_position.right > 600:
            #Flipping picture
            M_Plat = pygame.transform.flip(M_Plat, True, False)
            speed[0] = -speed[0]
        #moving in the opposite direction
        if M_Plat_rect_position.top < 0 or M_Plat_rect_position.bottom > 600:
            speed[1] = -speed[1]

    
        if not(man.isJump): # If man is not jumping 
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
            # Add gravity to person when not jumping

            gravity = 20
            #if (man.x < Plat_rect_position.left-40) or (man.x > Plat_rect_position.right-25):
            doesHeFall = 0

            # If the player's X and Y coordinates is within these coordinates, the man will fall 
            if not (
                    ((man.x > ground_rect_position.left) and (man.x < ground_rect_position.right)
                        and (man.y+60 < ground_rect_position.top) and (man.y+60 > ground_rect_position.top))
                        or
                        ((man.x > Plat_rect_position.left-40) and (man.x < Plat_rect_position.right-25)
                        and (man.y+60 < Plat_rect_position.top+10) and (man.y+60 > Plat_rect_position.top-5))
                        or
                        ((man.x > Plat_rect_position1.left - 40) and (man.x < Plat_rect_position1.right-25)
                        and (man.y+60 < Plat_rect_position1.top+10) and (man.y+60 > Plat_rect_position1.top-5))
                        or
                        ((man.x > Plat2_rect_position2.left - 40) and (man.x < Plat2_rect_position2.right-25)
                        and (man.y+60 < Plat2_rect_position2.top+10) and (man.y+60 > Plat2_rect_position2.top-5))
                        or
                        ((man.x > M_Plat_rect_position.left-40) and (man.x < M_Plat_rect_position.right-25)
                        and (man.y+60 < M_Plat_rect_position.top+10) and (man.y+60 > M_Plat_rect_position.top-5))
                        or
                        ((man.x > Long_Plat_rect_position.left-40) and (man.x < Long_Plat_rect_position.right-24)
                        and (man.y+60 < Long_Plat_rect_position.top+10) and (man.y+60 > Long_Plat_rect_position.top-5))
                        or
                        ((man.x > Long_Plat2_rect_position.left-40) and (man.x < Long_Plat2_rect_position.right-24)
                        and (man.y+60 < Long_Plat2_rect_position.top+10) and (man.y+60 > Long_Plat2_rect_position.top-5))
                        or
                        ((man.x > Plat_rect_position3.left-40) and (man.x < Plat_rect_position3.right-24)
                        and (man.y+60 < Plat_rect_position3.top+10) and (man.y+60 > Plat_rect_position3.top-5))
                        or
                        ((man.x > Plat_rect_position4.left-40) and (man.x < Plat_rect_position4.right-24)
                        and (man.y+60 < Plat_rect_position4.top+10) and (man.y+60 > Plat_rect_position4.top-5))
                    
                       ):

                doesHeFall = 1

            if (doesHeFall):
                if (man.y < 500):
                    man.isJump = True
                    man.jumpCount = -1
        
        else: # Else man is jumping
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
#This makes sure to make the player land on the platforms. The jumpcount is set to -11 to ensure he doesnt jump
                # Box 0
                if (man.x > Plat_rect_position.left-40) and (man.x < Plat_rect_position.right-25) and (man.y+60 < Plat_rect_position.top+35) and (man.y+60 > Plat_rect_position.top-15):
                    if (man.jumpCount < 0): # If he's falling down
                        man.y = Plat_rect_position.top-60
                        man.jumpCount = -11 # Make him stop falling from the jump
                
                # Box 1
                if ((man.x > Plat_rect_position1.left-40) and (man.x < Plat_rect_position1.right-25) and
                    (man.y+60 < Plat_rect_position1.top+35) and (man.y+60 > Plat_rect_position1.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat_rect_position1.top-60
                        man.jumpCount = -11
                # Box 2
                if ((man.x > Plat2_rect_position2.left-40) and (man.x < Plat2_rect_position2.right-25) and
                    (man.y+60 < Plat2_rect_position2.top+35) and (man.y+60 > Plat2_rect_position2.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat2_rect_position2.top-60
                        man.jumpCount = -11

                # Box 3 (Long platform)
                if ((man.x > Long_Plat_rect_position.left-40) and (man.x < Long_Plat_rect_position.right-24) and
                    (man.y+60 < Long_Plat_rect_position.top+10) and (man.y+60 > Long_Plat_rect_position.top-5)):
                    if (man.jumpCount < 0):
                        man.y = Long_Plat_rect_position.top-60
                        man.jumpCount = -11
                        
                # Box 4 (Long platform)
                if ((man.x > Long_Plat2_rect_position.left-40) and (man.x < Long_Plat2_rect_position.right-24) and
                    (man.y+60 < Long_Plat2_rect_position.top+10) and (man.y+60 > Long_Plat2_rect_position.top-5)):
                    if (man.jumpCount < 0):
                        man.y = Long_Plat2_rect_position.top-60
                        man.jumpCount = -11
                

                # Box moving platform
                if ((man.x > M_Plat_rect_position.left-40) and (man.x < M_Plat_rect_position.right-25) and
                    (man.y+60 < M_Plat_rect_position.top+35) and (man.y+60 > M_Plat_rect_position.top-15)):
                    if (man.jumpCount < 0):
                        man.y = M_Plat_rect_position.top-60
                        man.jumpCount = -11

                # Box 6
                if ((man.x > Plat_rect_position3.left-40) and (man.x < Plat_rect_position3.right-25) and
                    (man.y+60 < Plat_rect_position3.top+35) and (man.y+60 > Plat_rect_position3.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat_rect_position3.top-60
                        man.jumpCount = -11

                # Box 7
                if ((man.x > Plat_rect_position4.left-40) and (man.x < Plat_rect_position4.right-25) and
                    (man.y+60 < Plat_rect_position4.top+35) and (man.y+60 > Plat_rect_position4.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat_rect_position4.top-60
                        man.jumpCount = -11

                    
#Calculations for the man to fall 
                        
                if (man.jumpCount != -11):
                    man.y -= (man.jumpCount ** 2) * 0.5 * neg
#decrement the man's jumpcount 
                man.jumpCount -= 1
#The man stays on the platform 
                if (man.y > 500):
                    man.jumpCount = -11
                    man.y = 500
            else:
                man.isJump = False
                man.jumpCount = 8
#update screen
        redrawGameWindow()
        clock.tick(110) 
        pygame.display.update()

#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- TWO PLAYER -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
def Main_two():
#Global variables
    global score
    global M_Plat_rect_position
    global M_Plat
    global endgame
    shootLoop = 0
    pygame.mixer.music.play(-1)

    run = True 

    while run:
        clock.tick(50)    
        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0
#To quit           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.music.stop()
                startmenu()
#To pause               
            if keys[pygame.K_p]:
                paused()
# Quit
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        man.do()
        man2.do()
#Player 1        
#When the bullets hit the enemies their health bar will decrement. Scores will be incrementing by 1 and a sound effect will be played        
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hit_sound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))


            if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
                if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                    hit_sound.play()
                    goblin2.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    
            if bullet.y - bullet.radius < goblin3.hitbox[1] + goblin3.hitbox[3] and bullet.y + bullet.radius > goblin3.hitbox[1]:
                if bullet.x + bullet.radius > goblin3.hitbox[0] and bullet.x - bullet.radius < goblin3.hitbox[0] + goblin3.hitbox[2]:
                    hit_sound.play()
                    goblin3.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
            if bullet.y - bullet.radius < goblin4.hitbox[1] + goblin4.hitbox[3] and bullet.y + bullet.radius > goblin4.hitbox[1]:
                if bullet.x + bullet.radius > goblin4.hitbox[0] and bullet.x - bullet.radius < goblin4.hitbox[0] + goblin4.hitbox[2]:
                    hit_sound.play()
                    goblin4.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    
                    
            if bullet.x < 800 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
#To decrease the health bar of the 2nd player and decrement the score when he touches the alien. Scores will increment by one and sound effects will be played 
    #For goblin 1
        if goblin.y > man.y > goblin.y-60:
            if (goblin.vel > 0 and goblin.x-25 < man.x < goblin.x) or  (goblin.vel < 0 and goblin.x < man.x < goblin.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                    # end screen
    #For the second goblin
        if goblin2.y > man.y > goblin2.y-60:
            if (goblin2.vel > 0 and goblin2.x-25 < man.x < goblin2.x) or  (goblin2.vel < 0 and goblin2.x < man.x < goblin2.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                    # end screen
    #For the third goblin
        if goblin3.y > man.y > goblin3.y-60:
            if (goblin3.vel > 0 and goblin3.x-25 < man.x < goblin3.x) or  (goblin3.vel < 0 and goblin3.x < man.x < goblin3.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()
                    # end screen
     #For the fourth goblin
        if goblin4.y > man.y > goblin4.y-60:
            if (goblin4.vel > 0 and goblin4.x-25 < man.x < goblin4.x) or  (goblin4.vel < 0 and goblin4.x < man.x < goblin4.x + 25):
                man.hit()
                score -= 1
                if (man.health <= 0):
                    lose()

                   # end screen
#When the player wins
#For goblin 1    
        if goblin.y > man2.y > goblin.y-60:
            if ((goblin.vel > 0 and goblin.x-25 < man2.x < goblin.x) or
               (goblin.vel < 0 and goblin.x < man2.x < goblin.x + 25)):
               
                man2.hit()
                score -= 1
                if (man2.health <= 0):
                    lose()
                    #end screen 
#For second goblin
        if goblin2.y > man2.y > goblin2.y-60:
            if ((goblin2.vel > 0 and goblin2.x-25 < man2.x < goblin2.x) or
               (goblin2.vel < 0 and goblin2.x < man2.x < goblin2.x + 25)):
            
                man2.hit()
                score -= 1
                if (man2.health <= 0):
                    lose()
           # end screen

#For the third goblin
        if goblin3.y > man2.y > goblin3.y-60:
            if ((goblin3.vel > 0 and goblin3.x-25 < man2.x < goblin3.x) or
                (goblin3.vel < 0 and goblin3.x < man.x < goblin3.x + 25)):
                man2.hit()
                score -= 1
                if (man2.health <= 0):
                    lose()
                    # end screen
#For the fourth goblin
        if goblin4.y > man2.y > goblin4.y-60:
            if ((goblin4.vel > 0 and goblin4.x-25 < man2.x < goblin4.x) or
               (goblin4.vel < 0 and goblin4.x < man2.x < goblin4.x + 25)):
                man2.hit()
                score -= 1
                if (man2.health <= 0):
                    lose()
                    # end screen

    #If the man stands at the door
        if ((door_rect_position.left-20 < man.x < door_rect_position.right-25) and
            (door_rect_position.top-50 < man.y< door_rect_position.bottom+40)):
            if goblin.health <= 0 and  goblin2.health <= 0 and  goblin3.health <= 0 and  goblin4.health <= 0:
                if endgame == 0:
                    endgame = 1
                    score = score
                    # Writing to the text file when the game ends. The score will be saved and sorted later on the leadership board. 
                    f = open("scores2.txt", "a")
                    f.write("\n"+str(score))
                    f.close()
                    win_page()
        #Win screen displayed 
            
        keys = pygame.key.get_pressed()

        #moving picture
        M_Plat_rect_position = M_Plat_rect_position.move(speed)
        #through vel variable assigns value to position variable
        if M_Plat_rect_position.left < 400 or M_Plat_rect_position.right > 600:
            #Flipping picture
            M_Plat = pygame.transform.flip(M_Plat, True, False)
            speed[0] = -speed[0]
        #moving in the opposite direction
        if M_Plat_rect_position.top < 0 or M_Plat_rect_position.bottom > 600:
            speed[1] = -speed[1]

        
        if not(man.isJump): # If man is not jumping 
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
            # Add gravity to person when not jumping

            gravity = 20
            doesHeFall = 0

            # When the player is not within these coordinates, he will fall
            if not (
                    ((man.x > ground_rect_position.left) and (man.x < ground_rect_position.right)
                        and (man.y+60 < ground_rect_position.top) and (man.y+60 > ground_rect_position.top))
                        or
                        ((man.x > Plat_rect_position.left-40) and (man.x < Plat_rect_position.right-25)
                        and (man.y+60 < Plat_rect_position.top+10) and (man.y+60 > Plat_rect_position.top-5))
                        or
                        ((man.x > Plat_rect_position1.left - 40) and (man.x < Plat_rect_position1.right-25)
                        and (man.y+60 < Plat_rect_position1.top+10) and (man.y+60 > Plat_rect_position1.top-5))
                        or
                        ((man.x > Plat2_rect_position2.left - 40) and (man.x < Plat2_rect_position2.right-25)
                        and (man.y+60 < Plat2_rect_position2.top+10) and (man.y+60 > Plat2_rect_position2.top-5))
                        or
                        ((man.x > M_Plat_rect_position.left-40) and (man.x < M_Plat_rect_position.right-25)
                        and (man.y+60 < M_Plat_rect_position.top+10) and (man.y+60 > M_Plat_rect_position.top-5))
                        or
                        ((man.x > Long_Plat_rect_position.left-40) and (man.x < Long_Plat_rect_position.right-24)
                        and (man.y+60 < Long_Plat_rect_position.top+10) and (man.y+60 > Long_Plat_rect_position.top-5))
                        or
                        ((man.x > Long_Plat2_rect_position.left-40) and (man.x < Long_Plat2_rect_position.right-24)
                        and (man.y+60 < Long_Plat2_rect_position.top+10) and (man.y+60 > Long_Plat2_rect_position.top-5))
                        or
                        ((man.x > Plat_rect_position3.left-40) and (man.x < Plat_rect_position3.right-24)
                        and (man.y+60 < Plat_rect_position3.top+10) and (man.y+60 > Plat_rect_position3.top-5))
                        or
                        ((man.x > Plat_rect_position4.left-40) and (man.x < Plat_rect_position4.right-24)
                        and (man.y+60 < Plat_rect_position4.top+10) and (man.y+60 > Plat_rect_position4.top-5))
                    
                       ):

                doesHeFall = 1
#if the player is above the ground he will fall
            if (doesHeFall):
                if (man.y < 500):
                    man.isJump = True
                    man.jumpCount = -1
        
        else: # Else man is jumping
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
          
   #If he is on the platform he will stop jumping
                # Box 0
                if (man.x > Plat_rect_position.left-40) and (man.x < Plat_rect_position.right-25) and (man.y+60 < Plat_rect_position.top+35) and (man.y+60 > Plat_rect_position.top-15):
                    if (man.jumpCount < 0): # If he's falling down
                        man.y = Plat_rect_position.top-60
                        man.jumpCount = -11 # Make him stop falling from the jump
                
                # Box 1
                if ((man.x > Plat_rect_position1.left-40) and (man.x < Plat_rect_position1.right-25) and
                    (man.y+60 < Plat_rect_position1.top+35) and (man.y+60 > Plat_rect_position1.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat_rect_position1.top-60
                        man.jumpCount = -11
                # Box 2
                if ((man.x > Plat2_rect_position2.left-40) and (man.x < Plat2_rect_position2.right-25) and
                    (man.y+60 < Plat2_rect_position2.top+35) and (man.y+60 > Plat2_rect_position2.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat2_rect_position2.top-60
                        man.jumpCount = -11

                # Box 3 (Long platform)
                if ((man.x > Long_Plat_rect_position.left-40) and (man.x < Long_Plat_rect_position.right-24) and
                    (man.y+60 < Long_Plat_rect_position.top+10) and (man.y+60 > Long_Plat_rect_position.top-5)):
                    if (man.jumpCount < 0):
                        man.y = Long_Plat_rect_position.top-60
                        man.jumpCount = -11
                        
                # Box 4 (Long platform)
                if ((man.x > Long_Plat2_rect_position.left-40) and (man.x < Long_Plat2_rect_position.right-24) and
                    (man.y+60 < Long_Plat2_rect_position.top+10) and (man.y+60 > Long_Plat2_rect_position.top-5)):
                    if (man.jumpCount < 0):
                        man.y = Long_Plat2_rect_position.top-60
                        man.jumpCount = -11
                

                # Box moving platform
                if ((man.x > M_Plat_rect_position.left-40) and (man.x < M_Plat_rect_position.right-25) and
                    (man.y+60 < M_Plat_rect_position.top+35) and (man.y+60 > M_Plat_rect_position.top-15)):
                    if (man.jumpCount < 0):
                        man.y = M_Plat_rect_position.top-60
                        man.jumpCount = -11

                # Box 6
                if ((man.x > Plat_rect_position3.left-40) and (man.x < Plat_rect_position3.right-25) and
                    (man.y+60 < Plat_rect_position3.top+35) and (man.y+60 > Plat_rect_position3.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat_rect_position3.top-60
                        man.jumpCount = -11

                # Box 7
                if ((man.x > Plat_rect_position4.left-40) and (man.x < Plat_rect_position4.right-25) and
                    (man.y+60 < Plat_rect_position4.top+35) and (man.y+60 > Plat_rect_position4.top-15)):
                    if (man.jumpCount < 0):
                        man.y = Plat_rect_position4.top-60
                        man.jumpCount = -11

                    

 #calculations to fall                       
                if (man.jumpCount != -11):
                    man.y -= (man.jumpCount ** 2) * 0.5 * neg
#Player remains on the platform 
                man.jumpCount -= 1
                if (man.y > 500):
                    man.jumpCount = -11
                    man.y = 500
            else:
                man.isJump = False
                man.jumpCount = 8
        #------------------------------ for player two ---------------------------------------------------------#
        if not(man2.isJump): # If man is not jumping 
            if keys[pygame.K_w]:
                man2.isJump = True
                man2.right = False
                man2.left = False
                man2.walkCount = 0
            # Add gravity to person when not jumping

            gravity = 20
            doesHeFall = 0

            # If he is not within these coordinates, he will fall down 
            if not (
                    ((man2.x > ground_rect_position.left) and (man2.x < ground_rect_position.right)
                        and (man2.y+60 < ground_rect_position.top) and (man2.y+60 > ground_rect_position.top))
                        or
                        ((man2.x > Plat_rect_position.left-40) and (man2.x < Plat_rect_position.right-25)
                        and (man2.y+60 < Plat_rect_position.top+10) and (man2.y+60 > Plat_rect_position.top-5))
                        or
                        ((man2.x > Plat_rect_position1.left - 40) and (man2.x < Plat_rect_position1.right-25)
                        and (man2.y+60 < Plat_rect_position1.top+10) and (man2.y+60 > Plat_rect_position1.top-5))
                        or
                        ((man2.x > Plat2_rect_position2.left - 40) and (man2.x < Plat2_rect_position2.right-25)
                        and (man2.y+60 < Plat2_rect_position2.top+10) and (man2.y+60 > Plat2_rect_position2.top-5))
                        or
                        ((man2.x > M_Plat_rect_position.left-40) and (man2.x < M_Plat_rect_position.right-25)
                        and (man2.y+60 < M_Plat_rect_position.top+10) and (man2.y+60 > M_Plat_rect_position.top-5))
                        or
                        ((man2.x > Long_Plat_rect_position.left-40) and (man2.x < Long_Plat_rect_position.right-24)
                        and (man2.y+60 < Long_Plat_rect_position.top+10) and (man2.y+60 > Long_Plat_rect_position.top-5))
                        or
                        ((man2.x > Long_Plat2_rect_position.left-40) and (man2.x < Long_Plat2_rect_position.right-24)
                        and (man2.y+60 < Long_Plat2_rect_position.top+10) and (man2.y+60 > Long_Plat2_rect_position.top-5))
                        or
                        ((man2.x > Plat_rect_position3.left-40) and (man2.x < Plat_rect_position3.right-24)
                        and (man2.y+60 < Plat_rect_position3.top+10) and (man2.y+60 > Plat_rect_position3.top-5))
                        or
                        ((man2.x > Plat_rect_position4.left-40) and (man2.x < Plat_rect_position4.right-24)
                        and (man2.y+60 < Plat_rect_position4.top+10) and (man2.y+60 > Plat_rect_position4.top-5))
                    
                       ):

                doesHeFall = 1
#To ensure the man falls when he is above the ground, y = 500 
            if (doesHeFall):
                if (man2.y < 500):
                    man2.isJump = True
                    man2.jumpCount = -1
        
        else: # Else man is jumping
            if man2.jumpCount >= -10:
                neg = 1
                if man2.jumpCount < 0:
                    neg = -1
#To ensure the man doesnt fall when he is on a plaform 
                # Box 0
                if ((man2.x > Plat_rect_position.left-40) and (man2.x < Plat_rect_position.right-25) and
                    (man2.y+60 < Plat_rect_position.top+35) and (man2.y+60 > Plat_rect_position.top-15)):
                    if (man2.jumpCount < 0): # If he's falling down
                        man2.y = Plat_rect_position.top-60
                        man2.jumpCount = -11 # Make him stop falling from the jump
                
                # Box 1
                if ((man2.x > Plat_rect_position1.left-40) and (man2.x < Plat_rect_position1.right-25) and
                    (man2.y+60 < Plat_rect_position1.top+35) and (man2.y+60 > Plat_rect_position1.top-15)):
                    if (man2.jumpCount < 0):
                        man2.y = Plat_rect_position1.top-60
                        man2.jumpCount = -11
                # Box 2
                if ((man2.x > Plat2_rect_position2.left-40) and (man2.x < Plat2_rect_position2.right-25) and
                    (man2.y+60 < Plat2_rect_position2.top+35) and (man2.y+60 > Plat2_rect_position2.top-15)):
                    if (man2.jumpCount < 0):
                        man2.y = Plat2_rect_position2.top-60
                        man2.jumpCount = -11

                # Box 3 (Long platform)
                if ((man2.x > Long_Plat_rect_position.left-40) and (man2.x < Long_Plat_rect_position.right-24) and
                    (man2.y+60 < Long_Plat_rect_position.top+10) and (man2.y+60 > Long_Plat_rect_position.top-5)):
                    if (man2.jumpCount < 0):
                        man2.y = Long_Plat_rect_position.top-60
                        man2.jumpCount = -11
                        
                # Box 4 (Long platform)
                if ((man2.x > Long_Plat2_rect_position.left-40) and (man2.x < Long_Plat2_rect_position.right-24) and
                    (man2.y+60 < Long_Plat2_rect_position.top+10) and (man2.y+60 > Long_Plat2_rect_position.top-5)):
                    if (man2.jumpCount < 0):
                        man2.y = Long_Plat2_rect_position.top-60
                        man2.jumpCount = -11
                

                # Box moving platform
                if ((man2.x > M_Plat_rect_position.left-40) and (man2.x < M_Plat_rect_position.right-25) and
                    (man2.y+60 < M_Plat_rect_position.top+35) and (man2.y+60 > M_Plat_rect_position.top-15)):
                    if (man2.jumpCount < 0):
                        man2.y = M_Plat_rect_position.top-60
                        man2.jumpCount = -11

                # Box 6
                if ((man2.x > Plat_rect_position3.left-40) and (man2.x < Plat_rect_position3.right-25) and
                    (man2.y+60 < Plat_rect_position3.top+35) and (man2.y+60 > Plat_rect_position3.top-15)):
                    if (man2.jumpCount < 0):
                        man2.y = Plat_rect_position3.top-60
                        man2.jumpCount = -11

                # Box 7
                if ((man2.x > Plat_rect_position4.left-40) and (man2.x < Plat_rect_position4.right-25) and
                    (man2.y+60 < Plat_rect_position4.top+35) and (man2.y+60 > Plat_rect_position4.top-15)):
                    if (man2.jumpCount < 0):
                        man2.y = Plat_rect_position4.top-60
                        man2.jumpCount = -11

                    
#Calculations of how the man falls 
                        
                if (man2.jumpCount != -11):
                    man2.y -= (man2.jumpCount ** 2) * 0.5 * neg

                man2.jumpCount -= 1
#The man remains on the platform 
                if (man2.y > 500):
                    man2.jumpCount = -11
                    man2.y = 500
            else:
                man2.isJump = False
                man2.jumpCount = 8

        
                
    #update the screen
        redrawGameWindow()
        man2.draw(win)
        clock.tick(300) 
        pygame.display.update()

startmenu()
pygame.quit()
