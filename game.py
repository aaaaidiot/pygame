# -*- coding: utf-8 -*-
"""
使用画像

絶対オト幻 より
boss.png 
https://zeotogen.blog.fc2.com/blog-category-8.html#entry68

ＩＫＡＣＨＩ　より
ziki.png,teki.png　
http://www.ikachi.org/index.html

使用BGM・SE
NASHより  
NSE-S421-012 タッチ音 Simple (39)
NSE-660-078  Warning (2)
NSE-S391-134 ファンファーレ/レベルアップ (7)
NSR-514-18   Get Away From Your Anxiety 

効果音ラボ　https://soundeffect-lab.info/sound/battle/battle2.html　より
戦闘【2】
爆発2
爆発3 
"""
import pygame
from pygame.locals import *
import time
import math
import random

class App():
    w, h = 400, 400
    def __init__(self):
        self.fps, self.v, self.f, self.bf, self.gover,self.bossf = 30, 5, True ,True, True, True
        self.mv, self.mv2, self.mv3, self.mv4 =15, 5 ,8, 5
        self.count, self.min =10 ,0
        self.p = Player()
        self.score, self.life, self.cou =0 ,5, 0 #スコア,ライフ,ボスカウント
        self.c, self.e, self.eba,  self.bosses, self.bossh, self.cure  = [], [], [], [] ,[], []#弾、敵、敵の弾,ボスの配置、当たり判定
        self.boss=Boss(110,50)
        self.bosses =[self.boss]
        self.bossh =[self.boss.r]
        self.bosshp =0
        pygame.init()
        self.screen = pygame.display.set_mode((App.w, App.h))
        pygame.display.set_caption('課題')
        self.clock = pygame.time.Clock()
        self.soundflg = False
        self.font = pygame.font.SysFont("yumincho", 15)
        self.sound =pygame.mixer.Sound("NSE-S421-012.wav") #ライフ回復
        self.sound2 =pygame.mixer.Sound("爆発1.mp3") #敵撃破
        self.sound3 =pygame.mixer.Sound("NSE-660-078.wav") #ボス登場
        self.sound4 =pygame.mixer.Sound("爆発2.mp3") #被弾
        self.sound5 =pygame.mixer.Sound("NSE-S391-134.wav") #ボス撃破
        #pygame.mixer.init()
        #pygame.mixer.music.load("NSR-514-18.wav") #BGM
        #pygame.mixer.music.play(loops=-1)
        self.main()
    def main(self):
        while self.f:
            if self.gover:
                self.up()
                self.draw()
            self.ev()
    def up(self):
        if self.soundflg:
            self.sound3.play()
            self.soundflg = False
        if (self.cou>=20 and self.bossf):
            self.bf =False
            self.soundflg = True
            self.cou =0
            
        elif (self.cou>= 50):
            self.bf =False
            self.soundflg = True
            self.cou =0
        if(random.randint(0, 1000) > 997):
            self.cu =Cure(random.randrange(0, 350),0)
            self.cure.append(self.cu.r)
        for i,item in enumerate(self.cure):
            if(item.colliderect(self.p.r)):
                self.sound.play()
                self.life +=1
                self.cure.pop(i)
        if self.bf:
            self.min +=1
            if(self.min>self.count):
                self.ene = Enemy(random.randrange(0, 350),0)
                self.e.append(self.ene.r)
                self.eneb = Eneb(self.ene.r.x+38,self.ene.r.y+20)
                self.eba.append(self.eneb.r)
                self.min=0
            for i,item in enumerate(self.e):
                self.hit = item.collidelist(self.c)
                if  self.hit > -1:      #当たり判定（敵とプレイヤーの弾）
                    self.sound2.play()
                    self.score += 1     #当たった場合はスコア＋１
                    self.cou +=1
                    self.c.pop(self.hit)    #弾の削除
                    self.e.pop(i)    #敵の削除
                if(item.colliderect(self.p.r)):
                    self.life -=1
                    self.sound4.play()
                    self.e.pop(i)
            for i,item in enumerate(self.eba):
                if(item.colliderect(self.p.r)):
                    self.life -=1
                    self.sound4.play()
                    self.eba.pop(i)
        else:
            for item in self.bosses:
                if(self.bossf):
                    if(random.randint(0, 100) > 50):item.shoot(self.p)
                else:
                    if(random.randint(0, 100) > 45):item.shoot(self.p)
            for i,item in enumerate(self.bossh):
                if(item.colliderect(self.p.r)):
                    self.life -=1
                    self.sound4.play()
                self.hit =item.collidelist(self.c)
                if  self.hit > -1:
                    self.c.pop(self.hit)
                    self.bosshp +=1
                    if self.bossf :
                        if not self.bosshp >= 25:
                            self.sound2.play()
                        else :
                            self.sound5.play()
                            self.bosshp =0
                            self.score +=100
                            self.bossf = False
                            self.bf = True     
                    else:
                        if not self.bosshp >= 50:
                            self.sound2.play()
                        else :
                            self.sound5.play()
                            self.bosshp =0
                            self.score +=100
                            self.bf = True     
            for i, item in enumerate(Boss.b):
                item.move()
                if(item.r.colliderect(self.p.r)):
                   self.life -=1
                   self.sound4.play()
                   Boss.b.pop(i)
                if(not(0 < item.r.x < App.w)): Boss.b.pop(i)
                elif(not(0 < item.r.y < App.h)): Boss.b.pop(i)
            
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.p.img, self.p.r)
        for i,item in enumerate(self.c): 
            item.move_ip(0, -self.mv) 
            pygame.draw.circle(self.screen, (0, 255, 0), (item.x, item.y), item.w/2)
            if item.y < 0: 
                self.c.pop(i) 
        self.img2 =pygame.image.load("kaihuku.png")
        for i,item in enumerate(self.cure):
            item.move_ip(0,self.mv4)
            r2=Rect(item) 
            self.screen.blit(self.img2, r2)
            if item.y < 0: 
                self.cure.pop(i)
        if self.bf:
            self.img = pygame.image.load("teki.png")
            for i,item in enumerate(self.e):
                item.move_ip(0,self.mv2)
                r2=Rect(item) 
                self.screen.blit(self.img, r2)
                if item.y > self.h: 
                    self.e.pop(i)
            for i,item in enumerate(self.eba):
                item.move_ip(0,self.mv3)
                pygame.draw.circle(self.screen, (255, 0, 0), (item.x, item.y), item.w/2)
                if item.y < 0:
                    self.eba.pop(i)
        else:
            for item in self.bosses:
                self.screen.blit(item.img, item.r)
            for item in Boss.b:
                pygame.draw.circle(self.screen, (255, 0, 0), (item.r.x, item.r.y), 8)
        txt2 =""
        for i in range(self.life): txt2 += "●"
        txt = "スコア：" + str(self.score)+ "　            ライフ:" + txt2
        self.txt = self.font.render(txt, True, (255, 255, 255))
        self.screen.blit(self.txt, (0, 0))
        if(self.life <= 0):	
            self.txt = self.font.render("GAME OVER", True, (255, 255, 255))
            self.txt2 = self.font.render("スコア:"+str(self.score),True, (255, 255, 255))
            self.screen.blit(self.txt, (150, 185))
            self.screen.blit(self.txt2, (150, 200))
            self.gover= False
        pygame.display.update()
        self.clock.tick(self.fps)
    def ev(self):
        for event in pygame.event.get():
            if (event.type == MOUSEMOTION): #マウスが移動した場合
                x,y = event.pos
                self.p.move((x - self.p.r.x), (y - self.p.r.y))
            if event.type == MOUSEBUTTONDOWN and event.button == 1: #マウスをクリックした場合
                cx,cy = event.pos #クリック時のマウス座標を取得
                self.c.append(Rect(cx, cy, 10, 10)) 
            if(event.type == QUIT):
                self.f = False
            if(event.type == KEYDOWN and event.key == K_ESCAPE):
                self.f = False

class Player():
    def __init__(self):
        w, h = 20, 20
        self.r = Rect(150, 150, w, h)
        self.img = pygame.image.load("ziki.png")
    def move(self, x, y):
        self.r.move_ip(x, y)
class Enemy():
    def __init__(self, x, y):
        self.r = Rect(x, y, 70, 45)
    def move(self, x, y):
        self.r.move_ip(x, y)
class Eneb():
    def __init__(self, x, y):
        self.r = Rect(x, y, 10, 10)
    def move(self, x, y):
        self.r.move_ip(x, y)
class Cure():
    def __init__(self, x, y):
        self.r = Rect(x, y, 32, 32)
    def move(self, x, y):
        self.r.move_ip(x, y)
class Boss():
    b = []
    def __init__(self, x, y):
        self.r = Rect(x, y, 150, 120)
        self.img = pygame.image.load("boss.png")
    def shoot(self, p):
        Boss.b.append(Bullet(self.r.x+75, self.r.y+73, p))
class Bullet():
    def __init__(self, x, y, p):
        self.r = Rect(x, y, 5, 5)
        v = 6
        y = p.r.y - y
        x = p.r.x - x
        angle = int(math.degrees(math.atan2(y, x))) + random.randint(-10, 20)
        self.vx = v*math.cos(math.radians(angle))
        self.vy = v*math.sin(math.radians(angle))
    def move(self):
        self.r.move_ip(self.vx, self.vy) 
class Cure():
    def __init__(self, x, y):
        self.r = Rect(x, y, 32, 32)
    def move(self, x, y):
        self.r.move_ip(x, y)
if __name__ == '__main__': App()
