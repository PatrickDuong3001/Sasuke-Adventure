import pygame
import sys
import cv2
import numpy as np
import pickle
import threading
from character import character 
from zetsu import zetsu
from handSignChecker import handSignChecker
from explosion import explosion
from minion import minion

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
##############################################################Main Game########################################################################
handsigns = [] #set of handsigns
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# width, height = screen.get_size()
width = 800
height = 640
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Test')
clock = pygame.time.Clock()
pygame.font.init()

#player controls
left_move = False
right_move = False
fire_shoot = False
up_move = False
down_move = False
HP_font = pygame.font.Font("font.TTF",20)
HP = HP_font.render("HP:",True,"Red")

#basic attack
basic_attack = False
basic_attack_dur = 0

#fire style jutsu
fire_shoot_stance = False
fire_shoot_stance_dur = 0
jutsu_perform = False

#chidori jutsu
chidori_stance = False
chidori_dur = 0
facing_right = True #helpful for chidori move
chidori_right = False
chidori_left = False

#enemies controls
enemySpeed = 0
enemyAttack = False
sasukeAttack = False
idle = True
water_shoot = False
water_stance = False 
water_dur = 0

sasuke = character(50, 200, width, height, screen)
zetsu_1 = zetsu(500,500,width,height,screen)
minion_1 = minion(600,200,width,height,screen)
explode_sprite_group = pygame.sprite.Group()

BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():  #temp background
    screen.fill(BG)

#set comparator
handSignTracker = handSignChecker()

#camera on to detect hand gestures
handtrack = handTracker()
my_thread = threading.Thread(target=handtrack.run,daemon=True)
my_thread.start()

run = True
while run:
    clock.tick(60)
    draw_bg() #temp background
    screen.blit(HP,(5,5))
    
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$player and enemies control$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    sasuke.update()
    sasuke.draw_character()
    sasuke.health_bar_draw()
    
    sasuke.fire_sprite_update()
    
    if sasuke.checkAlive:
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
        elif chidori_stance:
            if chidori_dur <= 40:
                sasuke.action_updater(3)
            elif chidori_dur > 40 and chidori_dur < 90: 
                if facing_right:
                    chidori_right = True
                else: 
                    chidori_left = True
                sasuke.action_updater(4)
                sasuke.chidori_move(chidori_left,chidori_right)
            else: 
                chidori_stance = False
                jutsu_perform = False
                chidori_dur = 0
                chidori_left = False
                chidori_right = False
                handsigns.clear()
            chidori_dur += 1
        elif basic_attack:
            if basic_attack_dur == 25:
                basic_attack = False
                basic_attack_dur = 0
            sasuke.action_updater(5)
            basic_attack_dur += 1
        elif left_move or right_move or up_move or down_move:
            sasuke.action_updater(1)
        else:
            sasuke.action_updater(0)
        if not chidori_stance:
            sasuke.character_movements(left_move, right_move,down_move,up_move)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$hand signs detection controls$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    if len(handsigns) == 4 and jutsu_perform == True:                 
        if handSignTracker.compareHandSign(handsigns) == 1: #fire style
            fire_shoot_stance = True
            fire_shoot = True
        elif handSignTracker.compareHandSign(handsigns) == 2: #chidori
            chidori_stance = True
        else: 
            handsigns.clear()          #the user performs wrong handsigns, so clear handsigns list
                
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$keyboard detection$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        #keys free
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                idle = True
                up_move = False
            if event.key == pygame.K_s:
                idle = True
                down_move = False
            if event.key == pygame.K_a:
                left_move = False
            if event.key == pygame.K_d:
                right_move = False
            
        #keys pushed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                idle = False
                up_move = True
            if event.key == pygame.K_s:
                idle = False
                down_move = True
            if event.key == pygame.K_a:
                left_move = True
                facing_right = False
            if event.key == pygame.K_d:
                right_move = True
                facing_right = True
            if event.key == pygame.K_e:
                basic_attack = True
            if event.key == pygame.K_c:    #press c to start recording handsigns. Press again to cancel
                if jutsu_perform == True:
                    jutsu_perform = False
                    handsigns.clear()
                else: 
                    jutsu_perform = True
                    
    #$$$$$$$$$$$$$$$$$$$$$$$explosion and sprite collision controls$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    explode_sprite_group.draw(screen)
    explode_sprite_group.update()
        
    if pygame.sprite.spritecollide(zetsu_1,sasuke.getFireSprite(),False):
        explode_sprite_group.add(explosion(sasuke.getFireX()+50,sasuke.getFireY(),1))
        zetsu_1.enemyTakeFireDamage()
        sasuke.explicitFireKill()   #after explosion, kill the fire sprite explicitly
        
    if pygame.sprite.collide_rect_ratio(1.2)(sasuke, zetsu_1):
        if basic_attack:
            zetsu_1.enemyTakeSwingDamage()
        else: 
            sasuke.takeSwingDamge()       
            
    #$$$$$$$$$$$$$$$$$$$$$$$$Enemies states and controls$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    if zetsu_1.getHealth() > 0:
        zetsu_1.animate_updater()
        zetsu_1.move_towards_player(sasuke,enemySpeed)
        zetsu_1.draw_character()
    else:
        zetsu_1.kill()
         
    minion_1.movements(pygame.time.get_ticks())
    minion_1.animate_updater()
    minion_1.draw_character()
    minion_1.water_sprite_update()
    #$$$$$$$$$$$$$$$$$$$$$$$$Map control$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    pygame.display.update()
print(handsigns)
pygame.quit()
sys.exit()

