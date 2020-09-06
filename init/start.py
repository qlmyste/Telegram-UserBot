#!/usr/bin/env python3
import os
tf = open("./temp.txt", "w+")
tf.write("False")
tf = open("./temp.txt", "r")
isRestart = tf.read()
isFirstBoot = True
while isRestart is "True" or isFirstBoot:
  print("first boot or restarted")
  if isFirstBoot:
    print("first boot")
    isFirstBoot = False
  tf = open("./temp.txt", "r")
  isRestart = tf.read()

  if isRestart is "True":
    print("restarted")
    open("./temp.txt", "w").close()
    tf = open("./temp.txt", "w+")
    tf.write("False")

  os.system("redis-server --daemonize yes")
  os.system("python3 -m userbot")
