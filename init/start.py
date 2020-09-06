#!/usr/bin/env python3
import os
tf = open("./temp.txt", "w+")
tf.write("False")
tf = open("./temp.txt", "r")
isRestart = tf.read()
isFirstBoot = True
#            if it True            this False. It didn't enter. HOW??????
while (isRestart == "True") or isFirstBoot:
  #making    it   False means shutdown. Works - do not touch.
  os.system("redis-server --daemonize yes")
  os.system("python3 -m userbot")
  if isFirstBoot:
    isFirstBoot = False
  tf = open("./temp.txt", "r")
  isRestart = tf.read()




