from math import *
from ion import *
from kandinsky import *
from time import sleep

EMULATED = False
try: import os; EMULATED = True; print("Emulated")
except: pass


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 222
FPS = 60
TPF = 1/FPS
SPEED = 0.02
COLOR = color(0, 0, 0)
BG_COLOR = color(255, 255, 255)
HANDLE_COLOR = color(100, 100, 100)
SELECTED_HANDLE_COLOR = color(255, 100, 100)
HANDLE_COLOR_SEC = color(0, 200, 0)
SELECTED_HANDLE_COLOR_SEC = color(255, 200, 0)
DEFAULT_HANDLE_SIZE = 6


class Handle:
  handles: "list[Handle]" = []
  current_handle_i: int = 0
  
  
  @classmethod
  def set_current_handle(cls, i: int):
    cls.current_handle_i = i % max(1, len(cls.handles))
    cls.draw_handles()
  
  
  @classmethod
  def get_current_handle(cls) -> "Handle":
    return cls.handles[cls.current_handle_i]
  
  
  @classmethod
  def draw_handles(cls) -> "Handle":
    for i, handle in enumerate(cls.handles):
      if i == cls.current_handle_i:
        handle.draw_selected()
      else:
        handle.draw()
  
  
  @classmethod
  def ui_select_handle(cls):
    for i, handle in enumerate(cls.handles):
      if keydown(handle.keycode):
        cls.set_current_handle(i)
        return
  
  
  def __init__(self, x: float, y: float, name: str, keycode: int, color: "ColorOutput", selected_color: "ColorOutput", size: int = DEFAULT_HANDLE_SIZE) -> None:
    self.x = x
    self.y = y
    self.name = name
    self.keycode = keycode
    self.color = color
    self.selected_color = selected_color
    self.size = size
  
  
  def draw_name(self, x: int = 0, y: int = 0):
    draw_string(self.name, x, y, self.color, BG_COLOR)
  
  
  def draw(self, color=None):
    if color is None:
      color = self.color
      
    x = int(self.x * SCREEN_WIDTH)
    y = int(self.y * SCREEN_HEIGHT)
    
    fill_rect(x - self.size, y, self.size * 2, 1, color)
    fill_rect(x, y - self.size, 1, self.size * 2, color)
  
  
  def draw_selected(self):
    self.draw_name()
    self.draw(self.selected_color)


a = Handle(0, 0, "a", KEY_ONE, HANDLE_COLOR, SELECTED_HANDLE_COLOR)
p = Handle(0.33, 1, "p", KEY_TWO, HANDLE_COLOR_SEC, SELECTED_HANDLE_COLOR_SEC)
q = Handle(0.66, 0, "q", KEY_FIVE, HANDLE_COLOR_SEC, SELECTED_HANDLE_COLOR_SEC)
b = Handle(1, 0.5, "b", KEY_THREE, HANDLE_COLOR, SELECTED_HANDLE_COLOR)

Handle.handles = [
  a,
  p,
  q,
  b,
]

clear_on_editing = False


def false():
  return False


def clear_screen():
  fill_rect(0, 0, 320, 222, BG_COLOR)
  Handle.draw_handles()


def quad(t):
  return (a.x - 2*p.x + b.x)*t**2 + (2*p.x - 2*a.x)*t + a.x, (a.y - 2*p.y + b.y)*t**2 + (2*p.y - 2*a.y)*t + a.y, COLOR


def cubic(t):
  return (-a.x + 3*p.x - 3*q.x + b.x)*t**3 + (3*a.x - 6*p.x + 3*q.x)*t**2 + (3*p.x - 3*a.x)*t + a.x, (-a.y + 3*p.y - 3*q.y + b.y)*t**3 + (3*a.y - 6*p.y + 3*q.y)*t**2 + (3*p.y - 3*a.y)*t + a.y, COLOR


def cubic_rainbow(t):
  return (-a.x + 3*p.x - 3*q.x + b.x)*t**3 + (3*a.x - 6*p.x + 3*q.x)*t**2 + (3*p.x - 3*a.x)*t + a.x, (-a.y + 3*p.y - 3*q.y + b.y)*t**3 + (3*a.y - 6*p.y + 3*q.y)*t**2 + (3*p.y - 3*a.y)*t + a.y, color(int(200*t), int(200*(1-t)), int(sin(t*5)*200))


def s(t):
  return t, sin(2**(4*t)), COLOR


def fractional_to_screen(x, y, c):
  return int(x*320), int(y*222), c


DRAW_CALLBACK_INTERVAL = 50
def draw(f=quad, max_res=14, callback=false):
  callback_elasped = 0
  for res in range(1, max_res):
    for i in range(1, 2**res, 2):
      callback_elasped = callback_elasped + 1
      if callback_elasped >= DRAW_CALLBACK_INTERVAL:
        callback_elasped = 0
        if callback():
          return
      
      set_pixel(*fractional_to_screen(*f(i/2**res)))
      
  return True


def move_handle():
  move_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))
  if move_y:
    Handle.get_current_handle().y += move_y*SPEED
  
  move_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))
  if move_x:
    Handle.get_current_handle().x += move_x*SPEED
  
  return move_x or move_y


def update_handle():
  Handle.ui_select_handle()
  
  global clear_on_editing
  if keydown(KEY_ANS):
    clear_on_editing = False
  elif keydown(KEY_EXE):
    clear_on_editing = True
  
  if EMULATED and (keydown(KEY_BACK) or keydown(KEY_HOME) or keydown(KEY_OK)):
    exit()
  
  if move_handle():
    if Handle.current_handle_i == 1 or Handle.current_handle_i == 2:
      Handle.draw_handles()
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