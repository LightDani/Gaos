import os
import csv

from numpy import sin, cos, pi
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('easgamal')
def x_plus_1(x_i):
  return round(cos(17*x_i) * sin(8*x_i), 15)

def public_key(x):
  y = g**x % p
  return y

p = 2273
g = 0
for _ in range(1, p):
  g1 = [_**i % p for i in range(1, p)]
  g2 = [_**i % p for i in range(p, 2*p-1)]
  if g1 == g2 and len(set(g1)) == p-1:
    g = _
    break

# pembangkitan kunci
kunci = [pi/3]
data = {
  "kunci1" : [],
  "kunci2" : []
}

for i in range(1001):
  kunci.append(x_plus_1(kunci[i]))
  a = abs(kunci[-1])
  a = "{:<016s}".format(str(a).replace(".",""))
  a = [a[n-3:n] for n in range(len(a), 0, -3)]
  data["kunci1"].append(int(a[4]))
  data["kunci2"].append(int(a[3]))


x2 = data['kunci2'][0]
y1 = public_key(data['kunci1'][0])

def enc(m):
  ord_plain = [ord(c) for c in m]
  a = []
  b = []
  for i in range(len(ord_plain)):
    k = data['kunci2'][i+1]
    a.append(str(g**k % p).zfill(4))
    b.append(str((y1**k * ord_plain[i]) % p).zfill(4))
  a = "".join(a)
  b = "".join(b)
  return a, b

def dec(a, b):
  int_a = [int(a[i:i+4]) for i in range(0, len(a), 4)]
  int_b = [int(b[i:i+4]) for i in range(0, len(b), 4)]
  m = []
  for i in range(len(int_a)):
    ai = int_a[i]**(p-1-x2) % p
    m.append(int_b[i] * ai % p)

  return "".join([chr(i) for i in m])


while(1):
  prediction = []
  try:
    with open('test.csv') as t:
      a, b = t.readlines()
      a = a.replace('\n', '')

    m = dec(a, b)

    with open('test.csv', 'w+') as t:
      t.write(m)
    os.system('clear')
    with open('test.csv') as t:
      for test_set in csv.reader(t):
        inp1, inp2 = test_set
        prediction.append(model([np.array([eval(inp1)]), np.array([eval(inp2)])]).numpy()[0][0])
    os.remove('test.csv')
    for pred in prediction:
      print(pred)
  except:
    pass