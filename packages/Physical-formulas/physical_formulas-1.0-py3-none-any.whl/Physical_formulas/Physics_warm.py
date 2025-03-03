def quantity_of_heat(c, m, t_beg, t_end):
    return c*m*(t_end-t_beg)

def temperature_change(Q, c, m):
    return Q/c*m

def begin_temperature(Q, c, m, t_end):
    return abs((Q/c*m) - t_end)

def final_temperature(Q, c, m, t_beg):
    return abs((Q / c * m) + t_beg)

def mass(Q,c, t_beg, t_end):
    return Q/c*(abs(t_beg-t_end))

def specific_heat_capacity(Q, m, t_beg, t_end):
    return Q/(m*abs(t_beg-t_end))