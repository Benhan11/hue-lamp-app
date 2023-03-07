from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
import math



###*              RGB to xy               *###
#*     Red:   Huespec > Colormath (10-7)    *#
#*     Green: Huespec < Colormath (4-10)    *#
#*     Blue:  Huespec > Colormath (10-9)    *#
#*     White: Huespec T65 Conv. is BAD      *#
#*     Overall: Huespec too glitchy         *#
###*                                      *###



#- Bulb gamut
color_gamut = {
    "red": [],
    "green": [],
    "blue": []
}


def set_color_gamut(gamut):
    color_gamut["red"]   = gamut[0]
    color_gamut["green"] = gamut[1]
    color_gamut["blue"]  = gamut[2]


#* RGB to xy conversion using the colormath library [0, 255]
#* Different color approximations depending on illumination specification (ex. d55, d65)
#
#
#* d55: {
#-   Very weak Red, 
#+   Strong Green, 
#+   Strong Purpleish-Blue
#+   White point is fairly accurate (slightly toward Yellow-Orange)
#* }
#
#
#* d65: {
#-   Very weak Red,
#+   Strong Green, 
#+   Strong Purpleish-Blue
#+   White point is PERFECTLY accurate
#* }
def colormath_rgb_to_xy(r, g, b, target_illuminant):
    #- Get xyz from rgb
    rgb = sRGBColor(r, g, b, is_upscaled=True)
    xyz = convert_color(color=rgb, target_cs=XYZColor, target_illuminant=target_illuminant)

    #- Avoid division by zero
    if xyz.xyz_x + xyz.xyz_y + xyz.xyz_z == 0:
        xyz.xyz_x = 0.00001

    #- Derive x and y from xyz
    x = xyz.xyz_x / (xyz.xyz_x + xyz.xyz_y + xyz.xyz_z)
    y = xyz.xyz_y / (xyz.xyz_x + xyz.xyz_y + xyz.xyz_z)

    return {'x': x, 'y': y}


#  Adapted from https://github.com/johnciech/PhilipsHueSDK/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
#* RGB to xy conversion following HUE specifications [0, 255]
#* Different color approximations for different illumination conversion models
#
#
#* Wide RGB D65 Conversion {
#+   Strong Red,
#-   Weak Bluish-Green
#+   Strong Purpleish-Blue
#-   White point is EXTREMELY inaccurate (towards Red)
#* }
#
#
#* From https://github.com/benknight/hue-python-rgb-converter/blob/master/rgbxy/__init__.py {
#+   Strong Red,
#-   Very Weak Bluish-Green
#+   Strong Purpleish-Blue
#+   White point is fairly accurate (slightly towards Red)
#* }
def huespec_rgb_to_xy(r, g, b, RGB_D65_conversion):
    #- Convert to float
    r = r / 255
    g = g / 255
    b = b / 255

    #- Apply gamma correction
    red   = ((r + 0.055) / (1.0 + 0.055))**2.4 if (r > 0.04045) else (r / 12.92)
    green = ((g + 0.055) / (1.0 + 0.055))**2.4 if (g > 0.04045) else (g / 12.92)
    blue  = ((b + 0.055) / (1.0 + 0.055))**2.4 if (b > 0.04045) else (b / 12.92)

    #- Convert RGB to XYZ using Wide RGB D65 conversion
    if RGB_D65_conversion:
        X = red * 0.649926 + green * 0.103455 + blue * 0.197109
        Y = red * 0.234327 + green * 0.743075 + blue * 0.022598
        Z = red * 0.000000 + green * 0.053077 + blue * 1.035763

    #- Alternate values from https://github.com/benknight/hue-python-rgb-converter/blob/master/rgbxy/__init__.py
    else:
        X = red * 0.664511 + green * 0.154324 + blue * 0.162028
        Y = red * 0.283881 + green * 0.668433 + blue * 0.047685
        Z = red * 0.000088 + green * 0.072310 + blue * 0.986039

    #- Calculate xy from XYZ
    try:
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        xy_point = (x, y)
    except:
        xy_point = (0, 0)
    
    #- Check if point is in color reach otherwise find the closest point on the CIE 1931 'triangle'
    if not in_color_reach(xy_point):
        xy_point = closest_point_to_point(xy_point)

    return {
        'x': xy_point[0],
        'y': xy_point[1]
    }
    

def in_color_reach(xy_point):
    v1 = (color_gamut["green"][0] - color_gamut["red"][0], color_gamut["green"][1] - color_gamut["red"][1])
    v2 = (color_gamut["blue"][0] - color_gamut["red"][0], color_gamut["blue"][1] - color_gamut["red"][1])

    q = (xy_point[0] - color_gamut["red"][0], xy_point[1] - color_gamut["red"][1])

    s = cross_product(q, v2) / cross_product(v1, v2)
    t = cross_product(v1, q) / cross_product(v1, v2)

    return (s >= 0.0) and (t >= 0.0) and (s + t <= 1.0)


def cross_product(p1, p2):
    return (p1[0] * p2[1] - p1[1] * p2[0])


# Adapted from https://github.com/benknight/hue-python-rgb-converter/blob/f73a4ecb5dd0c5050edbfc460a696da685d441d7/rgbxy/__init__.py#L116
def closest_point_to_point(xy_point):
    #- Closest point in CIE 1931 'triangle' if the color is unreproducible
    pAB = closest_point_to_line(color_gamut["red"], color_gamut["green"], xy_point)
    pAC = closest_point_to_line(color_gamut["blue"], color_gamut["red"], xy_point)
    pBC = closest_point_to_line(color_gamut["green"], color_gamut["blue"], xy_point)

    #- Get distances per point
    dAB = distance_between_points(xy_point, pAB)
    dAC = distance_between_points(xy_point, pAC)
    dBC = distance_between_points(xy_point, pBC)

    #- Find the closest point
    lowest = dAB
    closest_point = pAB

    if (dAC < lowest):
        lowest = dAC
        closest_point = pAC

    if (dBC < lowest):
        lowest = dBC
        closest_point = pBC

    #- Change the value to one within the lamp's reach
    return (closest_point[0], closest_point[1])


# Adapted from https://github.com/benknight/hue-python-rgb-converter/blob/f73a4ecb5dd0c5050edbfc460a696da685d441d7/rgbxy/__init__.py#L101
def closest_point_to_line(A, B, xy_point):
    AP = (xy_point[0] - A[0], xy_point[1] - A[1])
    AB = (B[0] - A[0], B[1] - B[1])

    ab2 = AB[0] * AB[0] + AB[1] * AB[1]
    ap_ab = AP[0] * AB[0] + AP[1] * AB[1]

    t = ap_ab / ab2

    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0

    return (A[0] + AB[0] * t, A[1] + AB[1] * t)


def distance_between_points(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


#  Adapted from https://github.com/johnciech/PhilipsHueSDK/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
#  Reference https://github.com/benknight/hue-python-rgb-converter/blob/master/rgbxy/__init__.py
#* xy to RGB conversion following HUE specifications
#
#
#* (True) Wide RGB D65 Conversion {
#-   Worse Red (Orangeish)
#+   Better Blue
#+   White point less inaccurate (Pinkish)
#-   Worse representation on sliders
#* }
#
#
#* (False) Conversion from https://stackoverflow.com/a/45238704 {
#+   Better Red,
#-   Worse Blue (Purpleish)
#-   White point more inaccurate (Pink)
#+   Better representation on sliders
#* }
def huespec_xy_and_brightness_to_rgb(point, brightness, RGB_D65_conversion):
    xy_point = point

    #- Check if point is in color reach otherwise find the closest point on the CIE 1931 'triangle'
    if not in_color_reach(xy_point):
        xy_point = closest_point_to_point(xy_point)
    
    #- Calculate XYZ from xy
    x = xy_point[0]
    y = xy_point[1]
    z = 1 - x - y
    
    Y = brightness
    X = (Y / y) * x
    Z = (Y / y) * z

    #- Convert to RGB using Wide RGB D65 conversion
    if RGB_D65_conversion:
        r = X * 1.612 - Y * 0.203 - Z * 0.302 
        g = -X * 0.509 + Y * 1.412 + Z * 0.066
        b = X * 0.026 - Y * 0.072 + Z * 0.962

    #- Alternate values (far more accurate it would seem) from https://stackoverflow.com/a/45238704 
    else:
        r =  3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
        g = -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
        b =  0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z

    #- Reverse gamma correction
    r, g, b = map(
        lambda x: (12.92 * x) if (x <= 0.0031308) else ((1.0 + 0.055) * pow(x, (1.0 / 2.4)) - 0.055),
        [r, g, b]
    )

    #- Make non-negative
    r, g, b = map(lambda x: max(0, x), [r, g, b])

    #- If one component is greater than 1, weight components by that value
    max_component = max(r, g, b)
    if max_component > 1:
        r, g, b = map(lambda x: x / max_component, [r, g, b])

    r, g, b = map(lambda x: int(x * 255), [r, g, b])

    return {
        'red': r, 
        'green': g, 
        'blue': b
    }
