from math import *
from ion import *
from kandinsky import *
from time import sleep

EMULATED = False
try: import os; EMULATED = True; print("Emulated")
except: pass

FPS = 60
TPF = 1/FPS
SPEED = 0.02

a = 0
p = 1
q = 123
b = 0.5

current_handle_i = 0
handle_keys = {
  KEY_ONE: 0,
  KEY_TWO: 1,
  KEY_FIVE: 2,
  KEY_THREE: 3,
}


def false():
  return False


def quad(t):
  return (a - 2*p + b)*t**2 + (2*p - 2*a)*t + a


def s(t):
  return sin(2**(4*t))


def draw(f=quad, max_res=14, callback=false):
  for res in range(1, max_res):
    for i in range(1, 2**res, 2):
      if callback():
        return
      set_pixel(int(320*i/2**res), int(f(i/2**res)*222), color(0, 0, 0))
  return True


def select_handle():
  global current_handle_i
  for key in handle_keys:
    if keydown(key):
      current_handle_i = handle_keys[key]


def move_handle():
  move = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))
  
  if move:
    mod = current_handle_i % 4
    if mod == 0:
      global a
      a += move*SPEED
    elif mod == 1:
      global p
      p += move*SPEED
    elif mod == 2:
      global q
      q += move*SPEED
    else:
      global b
      b += move*SPEED
  
  return move


def update_handle():
  select_handle()
  
  if EMULATED and (keydown(KEY_BACK) or keydown(KEY_HOME) or keydown(KEY_OK)):
    exit()
  
  return move_handle()


def bezier():
  while True:
    fill_rect(0, 0, 320, 222, color(255, 255, 255))
    if draw(f=quad, max_res=10, callback=update_handle):
      while not update_handle():
        sleep(TPF)
    
    while update_handle():
      draw(f=quad, max_res=6, callback=false)


if EMULATED and __name__ == "__main__":
  bezier()