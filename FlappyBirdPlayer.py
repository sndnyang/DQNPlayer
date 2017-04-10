# coding: utf-8
import math
import time
import cv2
import numpy as np
import win32api
import win32con
from PIL import ImageGrab

class FlappyBirdPlayer:

    def __init__(self):
        self.live_time = time.time()
        self.template = cv2.imread('bird.png', 0)

    def act(self, hld):
        win32api.SendMessage(hld, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
        win32api.SendMessage(hld, win32con.WM_KEYUP, win32con.VK_UP, 0)
        time.sleep(0.02)

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
        res = cv2.matchTemplate(img , self.template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_loc
    
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

    def checkTerminal(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        now = time.time()
        lasting = now - self.live_time
        #reward = 0.2 /(1+math.exp(-lasting))
        reward = 0.1
        y, x= self.findBirdY(img)
        terminal = False
        if self.isCrash(img, x, y):
            terminal = True
            reward = -1
        if not terminal and lasting > 1.8:
            reward = 1
            self.live_time = now

        return reward, terminal
