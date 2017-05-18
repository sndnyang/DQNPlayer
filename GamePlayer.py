# coding: utf-8
import sys
import time
import cv2
import argparse

import numpy as np

from BrainDQN_mx import BrainDQN

from GrabReader import *

# preprocess raw image to 80*80 gray image
def preprocess(observation, w=80, h=80):
    observation = cv2.cvtColor(cv2.resize(observation, (w, h)), cv2.COLOR_BGR2GRAY)
    ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
    return np.reshape(observation,(w,h,1))

def play():

    args = parse_arguments()
    game = GrabReader(args)
    w = game.rangle[2] - game.rangle[0]
    h = game.rangle[3] - game.rangle[1]

    while w * h > 6400:
        w /= 2
        h /= 2
    w = 80
    h = 80

    # Step 1: init BrainDQN
    actions = game.player.actions
    if args.param: 
        try:
            brain = BrainDQN(actions, 'saved_networks/network-dqn_mx%04d.params'%
                    int(args.param))
        except ValueError:
            print "参数文件指定错误, " +\
                    "a wrong parameter to specify the param file"""
            sys.exit(1)
    else:
        brain = BrainDQN(actions)

    # Step 2: init Game
    action0 = np.zeros(actions)
    action0[0] = 1
    game.restart()
    ob, rew, ter = game.state(action0)

    ob = cv2.cvtColor(cv2.resize(ob, (w, h)), cv2.COLOR_BGR2GRAY)
    ret, ob = cv2.threshold(ob,1,255,cv2.THRESH_BINARY)
    brain.setInitState(ob)

    old = False
    while True:
        action = brain.getAction()
        if old:
            ob, rew, ter = game.state(action)
            ob = cv2.cvtColor(cv2.resize(ob, (w, h)), cv2.COLOR_BGR2GRAY)
            ret, ob = cv2.threshold(ob,1,255,cv2.THRESH_BINARY)
            brain.setInitState(ob)
            old = False
        else:
            print np.argmax(action),
            ob, rew, ter = game.state(action)
            print rew, ter,
            sys.stdout.flush()
            ob = preprocess(ob, w, h)
            brain.setPerception(ob, action, rew, ter)
            old = ter

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""a player autolearn and run games such as flappybird,
        mario etc.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(dest='file', nargs='?',
                        help='main file to run',
                        default=None)

    parser.add_argument('-a', '--action', dest='action',
            help="""控制键，control keys, 格式format: a,b,x,up,right""")
    parser.add_argument('-k', '--keybind', action="store_true", dest='method',
            help="""游戏操控方式，默认使用消息传递方式，模拟器运行需要该参数""")
    parser.add_argument('-g', '--game', dest='game',
            help="游戏名即游戏窗口显示的名字, game name, "
                "the text shown in the windows")
    parser.add_argument('-p', '--param', dest='param',
            help="""已保存参数文件序号,
            saved_networks/network-dqn_mx????.params""")
    return parser.parse_args()

if __name__ == "__main__":
    play()
