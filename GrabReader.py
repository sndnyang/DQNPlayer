# coding: utf-8
import sys
import time
import random
import numpy as np
import ctypes
import win32gui
import win32api
import win32con
from PIL import ImageGrab, Image

from player import *

class RECT(ctypes.Structure): 
    _fields_ = [('left', ctypes.c_long), 
            ('top', ctypes.c_long), 
            ('right', ctypes.c_long), 
            ('bottom', ctypes.c_long)] 
    def __str__(self): 
        return str((self.left, self.top, self.right, self.bottom)) 

c = 0

class GrabReader:

    def __init__(self, args): 
        self.label = args.game

        hld = win32gui.FindWindow(None, self.label)

        win32gui.ShowWindow(hld, win32con.SW_RESTORE)  # 强行显示界面后才好截图
      # win32gui.SetForegroundWindow(hld)  # 将窗口提到最前

        # 取当前窗口坐标  
        rect = RECT() 
        ctypes.windll.user32.GetWindowRect(hld,ctypes.byref(rect)) 
        self.hld = hld

        # 调整坐标
        self.rangle = (rect.left+3,rect.top+32,rect.right-3,rect.bottom-20) 
        self.first = None
        self.second = ImageGrab.grab(self.rangle)

        players = {'SuperMario': SuperMarioPlayer,
                'FlappyBird': FlappyBirdPlayer,
                'PacMan': PacManPlayer}
        if self.label not in players:
            print '游戏名不正确'
            sys.exit(1)

        self.player = players[self.label]()

    def state(self, action):
        # 抓图
        global c

        self.act(action)

        #time.sleep(0.03)
        self.first = self.second
        pic = ImageGrab.grab(self.rangle)
        self.second = pic

        reward, terminal = self.player.checkTerminal(np.asarray(self.first),
                np.asarray(self.second), action)

        if c < 100:
            t = np.abs(np.asarray(self.second, dtype="int16")-np.asarray(self.first, dtype="int16"))
            Image.fromarray(np.uint8(t)).save('images/'+self.label+'/subtract-' + str(c) + '.jpg')
            self.first.save('images/'+self.label+'/subtract-' + str(c) + '-1.jpg')
            self.second.save('images/'+self.label+'/subtract-' + str(c) + '-2.jpg')
        c+=1
        if terminal:
            # self.first.save(str(c) + '1.jpg')
            #self.second.save(str(c) + '.jpg')
            c += 1
            self.player.restart(self.hld)

        img = np.asarray(self.second)
        return img, reward, terminal

    def act(self, action):
        self.player.act(self.hld, action)

    def restart(self):
        self.player.restart(self.hld)

