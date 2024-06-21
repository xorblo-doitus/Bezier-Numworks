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

a_x = 0
a_y = 0
p_x = 0.33
p_y = 1
q_x = 123
q_y = 123
b_x = 1
b_y = 0.5

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
  return (a_x - 2*p_x + b_x)*t**2 + (2*p_x - 2*a_x)*t + a_x, (a_y - 2*p_y + b_y)*t**2 + (2*p_y - 2*a_y)*t + a_y


def s(t):
  return t, sin(2**(4*t))


def fractional_to_screen(x, y):
  return int(x*320), int(y*222)


def draw(f=quad, max_res=14, callback=false):
  for res in range(1, max_res):
    for i in range(1, 2**res, 2):
      if callback():
        return
      set_pixel(*fractional_to_screen(*f(i/2**res)), color(0, 0, 0))
  return True


def select_handle():
  global current_handle_i
  for key in handle_keys:
    if keydown(key):
      current_handle_i = handle_keys[key]


def move_handle():
  move_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))
  
  if move_y:
    mod = current_handle_i % 4
    if mod == 0:
      global a_y
      a_y += move_y*SPEED
    elif mod == 1:
      global p_y
      p_y += move_y*SPEED
    elif mod == 2:
      global q_y
      q_y += move_y*SPEED
    else:
      global b_y
      b_y += move_y*SPEED
  
  move_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))
  
  if move_x:
    mod = current_handle_i % 4
    if mod == 0:
      global a_x
      a_x += move_x*SPEED
    elif mod == 1:
      global p_x
      p_x += move_x*SPEED
    elif mod == 2:
      global q_x
      q_x += move_x*SPEED
    else:
      global b_x
      b_x += move_x*SPEED
  
  return move_x or move_y


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