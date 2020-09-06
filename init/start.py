#!/usr/bin/env python3
import os
tf = open("./temp.txt", "w+")
tf.write("False")
tf = open("./temp.txt", "r")
isRestart = tf.read()
isFirstBoot = True
while isRestart == "True" or isFirstBoot:
  if isFirstBoot:
    isFirstBoot = False
  tf = open("./temp.txt", "r")
  isRestart = tf.read()

  if isRestart == "True":
    open("./temp.txt", "w").close()
    tf = open("./temp.txt", "w+")
    tf.write("False")

  os.system("redis-server --daemonize yes")
  os.system("python3 -m userbot")
