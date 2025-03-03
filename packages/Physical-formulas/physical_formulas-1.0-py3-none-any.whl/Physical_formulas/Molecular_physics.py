R = 8,31
def pressure(v, t, ny):
    return (t*ny*R)/v
def kelvin_temperature(t):
    return t+273
def volume(p, t, ny):
    return (t*ny*R)/p
def internal_energy(ny,t):
    return 3/2*(ny*R*t)
def amount_of_substance(m, moler_m):
    return m/moler_m
def basic_equation_mkt_nRT(p, v):
    return p*v
def basic_equation_mkt_PV(t, ny):
    return ny*R*t