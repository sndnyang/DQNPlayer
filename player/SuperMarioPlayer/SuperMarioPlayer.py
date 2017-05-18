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

class SMPlayer:

    def __init__(self):
        # self.template = cv2.imread('bird.png', 0)
        # 动作[1,0,0,0,0]
        self.actions = 3
        # 有限状态自动机 [方向， 跳跃]
        # 0  1  2  0    1    2
        # 右 停 左 不跳 小跳 大跳
        # 小跳只是短暂情况，不会更新 self.fsm， 大跳的下一帧恢复不跳
        self.fsm = [0, 0]
        self.hld = None

    def start_game(self, hld):
        self.hld = hld
       #win32api.PostMessage(hld, win32con.WM_KEYDOWN, 65, 0)
       #time.sleep(0.03)
        win32api.PostMessage(hld, win32con.WM_KEYUP, 65, 0)
        self.fsm = [0, 0]
        win32api.PostMessage(hld, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)

    def act(self, hld, actions):
        """
        动作[1,0,0,0,0]
        0  1  2  3    4
        右 停 左 小跳 大跳
        """
        if self.fsm[1] == 2:
            self.fsm[1] = 0
            win32api.PostMessage(hld, win32con.WM_KEYUP, 65, 0)

        if actions[1] == 1:
           #if self.fsm[0] == 2:
           #    win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.win32con.VK_LEFT, 0)

            if self.fsm[0] != 0:
                win32api.PostMessage(hld, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
            self.fsm[0] = 0

       #elif actions[2] == 1:
       #    if self.fsm == 0:
       #        win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
       #    if self.fsm[0] != 2:
       #        win32api.PostMessage(hld, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
       #    self.fsm[0] = 2
        elif actions[0] == 1:
            self.fsm[0] = 1
            win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
            win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
       #elif actions[2] == 1:
       #    win32api.PostMessage(hld, win32con.WM_KEYDOWN, 65, 0)
       #    win32api.PostMessage(hld, win32con.WM_KEYUP, 65, 0)
        elif actions[2] == 1:
            self.fsm[1] = 2
            win32api.PostMessage(hld, win32con.WM_KEYDOWN, 65, 0)

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
            self.fsm = [0, 0]
            hld = self.hld
            win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
            win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.VK_LEFT, 0)

        return reward, terminal

    def restart(self, hld):
        win32api.PostMessage(hld, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
        time.sleep(0.02)
        win32api.PostMessage(hld, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
        time.sleep(0.05)
        self.start_game(hld)

