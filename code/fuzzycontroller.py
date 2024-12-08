"""
FLC: Fan Speed control
let two fuzzy inputs (Temperature (T) and Humidity (H) and one fuzzy output (Fan Speed (F))

Temperature range : [22 35]
temp_pertition:
  cool: open left MF (a = 22, b = 25.25)
  comfortable: Traingular(a = 22.7222, b = 26.3333, c = 29.9444)
  warm: Traingular(a = 27.0556, b = 30.6667, c = 34.2778)
  hot: open right MF (a = 31.75, b = 34.64)

Humidity range: [30 90]
hum_pertition:
  dry: open left MF(a = 30, b = 31.67)
  comfortable: Traingular(a = 33.3333, b = 50, c = 66.6667)
  humid: Traingular(a = 53.3333, b = 70, c = 86.6667)
  very_humid: open right MF(a = 75, b = 88.33)

Fan Speed: [0 100]
fs_pertition:
  OFF: open left MF(a = 2.083, b = 18.75)
  LOW: Traingular(a = .16667, b = 25, c = 45.8333)
  MED: Traingular(a = 29.1667, b = 50, c = 70.8333)
  HIGH: Traingular(a = 54.1667, b = 75, c = 95.8333)
  MAX: open right MF(a = 81.25, b = 97.92)

Rules:
  R1: IF cool and dry then FS is OFF
  R2: IF cool and comfortable then FS is OFF
  R3: IF cool and humid then FS is LOW
  R4: IF cool and very_humid then FS is LOW

  R5: IF comfortable and dry then FS is LOW
  R6: IF comfortable and comfortable then FS is LOW
  R7: IF comfortable and humid then FS is MED
  R8: IF comfortable and very_humid then FS is MED

  R9: IF warm and dry then FS is MED
  R10:  IF warm and comfortable then FS is MED
  R11:  IF warm and humid then FS is HIGH
  R12:  IF warm and very_humid then FS is HIGH

  R13:  IF hot and dry then FS is HIGH
  R14:  IF hot and comfortable then FS is HIGH
  R15:  IF hot and humid then FS is MAX
  R16:  IF hot and very_humid then FS is MAX
"""

# Functions for open left-Right fuzzyfication
def open_left(x, alpha, beta):
    if x < alpha:
        return 1
    elif alpha <= x < beta:
        return (beta - x) / (beta - alpha)
    else:
        return 0

def open_right(x, alpha, beta):
    if x < alpha:
        return 0
    elif alpha <= x < beta:
        return (x - alpha) / (beta - alpha)
    else:
        return 1


# Function for traingular fuzzyfication
def triangular(x, a, b, c):
    value = min((x - a) / (b - a), (c - x) / (c - b))
    if value > 0:
        return value
    return 0


# Temperature Fuzzy Partition
def temp_partition(x):
    cool = 0; comf_temp = 0; warm = 0; hot = 0

    if x > 22 and x < 25.25:
        cool = open_left(x, 22.36, 25.25)
    if x > 22.7222 and x < 29.9444:
        comf_temp = triangular(x, 22.7222, 26.3333, 29.9444)
    if x > 27.0556 and x < 34.2778:
        warm = triangular(x, 27.0556, 30.6667, 34.2778)
    if x > 31.75 and x < 35:
        hot = open_right(x, 31.75, 34.64)

    return cool, comf_temp, warm, hot

# Humidity Fuzzy Partition
def hum_partition(x):
    dry = 0; comf_hum = 0; humid = 0; very_humid = 0

    if x > 30 and x < 45:
        dry = open_left(x, 31.67, 45)
    if x > 33.3333 and x < 66.6667:
        comf_hum = triangular(x, 33.3333, 50, 66.6667)
    if x > 53.3333 and x < 86.6667:
        humid = triangular(x, 53.3333, 70, 86.6667)
    if x > 75 and x < 90:
        very_humid = open_right(x, 75, 88.33)

    return dry, comf_hum, humid, very_humid

# Compare values
def bi_compare(TC1, TC2):
    return TC2 if TC1 == 0 or (TC2 != 0 and TC1 > TC2) else TC1

def quad_compare(TC1, TC2, TC3, TC4):
    values = [TC1, TC2, TC3, TC4]
    non_zero_values = [value for value in values if value != 0]
    if non_zero_values:
      return min(non_zero_values)
    else:
      return 0

# Rule Implementation
def rule(cool, comf_temp, warm, hot, dry, comf_hum, humid, very_humid):
    off1 = min(cool, dry)
    off2 = min(cool, comf_hum)
    off = bi_compare(off1, off2)

    low1 = min(cool, humid)
    low2 = min(cool, very_humid)
    low3 = min(comf_temp, dry)
    low4 = min(comf_temp, comf_hum)
    low = quad_compare(low1, low2, low3, low4)

    med1 = min(comf_temp, humid)
    med2 = min(comf_temp, very_humid)
    med3 = min(warm, dry)
    med4 = min(warm, comf_hum)
    med = quad_compare(med1, med2, med3, med4)

    high1 = min(warm, humid)
    high2 = min(warm, very_humid)
    high3 = min(hot, dry)
    high4 = min(hot, comf_hum)
    high = quad_compare(high1, high2, high3, high4)

    max1 = min(hot, humid)
    max2 = min(hot, very_humid)
    MAX = bi_compare(max1, max2)

    return off, low, med, high, MAX

# De-fuzzyfication areas
def area_TR(mu, a, b, c):
    x1 = mu*(b-a) + a
    x2 = c - mu*(c-b)
    d1 = (c-a); d2 = x2-x1
    a = (1/2)*mu*(d1 + d2)
    return a # Returning area

def area_OL(mu, alpha, beta):
    xOL = beta - (mu * (beta - alpha))
    return 1/2*mu*(beta+ xOL), beta/2

def area_OR(mu, alpha, beta):
    xOR = (beta - alpha)*mu + alpha
    aOR = (1/2)*mu*((240 - alpha) + (240 -xOR))
    return aOR, (240 - alpha)/2 + alpha


# De-fuzzyfication
def defuzzyfication(off, low, med, high, MAX):
    area_off = 0; area_low = 0; area_med = 0; area_high = 0; area_max = 0
    c_off = 0; c_low = 0; c_med = 0; c_high = 0; c_max = 0

    if off != 0:
        area_off, c_off = area_OR(off, 2.083, 18.7)
    if low != 0:
        area_low = area_TR(low, 0.16667, 25, 45.8333)
        c_low = 25
    if med != 0:
        area_med = area_TR(med, 29.1667, 50, 70.8333)
        c_med = 50
    if high != 0:
        area_high = area_TR(high, 54.1667, 75, 95.8333)
        c_high = 75
    if MAX != 0:
        area_max, c_max = area_OL(MAX, 81.25, 97.92)

    numerator = area_off*c_off + area_low*c_low + area_med*c_med + area_high*c_high + area_max*c_max
    denominator = area_off + area_low + area_med + area_high + area_max

    if denominator != 0:
        return numerator/denominator
    else:
        print("No rules exist to give the result")
        return 0


def fan_speed(temperature, humidity):
    cool, comf_temp, warm, hot = temp_partition(temperature)
    dry, comf_hum, humid, very_humid = hum_partition(humidity)

    off, low, med, high, MAX = rule(cool, comf_temp, warm, hot, dry, comf_hum, humid, very_humid)

    fan_speed = defuzzyfication(off, low, med, high, MAX)

    return fan_speed

if __name__ == "__main__":
    temperature = 23
    humidity = 36

    fan_speed = fan_speed(temperature, humidity)
    print(f"The fan speed is {fan_speed}")
