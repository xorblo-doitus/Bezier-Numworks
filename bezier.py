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
COLOR = color(0, 0, 0)
BG_COLOR = color(255, 255, 255)
HANDLE_COLOR = color(100, 100, 100)
HANDLE_COLOR_SEC = color(0, 200, 0)
HANDLE_SIZE = 4

a_x = 0
a_y = 0
p_x = 0.33
p_y = 1
q_x = 0.66
q_y = 0
b_x = 1
b_y = 0.5

clear_on_editing = False
current_handle_i = 0
handle_keys = {
  KEY_ONE: 0,
  KEY_TWO: 1,
  KEY_FIVE: 2,
  KEY_THREE: 3,
}
handle_strings = ["a", "p", "q", "b"]


def false():
  return False


def clear_screen():
  fill_rect(0, 0, 320, 222, BG_COLOR)
  draw_handles()
  draw_current_handle()


def quad(t):
  return (a_x - 2*p_x + b_x)*t**2 + (2*p_x - 2*a_x)*t + a_x, (a_y - 2*p_y + b_y)*t**2 + (2*p_y - 2*a_y)*t + a_y, COLOR


def cubic(t):
  return (-a_x + 3*p_x - 3*q_x + b_x)*t**3 + (3*a_x - 6*p_x + 3*q_x)*t**2 + (3*p_x - 3*a_x)*t + a_x, (-a_y + 3*p_y - 3*q_y + b_y)*t**3 + (3*a_y - 6*p_y + 3*q_y)*t**2 + (3*p_y - 3*a_y)*t + a_y, COLOR


def cubic_rainbow(t):
  return (-a_x + 3*p_x - 3*q_x + b_x)*t**3 + (3*a_x - 6*p_x + 3*q_x)*t**2 + (3*p_x - 3*a_x)*t + a_x, (-a_y + 3*p_y - 3*q_y + b_y)*t**3 + (3*a_y - 6*p_y + 3*q_y)*t**2 + (3*p_y - 3*a_y)*t + a_y, color(int(200*t), int(200*(1-t)), int(sin(t*5)*200))


def s(t):
  return t, sin(2**(4*t)), COLOR


def fractional_to_screen(x, y, c):
  return int(x*320), int(y*222), c


def draw(f=quad, max_res=14, callback=false):
  for res in range(1, max_res):
    for i in range(1, 2**res, 2):
      if callback():
        return
      set_pixel(*fractional_to_screen(*f(i/2**res)))
      
  return True


def draw_handle(x, y, c=HANDLE_COLOR):
  x=x*320
  y=y*222
  fill_rect(int(x-HANDLE_SIZE), int(y), int(2*HANDLE_SIZE), 1, c)
  fill_rect(int(x), int(y-HANDLE_SIZE), 1, int(2*HANDLE_SIZE), c)


def draw_handles():
  draw_handle(a_x, a_y)
  draw_handle(p_x, p_y, HANDLE_COLOR_SEC)
  draw_handle(q_x, q_y, HANDLE_COLOR_SEC)
  draw_handle(b_x, b_y)


def draw_current_handle():
  draw_string(handle_strings[current_handle_i], 0, 0, COLOR, BG_COLOR)


def select_handle():
  global current_handle_i
  for key in handle_keys:
    if keydown(key):
      current_handle_i = handle_keys[key]
      draw_current_handle()
      return


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
  
  global clear_on_editing
  if keydown(KEY_ANS):
    clear_on_editing = False
  elif keydown(KEY_EXE):
    clear_on_editing = True
  
  if EMULATED and (keydown(KEY_BACK) or keydown(KEY_HOME) or keydown(KEY_OK)):
    exit()
  
  if move_handle():
    if current_handle_i == 1 or current_handle_i == 2:
      draw_handles()
    return True


def bezier(f=cubic):
  while True:
    clear_screen()
    if draw(f=f, max_res=10, callback=update_handle):
      while not update_handle():
        sleep(TPF)
    
    while update_handle():
      if clear_on_editing:
        clear_screen()
      draw(f=f, max_res=6, callback=false)


if EMULATED and __name__ == "__main__":
  bezier()