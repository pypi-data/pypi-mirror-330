import matplotlib.pyplot as plt
from puzzleandy import *

n = 256

x = woman_1()
y = subway()
x = match_hist(x,y,n)
show(x)

x = subway()
x = eq_hist(x,n)
show(x)