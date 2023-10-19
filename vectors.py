from math import *
from typing import Any

def crossProd(a, b): #returns the cross product of two vector3's
  if isinstance(a, vector3) and isinstance(b, vector3):
    return vector3(a.y * b.z - b.y * a.z, b.x * a.z - a.x * b.z, a.x * b.y - b.x * a.y)
  else:
    ValueError(f"x only works on vector3 and vector3 and not with {type(a)} and {type(b)}!")

def angl(a, b): #returns the angle between two vectors
  if isinstance(a, vector3) and isinstance(b, vector3) or isinstance(
      a, vector2) and isinstance(b, vector2):
    return acos((a * b) / (a.amount() * b.amount()))
  else:
    return ValueError(f"angl only works on vector3 and vector3 or vector2 and vector2 and not with {type(a)} and {type(b)}!")

def vecPar(a, b): #checks if two vectors are paralell or not
  return a.amount() * b.amount() == a * b

def intersect(g1, g2): #returns the intersection of g1 and g2
  dk = g1.a.y * g2.a.x - g2.a.y * g1.a.x
  if dk == 0:
    return None
  dt = g2.a.y * (g1.op.x - g2.op.x) - g2.a.x * (g1.op.y - g2.op.y)
  dt2 = g1.a.x * (g1.op.y + g2.op.y) - g1.a.y * (g1.op.x - g2.op.x)
  t = dt / dk
  t2 = dt2 / dk
  return g1.calc(t) if g1.op.z - g2.op.z == t2 * g2.a.z - t * g1.a.z else None

def det3x3(a):
  return (a[0][0]*a[1][1]*a[2][2]+a[0][1]*a[1][2]*a[2][0]+a[0][2]*a[1][0]*a[2][1]) - (a[2][0]*a[1][1]*a[0][2]+a[2][1]*a[1][2]*a[0][0]+a[2][2]*a[1][0]*a[0][1])

def mul3x3(a, b):
  return [
    [a[0][0]*b[0][0]+a[1][0]*b[0][1]+a[2][0]*b[0][2], a[0][1]*b[0][0]+a[1][1]*b[0][1]+a[2][1]*b[0][2], a[0][2]*b[0][0]+a[1][2]*b[0][1]+a[2][2]*b[0][2]],
    [a[0][0]*b[1][0]+a[1][0]*b[1][1]+a[2][0]*b[1][2], a[0][1]*b[1][0]+a[1][1]*b[1][1]+a[2][1]*b[1][2], a[0][2]*b[1][0]+a[1][2]*b[1][1]+a[2][2]*b[1][2]],
    [a[0][0]*b[2][0]+a[1][0]*b[2][1]+a[2][0]*b[2][2], a[0][1]*b[2][0]+a[1][1]*b[2][1]+a[2][1]*b[2][2], a[0][2]*b[2][0]+a[1][2]*b[2][1]+a[2][2]*b[2][2]]
  ]

def pIntersectG(e, g1, g1tLim = None, etLim = None, esLim = None):
  n = e.n()
  if n * g1.a == 0:
    return None
  dk = det3x3([
    [e.a.x, e.b.x, -g1.a.x],
    [e.a.y, e.b.y, -g1.a.y],
    [e.a.z, e.b.z, -g1.a.z]
  ])
  dt = det3x3([
    [g1.op.x - e.op.x, e.b.x, -g1.a.x],
    [g1.op.y - e.op.y, e.b.y, -g1.a.y],
    [g1.op.z - e.op.z, e.b.z, -g1.a.z]
  ])
  ds = det3x3([
    [e.a.x, g1.op.x - e.op.x, -g1.a.x],
    [e.a.y, g1.op.y - e.op.y, -g1.a.y],
    [e.a.z, g1.op.z - e.op.z, -g1.a.z]
  ])
  dp = det3x3([
    [e.a.x, e.b.x, g1.op.x - e.op.x],
    [e.a.y, e.b.y, g1.op.y - e.op.y],
    [e.a.z, e.b.z, g1.op.z - e.op.z]
  ])
  t = dt/dk
  s = ds/dk
  p = dp/dk
  if g1tLim != None:
    if p < g1tLim[0] or p > g1tLim[1]:
      return None
  if etLim != None:
    if t < etLim[0] or t > etLim[1]:
      return None
  if esLim != None:
    if s < esLim[0] or s > esLim[1]:
      return None
  return g1.calc(p)

def pReflectG(e, g1, sp): #returns the reflection of a line and a plane
  ret = gP(vector3(0, 0, 0), vector3(0, 0, 0))
  n = e.n()
  a = g1.a * -1
  ret.op = sp
  alpha = angl(a, n)
  if degrees(alpha) > 90:
    n = n * -1
    alpha = angl(a, n)
  a = a.unitVec() * (n.amount()/cos(alpha))
  a = n + (n - a)
  ret.a = a
  return ret

class vector3:

  def __init__(self, x = 0, y = 0, z = 0):
    self.x = x
    self.y = y
    self.z = z

  def unitVec(self):
    return self / self.amount()

  def amount(self):
    return sqrt(self.x**2 + self.y**2 + self.z**2)

  def tuple(self):
    return (self.x, self.y, self.z)

  def __add__(self, other):
    if isinstance(other, vector3):
      return vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 3:
        return vector3(self.x + other[0], self.y + other[1], self.z + other[2])
  
  def __radd__(self, other):
    if isinstance(other, vector3):
      return vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 3:
        return vector3(self.x + other[0], self.y + other[1], self.z + other[2])

  def __sub__(self, other):
    if isinstance(other, vector3):
      return vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 3:
        return vector3(self.x - other[0], self.y - other[1], self.z - other[2])

  def __mul__(self, other):
    if isinstance(other, vector3):
      return self.x * other.x + self.y * other.y + self.z * other.z
    elif isinstance(other, float) or isinstance(other, int):
      return vector3(self.x * other, self.y * other, self.z * other)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 3:
        return self.x * other[0] + self.y * other[1] + self.z * other[2]
  
  def __rmul__(self, other):
    if isinstance(other, vector3):
      return self.x * other.x + self.y * other.y + self.z * other.z
    elif isinstance(other, float) or isinstance(other, int):
      return vector3(self.x * other, self.y * other, self.z * other)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 3:
        return self.x * other[0] + self.y * other[1] + self.z * other[2]

  def __truediv__(self, other):
    if isinstance(other, float) or isinstance(other, int) and other != 0:
      return vector3(self.x / other, self.y / other, self.z / other)

  def __eq__(self, other):
    if isinstance(other, vector3):
      return (self.x == other.x) and (self.y == other.y) and (self.z== other.z)
    elif isinstance(other, tuple) or isinstance(other, list):
      return (self.x == other[0]) and (self.y == other[1]) and (self.z== other[2])
    else:
      return False

  def __gt__(self, other):
    if isinstance(other, vector3):
      return self.amount() > other.amount()
    elif isinstance(other, tuple) or isinstance(other, list):
      return self.amount() > sqrt(other[0]**2 + other[1]**2 + other[2]**2)

  def __lt__(self, other):
    if isinstance(other, vector3):
      return self.amount() < other.amount()
    elif isinstance(other, tuple) or isinstance(other, list):
      return self.amount() < sqrt(other[0]**2 + other[1]**2 + other[2]**2)

  def __ge__(self, other):
    if isinstance(other, vector3):
      return self.aamount() >= other.amount()
    elif isinstance(other, tuple) or isinstance(other, list):
      return self.amount() >= sqrt(other[0]**2 + other[1]**2 + other[2]**2)

  def __le__(self, other):
    if isinstance(other, vector3):
      return self.amount() <= other.amount()
    elif isinstance(other, tuple) or isinstance(other, list):
      return self.amount() <= sqrt(other[0]**2 + other[1]**2 + other[2]**2)

  def __str__(self):
    return f"{self.x}, {self.y}, {self.z}"

  def __len__(self):
    return 3

class vector2:

  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y

  def unitVec(self):
    return self / self.amount()

  def amount(self):
    return sqrt(self.x**2 + self.y**2)

  def tuple(self):
    return (self.x, self.y)

  def __add__(self, other):
    if isinstance(other, vector2):
      return vector2(self.x + other.x, self.y + other.y)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 2:
        return vector2(self.x + other[0], self.y + other[1])
  
  def __radd__(self, other):
    if isinstance(other, vector2):
      return vector2(self.x + other.x, self.y + other.y)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 2:
        return vector2(self.x + other[0], self.y + other[1])

  def __sub__(self, other):
    if isinstance(other, vector2):
      return vector2(self.x - other.x, self.y - other.y)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 2:
        return vector2(self.x - other[0], self.y - other[1])

  def __mul__(self, other):
    if isinstance(other, vector2):
      return self.x * other.x + self.y * other.y
    elif isinstance(other, float) or isinstance(other, int):
      return vector2(self.x * other, self.y * other)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 2:
        return self.x * other[0] + self.y * other[1]
  
  def __rmul__(self, other):
    if isinstance(other, vector2):
      return self.x * other.x + self.y * other.y
    elif isinstance(other, float) or isinstance(other, int):
      return vector2(self.x * other, self.y * other)
    elif isinstance(other, tuple) or isinstance(other, list):
      if len(other) >= 2:
        return self.x * other[0] + self.y * other[1]

  def __truediv__(self, other):
    if isinstance(other, float) or isinstance(other, int) and other != 0:
      return vector2(self.x / other, self.y / other)

  def __eq__(self, other):
    if isinstance(other, vector2):
      return (self.x == other.x) and (self.y == other.y)
    elif isinstance(other, tuple) or isinstance(other, list) and len(other) == 2:
      return (self.x == other[0]) and (self.y == other[1])
    else:
      return False

  def __gt__(self, other):
    if isinstance(other, vector2):
      return self.amount() > other.amount()
    elif isinstance(other, tuple) or isinstance(other, list) and len(other) == 2:
      return self.amount() > sqrt(other[0]**2 + other[1]**2)

  def __lt__(self, other):
    if isinstance(other, vector2):
      return self.amount() < other.amount()
    elif isinstance(other, tuple) or isinstance(other, list) and len(other) == 2:
      return self.amount() < sqrt(other[0]**2 + other[1]**2)

  def __ge__(self, other):
    if isinstance(other, vector2):
      return self.amount() >= other.amount()
    elif isinstance(other, tuple) or isinstance(other, list) and len(other) == 2:
      return self.amount() >= sqrt(other[0]**2 + other[1]**2)

  def __le__(self, other):
    if isinstance(other, vector2):
      return self.amount() <= other.amount()
    elif isinstance(other, tuple) or isinstance(other, list) and len(other) == 2:
      return self.amount() <= sqrt(other[0]**2 + other[1]**2)

  def __str__(self):
    return f"{self.x}, {self.y}"

  def __len__(self):
    return 3

class plane:

  def __init__(self, op: vector3, a: vector3, b: vector3):
    self.op = op
    self.a = a
    self.b = b
  
  def n(self):
    return crossProd(self.a, self.b)
  
  def calc(self, t, s):
    return self.op + t * self.a + s * self.b
  
  def onPlane(self, p: vector3):
    dk = self.a.x * self.b.y - self.a.y * self.b.x
    if dk == 0:
      return (False, 0, 0)
    dt = self.b.y * (p.z - self.op.z) - self.b.x * (p.y - self.op.y)
    ds = self.a.x * (p.z - self.op.z) - self.a.y * (p.y - self.op.y)
    t = dt / dk
    s = ds / dk
    return (True, t, s) if p.z - self.op.z == t * self.a.z + s * self.b.z else (False, 0, 0)

class g:

  def __init__(self, k, d):
    self.k = k
    self.d = d
  
  def calc(self, x):
    return self.k * x + self.d
  
  def element(self, p):
    return p.y == self.calc(p.x)
  
  def __str__(self):
    return f"y = {self.k} * x + {self.d}"

class gP:

  def __init__(self, op: vector3, a: vector3):
    self.op = op
    self.a = a
    
  def calc(self, t):
    return self.op + t * self.a

  def element(self, p):
    v = p - self.op
    if vecPar(v, self.a):
      t = v.amount() / self.a.amount()
      return (True, t if v.unitVec() == self.a.unitVec() else -t)
    else:
      return (False, 0)
  
  def __str__(self):
    return f"X = ({self.op}) + t * ({self.a})"