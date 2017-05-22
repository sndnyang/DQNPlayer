# coding: utf-8
import sys
sys.path.append("game/")

import math
import time
import cv2
import numpy as np
import win32api
import win32con
from PIL import ImageGrab

class PacManPlayer:

    def __init__(self):
        # self.template = cv2.imread('bird.png', 0)
        # 动作[1,0,0,0,0]
        self.actions = 4
        # 有限状态自动机 [0, 0, 0, 0]
        # 0  1  2  3   
        # 上 下 左 右
        self.hld = None

    def start_game(self, hld):
        self.hld = hld

    def act(self, hld, actions):
        """
        动作[1,0,0,0]
        0  1  2  3    
        上 下 左 右 
        """
        if actions[2] == 1:
            win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
            win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_UP, 0)

        elif actions[3] == 1:
            win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
            win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
        elif actions[0] == 1:
            win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
            win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
        elif actions[1] == 1:
            win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_RIGHT65, 0)
            win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)

    def wait_restart(self, a, b, rangle):
        now = time.time()
        while True:
            if np.array_equal(a, b):
                self.live_time = now
                return
            time.sleep(0.01)
            a = b
            b = ImageGrab.grab(rangle)

    def checkTerminal(self, img1, img2, action):
        #reward = 0.2 /(1+math.exp(-lasting))
        reward = 0.1
        terminal = False
        if np.array_equal(img1, img2):
            terminal = True
            reward = -1
        return reward, terminal

    def restart(self, hld):
        win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

