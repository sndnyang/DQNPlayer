# coding: utf-8
import sys
import time
import cv2
import numpy as np
from BrainDQN_mx import BrainDQN

from GrabReader import *

label = "FlappyBird"

# preprocess raw image to 80*80 gray image
def preprocess(observation):
    observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
    return np.reshape(observation,(80,80,1))

def play():
    # Step 1: init BrainDQN
    actions = 2
    #brain = BrainDQN(actions, 'saved_networks/network-dqn_mx1200.params')
    brain = BrainDQN(actions)
    # Step 2: init Flappy Bird Game
    game = GrabReader(label)
    game.act()
    action0 = np.array([0, 1])
    ob, reward, terminal = game.state(action0)

    ob = cv2.cvtColor(cv2.resize(ob, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, ob = cv2.threshold(ob,1,255,cv2.THRESH_BINARY)
    brain.setInitState(ob)

    c = 0
    tc = 0
    t = []
    while True:
        c += 1
        if c > 10000:
            break
        action = brain.getAction()
        ob, rew, ter = game.state(action)
        sys.stdout.flush()
        ob = preprocess(ob)
        brain.setPerception(ob, action, rew, ter)
        

if __name__ == "__main__":
    play()
