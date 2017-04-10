# coding: utf-8
import math
import time
import numpy as np
import win32api
import win32con
from PIL import ImageGrab

class FlappyBirdPlayer:

    def __init__(self):
        self.live_time = time.time()

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
            time.sleep(0.05)
            a = b
            b = ImageGrab.grab(rangle)

    def checkTerminal(self, old, new):
        now = time.time()
        lasting = now - self.live_time
        #reward = 0.2 /(1+math.exp(-lasting))
        reward = 0.1
        terminal = np.array_equal(old, new)
        if not terminal:
            c = np.count_nonzero(np.asarray(old) - np.asarray(new))
            print c,
            if c < 34 * 24 * 3 * 2:
                terminal = True
        if terminal:
            reward = -1
        if not terminal and lasting > 1.2:
            reward = 1
            self.live_time = now

        return reward, terminal
