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


class FlappyBirdPlayer:

    def __init__(self):
        self.actions = 2
        self.template = cv2.imread('bird.png', 0)

    def act(self, hld, action):
        if action[1] == 1:
            win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
            win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_UP, 0)

    def wait_restart(self, a, b, rangle):
        now = time.time()
        while True:
            if np.array_equal(a, b):
                self.live_time = now
                return
            time.sleep(0.01)
            a = b
            b = ImageGrab.grab(rangle)

    def findBirdY(self, img):
        res = cv2.matchTemplate(img , self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_loc, max_val
    
    def isCrash(self, img, x, y):

        if img[x][y-1] > 10:
            return True
        if img[x+24][y-1] > 10:
            return True
        if img[x+23][y+34] > 10:
            return True
        if img[x+24][y+33] > 10:
            return True
        if img[x+23][y] > 10:
            return True
        if img[x-1][y] > 10:
            return True
        if img[x-1][y+34] > 10:
            return True
        if img[x][y+34] > 10:
            return True
        return False

    def checkTerminal(self, img1, img2, action):
        img = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) 
        #reward = 0.2 /(1+math.exp(-lasting))
        reward = 0.1
        loc, val = self.findBirdY(img)
        terminal = False
        x, y = loc
        if self.isCrash(img, y, x):
            terminal = True

        pipe_y = 1
        if y < 2:
            pipe_y = 35

        w = len(img[0])
        for i in range(10, w-10):
            if img[pipe_y][i-1] < 10 and img[pipe_y][i] > 10\
                    and i < x + 22 and i > x + 17:
                reward = 1

        if val < 0.5 or terminal:            
            reward = -1

        return reward, terminal

    def restart(self, hld):
        win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
        win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
