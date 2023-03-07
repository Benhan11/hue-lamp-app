import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
from color_conversion import *
import json
import requests
import urllib3
import math
import sys
import time



###* Config

#- Disable unsafe request related warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#- Slider update rate-limiting
t0 = time.perf_counter()
allowed_updates_per_second = 5
t_update_interval = 1 / allowed_updates_per_second

#- GUI
root = tk.Tk()
root.option_add("*font", "CascadiaMono 14")
w_width = 504
w_height = 356
is_resizable = True

#- Exit on 'esc'
def close(_event):
    sys.exit()
root.bind('<Escape>', close)

#- Ben bedroom light
ben_light = 10

#- HUE bridge username
f = open('credentials.json')
username = json.load(f)['username']
f.close()

#- API-endpoint
URL = f"https://192.168.1.142/api/{username}"

#- Light on-state
on_state = False

#- Data file path
data_file_path = 'data/data.json'

#- Selected palette
selected_palette_box = None



###* GUI functions

def create_gui(light_info, initial_rgb, initial_bri):

    ###* Window config
    root.geometry(f"{w_width}x{w_height}")
    root.resizable(is_resizable, is_resizable)
    root.title("HUE Lamp Color")
    root.iconbitmap("./images/icons/bulb.ico")


    ###* Content config

    ##+ Content images

    slider_icon_size = 20
    button_icon_size = 40
    palette_box_size = 125
    palette_color_preview_size = 50

    slider_icon_names = ['red', 'green', 'blue', 'brightness']
    slider_icons = get_resized_tk_images(path="./images/icons/", image_names=slider_icon_names, size=slider_icon_size)

    button_icon_names = ['power-button-off', 'power-button-on']
    button_icons = get_resized_tk_images(path="./images/icons/", image_names=button_icon_names, size=button_icon_size)

    palette_boxes_names = ['palette_box', 'palette_box_pressed']
    palette_boxes = get_resized_tk_images(path="./images/design/", image_names=palette_boxes_names, size=palette_box_size)
    palette_preview_overlay_image = Image.open("./images/design/overlay.png")


    ##+ Fonts
    slider_font = ("Cascadia Mono", 12)
    palette_font = ("Cascadia Mono", 10)
    palette_max_font_size = 13


    ##+ Dimensions

    slider_length = 300
    slider_val_label_width = 3
    palette_text_label_size = palette_box_size - 30
    max_palette_rows = 2


    ##+ Padding

    slider_padx_s = 25
    slider_padx_l = 50
    slider_pady_s = 4
    slider_pady_l = 50

    palette_pady = 60
    palette_box_padding = 0

    button_pady = 50


    ###* Content

    ##+ Red slider

    #- Widgets
    r_label = tk.Label(root, image=slider_icons["red"])
    r_scale = ttk.Scale(root, from_=0, to=255, orient='horizontal', length=slider_length, value=initial_rgb["red"])
    r_val_label = tk.Label(root, width=slider_val_label_width, text=initial_rgb["red"], anchor="e", font=slider_font)

    #- Placement
    r_label.grid(row=0, column=0, padx=(slider_padx_l, 0), pady=(slider_pady_l, 0))
    r_scale.grid(row=0, column=1, padx=(slider_padx_s, 0), pady=(slider_pady_l, 0))
    r_val_label.grid(row=0, column=2, padx=(slider_padx_s, slider_padx_l), pady=(slider_pady_l, 0))

    #- Events
    r_scale["command"] = lambda val: color_slider_update(val, r_scale["value"], g_scale["value"], b_scale["value"], r_val_label, release=False)
    r_scale.bind("<ButtonRelease-1>", lambda _event: color_slider_update(r_scale["value"], r_scale["value"], g_scale["value"], b_scale["value"], r_val_label, release=True))


    ##+ Green slider

    #- Widgets
    g_label = tk.Label(root, image=slider_icons["green"])
    g_scale = ttk.Scale(root, from_=0, to=255, orient='horizontal', length=slider_length, value=initial_rgb["green"])
    g_val_label = tk.Label(root, width=slider_val_label_width, text=initial_rgb["green"], anchor="e", font=slider_font)
    
    #- Placement
    g_label.grid(row=1, column=0, padx=(slider_padx_l, 0), pady=(slider_pady_s, 0))
    g_scale.grid(row=1, column=1, padx=(slider_padx_s, 0), pady=(slider_pady_s, 0))
    g_val_label.grid(row=1, column=2, padx=(slider_padx_s, slider_padx_l), pady=(slider_pady_s, 0))
    
    #- Events
    g_scale["command"] = lambda val: color_slider_update(val, r_scale["value"], g_scale["value"], b_scale["value"], g_val_label, False)
    g_scale.bind("<ButtonRelease-1>", lambda _event: color_slider_update(g_scale["value"], r_scale["value"], g_scale["value"], b_scale["value"], g_val_label, release=True))


    ##+ Blue slider

    #- Widgets
    b_label = tk.Label(root, image=slider_icons["blue"])
    b_scale = ttk.Scale(root, from_=0, to=255, orient='horizontal', length=slider_length, value=initial_rgb["blue"])
    b_val_label = tk.Label(root, width=slider_val_label_width, text=initial_rgb["blue"], anchor="e", font=slider_font)

    #- Placement    
    b_label.grid(row=2, column=0, padx=(slider_padx_l, 0), pady=(slider_pady_s, 0))
    b_scale.grid(row=2, column=1, padx=(slider_padx_s, 0), pady=(slider_pady_s, 0))
    b_val_label.grid(row=2, column=2, padx=(slider_padx_s, slider_padx_l), pady=(slider_pady_s, 0))

    #- Events
    b_scale["command"] = lambda val: color_slider_update(val, r_scale["value"], g_scale["value"], b_scale["value"], b_val_label, False)
    b_scale.bind("<ButtonRelease-1>", lambda _event: color_slider_update(b_scale["value"], r_scale["value"], g_scale["value"], b_scale["value"], b_val_label, release=True))    


    ##+ Brightness slider

    #- Widgets
    bri_label = tk.Label(root, image=slider_icons["brightness"])
    bri_scale = ttk.Scale(root, from_=1, to=255, orient='horizontal', length=slider_length, value=initial_bri)
    bri_val_label = tk.Label(root, width=slider_val_label_width, text=initial_bri, anchor="e", font=slider_font)

    #- Placement
    bri_label.grid(row=3, column=0, padx=(slider_padx_l, 0), pady=(slider_pady_l, 0))
    bri_scale.grid(row=3, column=1, padx=(slider_padx_s, 0), pady=(slider_pady_l, 0))
    bri_val_label.grid(row=3, column=2, padx=(slider_padx_s, slider_padx_l), pady=(slider_pady_l, 0))

    #- Events
    bri_scale["command"] = lambda val: bri_slider_update(val, bri_val_label, release=False)
    bri_scale.bind("<ButtonRelease-1>", lambda _event: bri_slider_update(bri_scale["value"], bri_val_label, release=True))


    ##+ Palettes
    make_palettes_widget(pady=palette_pady, 
                         max_rows=max_palette_rows,
                         box_image=palette_boxes["palette_box"],
                         box_image_pressed=palette_boxes["palette_box_pressed"],
                         box_size=palette_box_size, 
                         box_padding=palette_box_padding,
                         text_label_size=palette_text_label_size, 
                         font=palette_font, 
                         max_font_size=palette_max_font_size,
                         preview_size=palette_color_preview_size, 
                         preview_overlay_image=palette_preview_overlay_image)


    ##+ On/Off button

    #- Widgets
    onoff_state = "on" if light_info['state']['on'] else "off"
    onoff_button = tk.Button(root, image=button_icons[f"power-button-{onoff_state}"], border=0)

    #- Placement
    onoff_button.grid(row=6, column=0, pady=(button_pady, 0), columnspan=3)

    #- Events    
    onoff_button["command"] = lambda: press_light_button(onoff_button, button_icons["power-button-on"], button_icons["power-button-off"])    




    #!!! BOUNDARY TEST !!!#
    #t = tk.Label(root, image=slider_icons["red"]).grid(row=100, column=0, columnspan=3, sticky="E")


    ##+ Run the tkinter window
    root.mainloop()


def get_resized_tk_images(path, image_names, size):
    resized_images = {}
    for image_name in image_names:
        img = Image.open(f"{path}{image_name}.png")
        img = img.resize((size, size), Image.LANCZOS)
        img_resized = ImageTk.PhotoImage(img)
        resized_images[image_name] = img_resized

    return resized_images
    

def press_light_button(button, icon_on, icon_off):
    toggle_light()
    is_on = get_light_is_on()
    image = icon_on if is_on else icon_off
    button.configure(image=image)


def get_all_palettes():
    return get_data_file_dict()["saved_palettes"]
    

def make_palettes_widget(pady, max_rows, 
                         box_image, box_image_pressed, box_size, box_padding,
                         text_label_size, font, max_font_size,
                         preview_size, preview_overlay_image):
    
    global w_height

    palettes = get_all_palettes()
    palettes_count = len(palettes)

    cols_per_row = math.ceil(palettes_count / max_rows) if max_rows > 0 else 0
    rows = max_rows if palettes_count >= max_rows else palettes_count
    if (rows == 0):
        return
    
    frame_size = (box_size + box_padding) * rows

    #- Resize entire window according to the frame and an offset for the scrollbar
    w_height = w_height + (frame_size + pady + 17)
    root.geometry(f"{w_width}x{w_height}")

    palettes_frame = make_palettes_frame(row=4, column=0, columnspan=3, padx=0, pady=(pady, 0), frame_size=frame_size)

    for i, (p_name, p_data) in enumerate(palettes.items()):         
        row = math.floor(i / cols_per_row)
        col = i - (row * cols_per_row)

        colored_preview_image = get_colored_image(p_data, preview_size, preview_overlay_image)

        make_palette(frame=palettes_frame,
                    row=row,
                    column=col,
                    padding=box_padding,
                    name=p_name,
                    label_size=text_label_size,
                    font=font,
                    max_font_size=max_font_size,
                    box_image=box_image,
                    box_image_pressed=box_image_pressed,
                    color_preview_image=colored_preview_image)


def make_palettes_frame(row, column, columnspan, padx, pady, frame_size):
    outer_frame = tk.Frame(root, borderwidth=1)
    outer_frame.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)

    p_canvas = tk.Canvas(outer_frame, borderwidth=0, height=frame_size)
    p_frame = tk.Frame(p_canvas)
    p_scrollbar = tk.Scrollbar(outer_frame, orient="horizontal", command=p_canvas.xview)
    p_canvas.config(xscrollcommand=p_scrollbar.set)

    p_scrollbar.pack(side="bottom", fill="x")
    p_canvas.pack(side="top", fill="both", expand=True)
    p_canvas.create_window((0, 0), window=p_frame, anchor="w")

    p_frame.bind("<Configure>", lambda _event, canvas=p_canvas: on_frame_configure(canvas))

    return p_frame


# TODO Split long palette names
def make_palette(frame, row, column, padding, name, label_size, font, max_font_size, box_image, box_image_pressed, color_preview_image):
    #- Contents
    box_frame = tk.Frame(frame, borderwidth=0)
    box = tk.Label(box_frame, image=box_image, border=0, cursor="hand2")
    text_label = tk.Label(box_frame, text=name, font=font, background="white", cursor="hand2")
    image_label = tk.Label(box_frame, image=color_preview_image, background="white", cursor="hand2")
    image_label.image = color_preview_image

    #- Content placement
    box_frame.grid(row=row, column=column, padx=(0, padding), pady=(0, padding))
    box.grid(row=0, column=0, rowspan=2)
    text_label.grid(row=0, column=0, sticky="N", pady=(20, 0))
    image_label.grid(row=1, column=0, sticky="S", pady=(0, 20))

    #- Events
    box.bind("<ButtonRelease-1>", lambda _event: press_release_palette(name=name, box=box, images=[box_image, box_image_pressed]))
    text_label.bind("<ButtonRelease-1>", lambda _event: press_release_palette(name=name, box=box, images=[box_image, box_image_pressed]))
    image_label.bind("<ButtonRelease-1>", lambda _event: press_release_palette(name=name, box=box, images=[box_image, box_image_pressed]))

    approximate_font_size(text_label, label_size, font, max_font_size)


def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


# TODO What to do when unclicking a palette
def press_release_palette(name, box, images):    
    global selected_palette_box

    #- Unclick this palette
    if selected_palette_box == box:
        box.configure(image=images[0])
        box.image = images[0]
        selected_palette_box = None
        # ?
        return
    
    #- Unclick other palette
    if selected_palette_box != None:
        selected_palette_box.configure(image=images[0])
        selected_palette_box.image = images[0]

    #- Click this palette
    box.configure(image=images[1])
    box.image = images[1]
    selected_palette_box = box

    #- Load palette
    load_palette(name)



def get_colored_image(data, size, overlay_image):
    #- Get colors
    x = data["xy"][0]
    y = data["xy"][1]
    bri = data["brightness"]
    rgb = huespec_xy_and_brightness_to_rgb((x, y), bri, False)
    
    #- Make a colored image
    image = Image.new('RGB', (size, size), (rgb["red"], rgb["green"], rgb["blue"]))

    #- Smooth corners with an overlay
    overlay_image = overlay_image.resize((size, size), Image.LANCZOS)
    image.paste(overlay_image, (0, 0), overlay_image)

    return ImageTk.PhotoImage(image=image)


def approximate_font_size(text_label, label_size, palette_font, max_font_size):
    #- Font resize depending on length of palette text
    original_font = font.Font(family=palette_font[0], size=palette_font[1])
    resizable_font = font.Font()
    resizable_font.configure(**original_font.configure())
    text_label.configure(font=resizable_font)

    text = text_label.cget("text")

    #- Grow the text until it is too large
    t_size = resizable_font.actual("size")
    while t_size < label_size:
        t_size += 1
        resizable_font.configure(size=t_size)

    #- Shrink it to fit
    while t_size > 1 and resizable_font.measure(text) > label_size:
        t_size -= 1
        resizable_font.configure(size=t_size)

    if t_size > max_font_size:
        resizable_font.configure(size=max_font_size)


# TODO
def palette_mouse_down():
    return


def load_palette(name):
    palette = get_all_palettes()[name]
    
    xy = {
        "x": palette["xy"][0], 
        "y": palette["xy"][1]
    }

    change_color(xy)
    change_brightness(palette["brightness"])

    print(palette)


# TODO Should account for different conversion types
def save_palette(palette_name, red, green, blue, brightness, conversion_type):
    data = get_data_file_dict()

    #- Already exists
    if palette_name in data["saved_palettes"]:
        return "Error"

    #! if huespec
    #! if colormath
    #! etc
    xy = colormath_rgb_to_xy(red, green, blue, target_illuminant="d65")
    
    palette = {
        "xy": [
            xy['x'],
            xy['y']
        ],
        "brightness": brightness,
        "conversion_type": conversion_type
    }

    #- Add palette and save to data file
    data["saved_palettes"][palette_name] = palette
    update_data_file(data)

    #! update palettes in window

    
def remove_palette(palette_name):
    data = get_data_file_dict()

    #- Remove palette and save to data file
    data["saved_palettes"].pop(palette_name)
    update_data_file(data)



###* Request related functions

##+ Get

def get_light_info():
    r = requests.get(url=f"{URL}/lights/{ben_light}", verify=False)
    return r.json()


def get_light_is_on():
    light_info = get_light_info()
    is_on = light_info['state']['on']
    return is_on


def get_xy_point():
    light_info = get_light_info()
    xy_point = light_info['state']['xy']
    return (xy_point[0], xy_point[1])


def get_brightness():
    light_info = get_light_info()
    brightness = light_info['state']['bri']
    return brightness


##+ Set

def request_state_change(data):
    d = json.dumps(data)
    r = requests.put(url=f"{URL}/lights/{ben_light}/state", data=d, verify=False)
    return r


def toggle_light():
    light_info = get_light_info()
    on_state = False if (light_info['state']['on']) else True
    d = {'on': on_state}
    return request_state_change(d)


def change_color(xy):
    d = {'xy': [
            xy['x'],
            xy['y']
        ]}
    return request_state_change(d)


def change_brightness(bri):
    d = {'bri': int(bri)}
    return request_state_change(d)


# TODO Should account for different conversion types
def color_slider_update(new_value, red, green, blue, val_label, release):
    val_label["text"] = round(float(new_value))

    if not release and not update_is_allowed():
        return

    #print(f"{red}, {green}, {blue}: {huespec_rgb_to_xy(red, green, blue, False)}")
    #change_color(huespec_rgb_to_xy(red, green, blue, False))
    #change_color(huespec_rgb_to_xy(red, green, blue, True))
    #change_color(colormath_rgb_to_xy(red, green, blue, target_illuminant="d55"))
    change_color(colormath_rgb_to_xy(red, green, blue, target_illuminant="d65")) # Best so far


def bri_slider_update(new_value, val_label, release):
    rounded_value = round(float(new_value))
    
    #- Update label
    val_label["text"] = rounded_value

    if not release and not update_is_allowed:
        return
    
    change_brightness(rounded_value)



###* Utility

def update_is_allowed():
    global t0
    
    t1 = time.perf_counter()
    td = t1 - t0

    if td > t_update_interval:
        t0 = t1
        return True
    return False


def get_data_file_dict():
    f = open(data_file_path, "r")
    data = json.load(f)
    return data


def update_data_file(data):
    with open(data_file_path, "w") as data_file:
        data_file.write(json.dumps(data, indent=4))



###* Testing

def between_test(white_transition_color):
    time.sleep(1)
    if white_transition_color:
        change_color({
            'x': 0.31271163465853535,
            'y': 0.3290082765355151
        })
    else:
        # Red transitionary color
        change_color(huespec_rgb_to_xy(255, 0, 0, True))
    time.sleep(0.2)


def test_rgb(by):
    colors = [
        [255, 0, 0], 
        [0, 255, 0], 
        [0, 0, 255]
    ]

    if by == "color":
        for color in colors:
            change_color(colormath_rgb_to_xy(color[0], color[1], color[2], "d55"))
            between_test(True)

            change_color(colormath_rgb_to_xy(color[0], color[1], color[2], "d65"))
            between_test(True)

            change_color(huespec_rgb_to_xy(color[0], color[1], color[2], True))
            between_test(True)

            change_color(huespec_rgb_to_xy(color[0], color[1], color[2], False))
            between_test(True)

    elif by == "type":
        for color in colors:
            change_color(colormath_rgb_to_xy(color[0], color[1], color[2], "d55"))
            between_test(True)
        
        for color in colors:
            change_color(colormath_rgb_to_xy(color[0], color[1], color[2], "d65"))
            between_test(True)

        for color in colors:
            change_color(huespec_rgb_to_xy(color[0], color[1], color[2], True))
            between_test(True)

        for color in colors:
            change_color(huespec_rgb_to_xy(color[0], color[1], color[2], False))
            between_test(True)


def test_whites():
    change_color(colormath_rgb_to_xy(255, 255, 255, "d55"))
    between_test(False)

    change_color(colormath_rgb_to_xy(255, 255, 255, "d65"))
    between_test(False)

    change_color(huespec_rgb_to_xy(255, 255, 255, True))
    between_test(False)

    change_color(huespec_rgb_to_xy(255, 255, 255, False))



###* Executes if run as a script

if __name__ == '__main__':

    ##+ Get and set light information

    #- Get light info
    light_info = get_light_info()

    #- Set color gamut
    set_color_gamut(light_info['capabilities']['control']['colorgamut'])

    #- Get light on state
    on_state = False if (light_info['state']['on']) else True
    
    #- Get brightness and saturation
    initial_bri = get_brightness()

    #- Get RGB from xy
    initial_rgb = huespec_xy_and_brightness_to_rgb(get_xy_point(), initial_bri, RGB_D65_conversion=False)


    ##+ Build GUI with initial state information
    
    create_gui(light_info, initial_rgb, initial_bri)



    #####! TESTING !#####
    #change_color(colormath_rgb_to_xy(255, 255, 255, "d55"))
    #change_color(colormath_rgb_to_xy(255, 255, 255, "d65"))
    #change_color(huespec_rgb_to_xy(255, 255, 255, True))
    #change_color(huespec_rgb_to_xy(255, 255, 255, False))
    #change_color(huespec_rgb_to_xy(255, 255, 255, False))
    #test_rgb("color")
    #test_rgb("type")
    #test_whites()
    #bri_slider_update(0, 0, True, True)
    #bri_slider_update(0, 0, True, False)
    #bri_slider_update(0, 0, False, True)
    #bri_slider_update(0, 0, False, False)
    #get_data_file()
    #test = save_palette("Big Crispy", 255, 0, 0, 155, "colormath_d65")
    #print(test)
    #remove_palette("King Crimson")
    #####! TESTING !#####






