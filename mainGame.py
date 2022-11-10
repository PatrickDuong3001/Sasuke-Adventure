import pygame
import os
import sys
import cv2
import numpy as np
import pickle
import threading
import time

class character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 100
        self.max_health = self.health
        self.update_time = pygame.time.get_ticks()
        self.cooldown_jutsu_duration = 0
        self.action_type = 0
        self.character_direct = 1
        self.flip_character = False
        self.f_ind = 0    
        self.animation_list = []    
        animation_types = ["stand", "run","fire"]
        
        for animation in animation_types:
            temp = []
            for i in range(len(os.listdir(f'animation/{animation}'))):
                img = pygame.image.load(f'animation/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(2*img.get_width()), int(2*img.get_height())))
                temp.append(img)
            self.animation_list.append(temp)
        self.image = self.animation_list[self.action_type][self.f_ind]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.animate_updater()
        #self.check_alive()
        #update cooldown
        if self.cooldown_jutsu_duration > 0:
            self.cooldown_jutsu_duration -= 1
            
    def animate_updater(self):
        #based on current frame, updating image
        self.image = self.animation_list[self.action_type][self.f_ind]
        if pygame.time.get_ticks() - self.update_time > 70:
            self.update_time = pygame.time.get_ticks()
            self.f_ind += 1
        if self.f_ind >= len(self.animation_list[self.action_type]):
            if self.action_type == 3:
                self.f_ind = len(self.animation_list[self.action_type]) - 1
            else:
                self.f_ind = 0

    def action_updater(self, action):
        #check if the new action is different to the previous one
        if action != self.action_type:
            self.action_type = action
            #update the animation settings
            self.f_ind = 0
            self.update_time = pygame.time.get_ticks()
            
    def fireJutsu(self):
        if self.cooldown_jutsu_duration == 0:
            self.cooldown_jutsu_duration = 30
            fire = FireJutsu(0.6*self.rect.size[0] * self.character_direct + self.rect.centerx, self.rect.centery-10, self.character_direct)
            fire_sprite_group.add(fire)

    def character_movements(self, left_move, right_move):
        dx = 0
        dy = 0
        global fire_flip
        if right_move:
            if self.rect.x <= width - 80:
                dx = 5
            self.flip_character = False
            fire_flip = False
            self.character_direct = 1
        if left_move:
            if self.rect.x >= 1:
                dx = -5
            fire_flip = True
            self.flip_character = True
            self.character_direct = -1
        if down_move:
            if self.rect.y <= height - 100:
                dy = 3
        if up_move:
            if self.rect.y >= 10:
                dy = -3        
        self.rect.y += dy
        self.rect.x += dx
    
    def draw_character(self):
        screen.blit(pygame.transform.flip(self.image, self.flip_character, False), self.rect)
        

class FireJutsu(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        if fire_flip:
            self.image = fire_ball_flip
        else:
            self.image = fire_ball
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.character_direct = direction

    def update(self):
        self.rect.x += (self.character_direct * 5)
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()

class handTracker:
    import mediapipe as mp
    def __init__(self):
        self.hands = self.mp.solutions.hands.Hands(static_image_mode=False,max_num_hands=1,min_detection_confidence=0.5,min_tracking_confidence=0.5)
        self.width=1280
        self.height=720
        self.cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
        self.cam.set(cv2.CAP_PROP_FPS, 30)
        self.keyPoints=[0,4,5,9,13,17,8,12,16,20]
        with open('handsigns.pkl','rb') as f:
            self.gestNames=pickle.load(f)
            self.knownGestures=pickle.load(f)
    
    def findDistances(self,handData):
        distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
        palmSize=((handData[0][0]-handData[9][0])**2+(handData[0][1]-handData[9][1])**2)**(1./2.)
        for row in range(0,len(handData)):
            for column in range(0,len(handData)):
                distMatrix[row][column]=(((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.))/palmSize
        return distMatrix
            
    def Marks(self,frame):
            myHands=[]
            frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            results=self.hands.process(frameRGB)
            if results.multi_hand_landmarks != None:
                for handLandMarks in results.multi_hand_landmarks:
                    myHand=[]
                    for landMark in handLandMarks.landmark:
                        myHand.append((int(landMark.x*self.width),int(landMark.y*self.height)))
                    myHands.append(myHand)
            return myHands
        
    def findGesture(self,unknownGesture,knownGestures,keyPoints,gestNames,tol):
        errorArray=[]
        for i in range(0,len(gestNames),1):
            error=self.findError(knownGestures[i],unknownGesture,keyPoints)
            errorArray.append(error)
        errorMin=errorArray[0]
        minIndex=0
        for i in range(0,len(errorArray),1):
            if errorArray[i]<errorMin:
                errorMin=errorArray[i]
                minIndex=i
        if errorMin<tol:
            gesture=gestNames[minIndex]
        if errorMin>=tol:
            gesture='Unknown'
        return gesture
    
    def findError(self,gestureMatrix,unknownMatrix,keyPoints):
        error=0
        for row in keyPoints:
            for column in keyPoints:
                error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
        return error
    
    def run(self):
        global handsigns
        while True:
            ignore, frame = self.cam.read()
            frame=cv2.resize(frame,(self.width,self.height))
            handData=self.Marks(frame)
            if handData!=[]:
                unknownGesture=self.findDistances(handData[0])
                myGesture=self.findGesture(unknownGesture,self.knownGestures,self.keyPoints,self.gestNames,10)
                if jutsu_perform == True and (myGesture != 'Unknown') and len(handsigns) < 4 and (myGesture not in handsigns):
                    print(myGesture)
                    handsigns.append(myGesture)
class setCheck:
    def __init__(self):
        self.fire_style = ["three","four","one","five"]
        self.chidori = ["two","four","one","five"]
        self.karin = [] #define later
    
    def compareHandSign(self):
        if handsigns[0] == "three" and handsigns[1] == "four" and handsigns[2] == "one" and handsigns[3] == "two":
            print("Hello")
            return 1
        return -1
        
        
##############################################################Main Game########################################################################
handsigns = [] #set of handsigns
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# width, height = screen.get_size()
width = 800
height = 640
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Test')
clock = pygame.time.Clock()

#player controls
left_move = False
right_move = False
fire_shoot = False
up_move = False
down_move = False
fire_flip = False
fire_shoot_stance = False
fire_shoot_stance_dur = 0
jutsu_perform = False

fire_ball = pygame.image.load('fire.png').convert_alpha()
fire_ball_flip = pygame.transform.flip(fire_ball,True,False)
fire_sprite_group = pygame.sprite.Group()
sasuke = character(50, 200)

BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():  #temp
    screen.fill(BG)

#set comparator
handSignTracker = setCheck()

#camera on
handtrack = handTracker()
my_thread = threading.Thread(target=handtrack.run,daemon=True)
my_thread.start()

run = True

while run:
    clock.tick(60)
    draw_bg() #temp
    
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$player and enemies control$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    sasuke.update()
    sasuke.draw_character()

    fire_sprite_group.update()
    fire_sprite_group.draw(screen)
    if sasuke.alive:
        #shoot bullets
        if fire_shoot_stance:
            if fire_shoot_stance_dur == 20:
                fire_shoot_stance_dur = 0
                fire_shoot_stance = False
            sasuke.action_updater(2)
            fire_shoot_stance_dur += 1
            if fire_shoot:
                sasuke.fireJutsu()
                fire_shoot = False
                jutsu_perform = False          #set false to disable hand sign detection. User has to press c every time to perform a jutsu
                handsigns.clear()              #clear handsigns list to prepare for next jutsu
        elif left_move or right_move or up_move or down_move:
            sasuke.action_updater(1)
        else:
            sasuke.action_updater(0)
        sasuke.character_movements(left_move, right_move)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$hand signs detection controls$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    if len(handsigns) == 4 and jutsu_perform == True:                 
        if handSignTracker.compareHandSign() == 1:
            fire_shoot_stance = True
            fire_shoot = True
        elif handSignTracker.compareHandSign() == 2:
            print("Place Holder")
        else: 
            handsigns.clear()          #the user performs wrong handsigns, so clear handsigns list
                
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$keyboard detection$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        #keys free
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up_move = False
            if event.key == pygame.K_s:
                down_move = False
            if event.key == pygame.K_a:
                left_move = False
            if event.key == pygame.K_d:
                right_move = False
            
        #keys pushed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up_move = True
            if event.key == pygame.K_s:
                down_move = True
            if event.key == pygame.K_a:
                left_move = True
            if event.key == pygame.K_d:
                right_move = True
            if event.key == pygame.K_c:    #press c to start recording handsigns. Press again to cancel
                if jutsu_perform == True:
                    jutsu_perform = False
                    handsigns.clear()
                else: 
                    jutsu_perform = True

    #$$$$$$$$$$$$$$$$$$$$$$$$Map control$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    pygame.display.update()
print(handsigns)
pygame.quit()
sys.exit()

