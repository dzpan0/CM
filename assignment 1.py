#B. Write a function for each of the processing steps and name these functions: 
#“start”, “perceptualstep”, “cognitivestep”, and “motorstep”. The functions 
#have no input and return as output the time this step took in milliseconds 

_error_multiplication_factors = {
     "f": 3,
     "m": 2,
     "s": 0.5,
}

def perceptualstep(mode, error_rate):
    if mode == "f":
        t_p = 50
    elif mode == "m":
        t_p = 100
    elif mode == "s":
        t_p = 200

    return t_p, _error_multiplication_factors[mode]*error_rate

def cognitivestep(mode, error_rate):
    if mode == "f":
        t_c = 25
    elif mode == "m":
        t_c = 70
    elif mode == "s":
        t_c = 170

    return t_c, _error_multiplication_factors[mode]*error_rate

def motorstep(mode, error_rate):
    if mode == "f":
            t_p = 30
    elif mode == "m":
            t_p = 70
    elif mode == "s":
            t_p = 100

    return t_p, _error_multiplication_factors[mode]*error_rate

def example1():
    t_p = perceptualstep()
    t_c = cognitivestep()
    t_m = motorstep()
    pass

def example3():

    string1 = input()
    mode1, mode2, mode3, mode4, mode5 = string1.split()

    tp = perceptualstep(mode1)
    tp2 = perceptualstep(mode2)
    tc = cognitivestep(mode3)
    tc2 = cognitivestep(mode4)
    tm = motorstep(mode5)

    return tp + tp2 + tc + tc2 + tm


def example4():
    string1 = input()
    mode1, mode2, mode3, mode4, mode5 = string1.split()
    total = []
    times = [40, 80, 110, 150, 210, 240]
    for t in times:
        tp = perceptualstep(mode1)
        tp2 = perceptualstep(mode2)
        tc = cognitivestep(mode3)
        tc2 = cognitivestep(mode4)
        tm = motorstep(mode5)
        total.append(tp + t + tp2 + tc + tc2 + tm)

    return total

def example5():
    error_rate = 0.01
    total_times = []
    error_rates = []
    speed_options = ["f", "m", "s"]

    for perceptual in speed_options:
        for cognitive in speed_options:
             for motor in speed_options:
                tp, error_rate = perceptualstep(perceptual, error_rate)
                tp2, error_rate = perceptualstep(perceptual, error_rate)
                tc, error_rate = cognitivestep(cognitive, error_rate)
                tc2, error_rate = cognitivestep(cognitive, error_rate)
                tm, error_rate = motorstep(motor, error_rate)
                total_times.append(tp + tp2 + tc + tc2 + tm)
                error_rates.append(error_rate)
    
