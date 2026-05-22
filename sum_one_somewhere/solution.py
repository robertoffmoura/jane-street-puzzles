from mpmath import mp

mp.dps = 50
sol = mp.findroot(lambda x: 3*x**3 - 10*x**2 + 12*x - 4, 0.5)
mp.nprint(sol,10)
