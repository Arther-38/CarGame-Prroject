# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:16:11 2023

@author: chenh
"""
import pygame
import random
# Color

red = (200,0,0)
green = (76,208,56)
blue = (0,0,255)
grey = (100,100,100)
black = (0,0,0)
white = (255,255,255)
yellow = (255,232,0)


class Screen:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.screen_size = (width , height)
        self.screen = pygame.display.set_mode(screen_size)
        
    def fill_color(self,color):
        self.screen.fill(color)


    def blit(self , obj1 , obj2):
        self.screen.blit(obj1 , obj2)


class Road:

    def __init__(self , height):
        self.marker_width = 10
        self.marker_height = 50
        self.left_lane = 205
        self.center_lane = 500
        self.right_lane = 695
        self.lanes = [self.left_lane , self.center_lane , self.right_lane]
        self.center_lanes = [ (self.left_lane + self.left_lane+155 ) / 2 , (self.left_lane+155 + self.center_lane+35) / 2 , (self.right_lane + self.center_lane+35 ) / 2]
        self.lane_marker_move_y = 0
        self.left_edge_marker = (195,0,self.marker_width,height)
        self.right_edge_marker = (695,0,self.marker_width,height)
        self.road=(200,0,500,height)
        
    def draw(self, screen):
        pygame.draw.rect(screen,grey,self.road)
        pygame.draw.rect(screen,yellow,self.left_edge_marker)
        pygame.draw.rect(screen,yellow,self.right_edge_marker)
        
        for y in range(self.marker_height*-2 , height ,  self.marker_height*2):
            pygame.draw.rect(screen , white , (self.left_lane+155 , y+self.lane_marker_move_y , self.marker_width , self.marker_height))     
            pygame.draw.rect(screen , white , (self.center_lane+35 , y+self.lane_marker_move_y , self.marker_width , self.marker_height))   

    def move(self , speed , action):
        if action==True:
            self.lane_marker_move_y += speed
            
            if self.lane_marker_move_y >= self.marker_height*2:
                self.lane_marker_move_y=0
                
            if self.lane_marker_move_y <= -self.marker_height*2:
                self.lane_marker_move_y = 0
        

class opposite_Car(pygame.sprite.Sprite): #對向來車
    
    def __init__(self,image,x,y,colors):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y= y
        self.color = colors
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        #self.image.set_colorkey((0, 0, 255))
        self.image.fill(colors)
        self.Iscollide = False
        
    def display(self,screen):
        new_image = pygame.transform.rotate(self.image, 0)
        new_rect = new_image.get_rect(center=self.image.get_rect(topleft=(self.x,self.y)).center)
        screen.blit(new_image , new_rect.topleft)
        self.rect = new_rect
        
    def forward(self):
        self.y += 2
        self.rect.y += 2


import math

class Vehicle(pygame.sprite.Sprite):
    def __init__(self,image,x,y,color,angle):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y= y
        self.image = image
        self.image.set_colorkey((255, 255, 255))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.angle = angle
        self.speed = 2
        self.max_speed = 8
        self.min_speed = 0
        self.rotation_speed = 0.5
        self.radars = []
        self.intersect = True
        
    def display(self,screen):
        new_image = pygame.transform.rotate(self.image, self.angle)
        #new_rect = new_image.get_rect(center=self.image.get_rect(topleft=(self.x,self.y)).center)
        self.rect = new_image.get_rect(center=self.image.get_rect(topleft=(self.x,self.y)).center)
        screen.blit(new_image , self.rect.topleft)
        #screen.blit(new_image , new_rect.topleft)
        #self.rect = new_rect

    def cast_sensor(self,sensor,vehicle_group):
        BLUE = pygame.Color('dodgerblue1')
        for angle in range(-80, 80, 20):
            sensor.draw_line(self.image.get_rect().center, angle, 120, 2, BLUE, screen,vehicle_group)

    def rotate_left(self):
        self.angle += self.rotation_speed
    
    def rotate_right(self):

        self.angle -= self.rotation_speed
    
    def forward(self): # var : variation of car's y axis
    
        if self.speed < self.max_speed: 
            self.speed +=0.01
            
        radians = math.radians(self.angle)
        #vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed
        
        self.x -= horizontal
        #self.y -= vertical
    
    def retard(self):
        if self.speed > self.min_speed: 
            self.speed -=0.1

        radians = math.radians(self.angle)
        #vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed
        
        #self.x += horizontal
        #self.y += vertical
    
    def player_pressKey(self):
        
        move_road = True
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            print('left!')
            self.rotate_left()
            move_road = True
            #return move_road
            
        if keys[pygame.K_d]:
            print('right!')
            self.rotate_right()
            move_road = True
            #return move_road
            
        if keys[pygame.K_w]:
            print('forward!')
            self.forward()
            move_road = True
            #return move_road
            
        if keys[pygame.K_s]:
            print('retard!')
            self.retard()
            move_road = True
            #return move_road
            
        return move_road
    
    def agent_pressKey(self):
        choicelist = ['left' , 'right' , 'forward' ]
        choice = random.choice(choicelist)
        move_road = True
        
        if choice == 'left':
            print('left!')
            self.rotate_left()
            move_road = True
            #return move_road
            
        if choice == 'right':
            print('right!')
            self.rotate_right()
            move_road = True
            #return move_road
            
        if choice == 'forward':
            print('forward!')
            self.forward()
            move_road = True
            #return move_road
        '''
        if choice == 'retard':
            print('retard!')
            self.retard()
            move_road = True
            #return move_road
        '''
        return move_road
            
        
    
    def draw_line(self , position, angle, line_length, line_width, color, screen ,right_lane, left_lane ,vehicle):
        radars = []
        len = 0
        x = int(position[0] + math.cos(math.radians(360 - (angle ))) * len)
        y = int(position[1] + math.sin(math.radians(360 - (angle ))) * len)
        
        collide = False

        while not ((x > right_lane) or ( x < left_lane) or (vehicle.rect.collidepoint((x,y))) ) and len < line_length and collide == False:
                                
            len = len + 1
            x = int(self.rect.center[0] + math.cos(math.radians(360 - (angle))) * len)
            y = int(self.rect.center[1] + math.sin(math.radians(360 - (angle))) * len)
            pygame.draw.line(screen, color, position, (x,y) , line_width)
            
            if vehicle.rect.collidepoint((x,y)):
                collide = True
                print('collide!!! len = ' , len)
                break
        
        len2 = 125-len
        x2 = int(x + math.cos(math.radians(360 - (angle))) * len2 )
        y2 = int(y + math.sin(math.radians(360 - (angle))) * len2 )
        
        if (x > right_lane) or ( x < left_lane) :
            collide = True
            print('collide wall !!!')
        
        if collide == True:
            print('draw line !!!!!!!! ',(x,y), (x2,y2))
            pygame.draw.line(screen, (255,0,0), (x,y), (x2,y2) , line_width)
        
        dist = int(math.sqrt(math.pow(x - position[0], 2) + math.pow(y - position[1], 2)))
        radars=((x, y), dist)
        return radars


import random
radars_list = []

if __name__ == "__main__" :
    # initial pygame
    pygame.init()
    
    running = True
    done =False
    FPS = 120
    width = 900
    height = 750
    player_x = 430
    player_y = 300
    screen_size = (width , height)
    clock = pygame.time.Clock()
    screen = Screen(width,height)
    road = Road(height)
    car_size = (60,80)
    car_body = pygame.Surface(car_size)
    car = Vehicle(car_body ,player_x , player_y , red , 0)
    player_group = pygame.sprite.Group()
    player_group.add(car)
    enemy_group = pygame.sprite.Group()
    
    enemy_colors = [[200,100,100] , [0,255,0] , [0,0,255] , [50,150,30]] 
    
    score = 0
    kill = 0
    finish = False
    
    while running :
        Iscollide = False
        
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        screen.fill_color(green)
        
        if not finish:
            #car.player_pressKey()
            #move_road = car.player_pressKey()
            car.agent_pressKey()
            move_road = car.agent_pressKey()
        
        road.draw(screen.screen)
        
        #car.cast_sensor(sensor)
        car.display(screen)
        speed = car.speed
        road.move(speed, move_road)
        #control_group(enemy_group , enemy_colors , road.center_lanes , score , screen.height)

        print('MyCar position : ' , car.x , car.y)

        print('----------------------  ' , car.rect.top)
        print('MyCar.rect.top = ', car.rect.top)

        if len(enemy_group) < 2 :
            
            add_vehicle = True
            for enemy in enemy_group:
                if enemy.rect.top < enemy.rect.height*1.5 :
                    print('top = ' , enemy.rect.top , 'height = ' , enemy.rect.height)
                    add_vehicle = False
                    
            print('len vehicle = ' , len(enemy_group))        
            
            if add_vehicle:
                
                c_lane = random.choice(road.center_lanes)
                print('c_lane = ----------------------------------- ' , c_lane)
                image = pygame.Surface([60,80])
                color = random.choice(enemy_colors)
                vehicle = opposite_Car(image , c_lane , screen.height/-4 , color ) # height/-2
                
                enemy_group.add(vehicle)
                print('ADD vehicle !!!--------------------------------------------------')
        
        #enemy_group.draw(screen.screen)
        
        for vehicle in enemy_group :
            #vehicle.rect.y += 2
            if finish == False:
                vehicle.forward()
            #print('vehicle position : ' , vehicle.x , vehicle.y)
            vehicle.display(screen)
            #print('----------------------  ' , vehicle.rect.top)
            #print('vehicle.rect.top = ', vehicle.rect.top)
            radar = []
            BLUE = pygame.Color('dodgerblue1')
            for angle in range(15, 160, 15):
                length = car.draw_line(car.rect.center, (angle + car.angle), 120, 2, BLUE, screen.screen,road.right_lane,road.left_lane,vehicle)
                radar.append(length)
                
            if vehicle.rect.top > screen.height: #>= height
                print('----------------------- ' ,vehicle.rect.top , ' kill*-------------------------------------')
                kill += 1
                vehicle.kill()
                
                score += 1
                
                if score>0 and score % 5 == 0 :
                    #speed += 1
                    pass
            
            if pygame.Rect.colliderect(car.rect, vehicle.rect) or (car.rect.topleft[0] <= road.left_lane) or (car.rect.topright[0] >= road.right_lane) :
                if pygame.Rect.colliderect(car.rect, vehicle.rect):
                    print('vehicle.rect.top = ', vehicle.rect.top)
                    print('car.rect.top = ', car.rect.top)
                    print('colllllllllllllllllllllllide!')
                vehicle.Iscollide = True

            if vehicle.Iscollide == True :
                car.image.fill([0,255,0])
                vehicle.image.fill([255,0,0])
                finish = True
            else:
                car.image.fill([255,0,0])
            
            car.radars.append(radar)
            
            if finish :
                car.speed = 0
                vehicle.speed = 0
            
        print('score = ',  score)        
        print('current speed = ' , car.speed)
        pygame.display.update()
    
    radars_list = car.radars
    print('kill')
    pygame.quit()

#%%
print(radars_list[1])

#%%
import numpy as np
import gym
from gym import spaces

class CarGameEnv(gym.Env):
    
    def __init__(self,env_config=None):
        self.action_space = spaces.Discrete(4) 
        self.observation_space = spaces.Box(low = 0 , high = 120 , shape=(8,) , dtype = np.float32)
        
        self.angle = 0
        self.velX = 0
        self.velY = 0

    def step(self,action=np.zeros((2),dtype=np.float)):
        pass
    
    def render(self):
        pass
    
    def reset(self):
        observation = 0
        return observation
    
    def close(self):
        pass

    
#%%

environment = CarGameEnv()
environment.init_render()
run = True






















