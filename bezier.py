from math import *
from ion import *
from kandinsky import *

EMULATED = False
try: f""; EMULATED = True
except: pass


a=0
p=1
b=0.5


def false():
  return False


def quad(t):
  return (a - 2*p + b)*t**2 + (2*p - 2*a)*t + a


def s(t):
  return sin(2**(4*t))


def draw(f=quad, max_res=14, callback=false):
  for res in range(1,max_res):
    for i in range(1,2**res,2):
      if callback():
        return
      set_pixel(int(200*i/2**res),int(f(i/2**res)*200),color(0,0,0))
  return True

handle_i=0
def update_handle():
  global handle_i
  handle_i+=int(keydown(KEY_RIGHT))-int(keydown(KEY_LEFT))
  
  move=int(keydown(KEY_UP))-int(keydown(KEY_DOWN))
  
  if move:
    mod=handle_i % 3
    if mod==0:
      global a
      a+=move/100
    elif mod==1:
      global p
      p+=move/100
    else:
      global b
      b+=move/100
  
  return move


def bezier():
  while True:
    fill_rect(0,0,500,300,color(255,255,255))
    if draw(f=quad, max_res=10,callback=update_handle):
      while not update_handle():
        pass


if EMULATED and __name__ == "__main__":
  bezier()