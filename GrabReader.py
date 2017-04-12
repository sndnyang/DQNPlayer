# coding: utf-8
import random
import time
import numpy as np
import ctypes
import win32gui
import win32api
import win32con
from PIL import ImageGrab

from FlappyBirdPlayer import FlappyBirdPlayer as Player

class RECT(ctypes.Structure): 
    _fields_ = [('left', ctypes.c_long), 
            ('top', ctypes.c_long), 
            ('right', ctypes.c_long), 
            ('bottom', ctypes.c_long)] 
    def __str__(self): 
        return str((self.left, self.top, self.right, self.bottom)) 


c = 0

class GrabReader:

    def __init__(self, label): 
        self.label = label

        hld = win32gui.FindWindow(None, label)

        win32gui.ShowWindow(hld, win32con.SW_RESTORE)  # 强行显示界面后才好截图
        win32gui.SetForegroundWindow(hld)  # 将窗口提到最前
        time.sleep(1)

        # 取当前窗口坐标  
        rect = RECT() 
        ctypes.windll.user32.GetWindowRect(hld,ctypes.byref(rect)) 
        self.hld = hld

        # 调整坐标  
        self.rangle = (rect.left+3,rect.top+32,rect.right-3,rect.bottom-20) 
        self.first = None
        self.second = ImageGrab.grab(self.rangle)

        self.player = Player()

    def state(self, action):
        # 抓图
        global c

        self.act(action)

        self.first = self.second
        pic = ImageGrab.grab(self.rangle)

        reward, terminal = self.player.checkTerminal(np.asarray(pic),
                action[1])
        self.second = pic
        if terminal:
           #if action[1] == 1:
           #    self.first.save(str(c) + '-' + str(action[1]) + '-1.jpg')
           #    self.second.save(str(c) + '-' + str(action[1]) + '-2.jpg')
           #    c += 1
            self.player.restart(self.hld)
        img_data = np.asarray(self.second)

        return img_data, reward, terminal

    def act(self, action):
        self.player.act(self.hld, action)

