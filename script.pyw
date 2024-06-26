import tkinter as tk
from tkinter import ttk, font
from PIL import Image
import math

import sys
sys.path.insert(0, './modules')
from api_interface import *
from color_conversion import *
from utilities import *



###* GUI

#- Window
root = tk.Tk()
root.option_add("*font", "CascadiaMono 14")
w_width = 504
w_base_height = 400
is_resizable = False


#- Necessarily global widgets and other elements
p_title_entry_frame = None 
p_title_entry = tk.StringVar()
p_title_label = None
p_rename_button = p_save_button = p_duplicate_button = p_delete_button = p_confirm_button = p_cancel_button = None

r_scale = r_val_label = None
g_scale = g_val_label = None
b_scale = b_val_label = None
bri_scale = bri_val_label = None

palettes_frame = None
palette_box_icons = None
palettes_outer_frame = None

onoff_button = None


#- Current paletteless profile
paletteless_profile = None
palette_is_selected = False


#- Selected palette
selected_palette_box = None
selected_palette_name = None
selected_palette_overwritten = False


#- True for the first render
is_startup = True



###* GUI functions


def create_gui():

    ###* Window config
    root.geometry(f"{w_width}x{w_base_height}")
    root.resizable(is_resizable, is_resizable)
    root.title("HUE Lamp Color")
    root.iconbitmap("./images/icons/bulb.ico")


    ###* Content config

    ##+ Grid
    row_index = 0
    max_columns = 3


    ##+ Content images

    palette_modification_icon_size = 20
    slider_icon_size = 20
    on_off_icon_size = 40
    palette_box_size = 125
    palette_color_preview_size = 50

    palette_modification_icon_names = ['save', 'delete', 'duplicate', 'rename', 'confirm', 'cancel']
    palette_modification_icons = get_resized_tk_images(path="./images/icons/", image_names=palette_modification_icon_names, size=palette_modification_icon_size)

    slider_icon_names = ['red', 'green', 'blue', 'brightness']
    slider_icons = get_resized_tk_images(path="./images/icons/", image_names=slider_icon_names, size=slider_icon_size)

    on_off_icon_names = ['power_button_off', 'power_button_on']
    on_off_icons = get_resized_tk_images(path="./images/icons/", image_names=on_off_icon_names, size=on_off_icon_size)

    global palette_box_icons
    palette_box_names = ['palette_box', 'palette_box_pressed']
    palette_box_icons = get_resized_tk_images(path="./images/design/", image_names=palette_box_names, size=palette_box_size)
    palette_preview_overlay_image = Image.open("./images/design/overlay.png")


    ##+ Fonts
    palette_title_font = ("Cascadia Mono", 13)
    slider_font = ("Cascadia Mono", 12)
    palette_font = ("Cascadia Mono", 10)
    palette_max_font_size = 13


    ##+ Dimensions
    slider_length = 300
    slider_val_label_width = 3
    palette_text_label_size = palette_box_size - 30
    max_palette_rows = 2


    ##+ Padding

    p_title_frame_pady_l = 35
    p_title_frame_pady_s = 30
    p_title_buttons_padx_l = 15
    p_title_buttons_padx_s = 5

    slider_padx_s = 25
    slider_padx_l = 50
    slider_pady_s = 4
    slider_pady_l = 50

    palette_pady = 60
    palette_box_padding = 0

    on_off_pady = 50



    ###* Content

    ##+ Palette title/Entry, Save, and Delete
    row_index = make_palette_title_widget(row_index=row_index,
                                          max_columns=max_columns,
                                          title_font=palette_title_font,
                                          frame_pady_l=p_title_frame_pady_l,
                                          frame_pady_s=p_title_frame_pady_s,
                                          button_icons=palette_modification_icons,
                                          button_padx_l=p_title_buttons_padx_l,
                                          button_padx_s=p_title_buttons_padx_s)


    ##+ Sliders
    row_index = make_sliders_widget(row_index=row_index,
                                    icons=slider_icons,
                                    font=slider_font,
                                    length=slider_length,
                                    val_label_width=slider_val_label_width,
                                    padx_l=slider_padx_l,
                                    padx_s=slider_padx_s,
                                    pady_l=slider_pady_l,
                                    pady_s=slider_pady_s)

    
    ##+ Palettes
    palette_index = row_index
    root.bind("<<generate-palettes>>", lambda _event: make_palettes_widget(row_index=palette_index, 
                                                                           pady=palette_pady, 
                                                                           max_rows=max_palette_rows,
                                                                           max_columns=max_columns,
                                                                           box_size=palette_box_size, 
                                                                           box_padding=palette_box_padding,
                                                                           text_label_size=palette_text_label_size, 
                                                                           font=palette_font, 
                                                                           max_font_size=palette_max_font_size,
                                                                           preview_size=palette_color_preview_size, 
                                                                           preview_overlay_image=palette_preview_overlay_image))
    root.event_generate("<<generate-palettes>>")
    row_index += 1


    ##+ On/Off button
    row_index = make_on_off_button_widget(row_index=row_index, 
                                          max_columns=max_columns,
                                          icons=on_off_icons,
                                          pady=on_off_pady)


    ##+ Special events
    root.bind('<Escape>', lambda _event: on_quit())
    root.protocol('WM_DELETE_WINDOW', on_quit)

    root.bind('<Return>', lambda _event: press_light_button(onoff_button, on_off_icons["power_button_on"], on_off_icons["power_button_off"]))
    root.bind('<space>', lambda _event: press_light_button(onoff_button, on_off_icons["power_button_on"], on_off_icons["power_button_off"]))


    ##+ Finished generating the tkinter window
    global is_startup
    is_startup = False

    ##+ Run the tkinter window
    root.focus()
    root.mainloop()


def resize_window(height):
    root.geometry(f"{w_width}x{height}")


def on_quit():
    save_selected_palette()
    sys.exit()


def press_light_button(button, icon_on, icon_off):
    toggle_light()
    is_on = get_light_is_on()
    image = icon_on if is_on else icon_off
    button.configure(image=image)
    

def make_palette_title_widget(row_index, max_columns, title_font, frame_pady_l, frame_pady_s, button_icons, button_padx_l, button_padx_s):
    global p_title_entry, p_title_entry_frame, p_title_label, p_rename_button, p_save_button, p_duplicate_button, p_delete_button, p_confirm_button, p_cancel_button

    #- Frame Widget and it's placement
    p_title_frame = tk.Frame(root, borderwidth="0", relief="solid")
    p_title_frame.grid(row=row_index, column=0, columnspan=max_columns, pady=(frame_pady_l, frame_pady_s))

    #- Palette Entry
    p_title_entry_frame = tk.Frame(p_title_frame, borderwidth=1, relief=tk.SUNKEN, background="white")
    p_new_entry = tk.Entry(p_title_entry_frame, borderwidth=1, relief=tk.FLAT, textvariable=p_title_entry, font=title_font)

    #- Palette title
    p_title_label = tk.Label(p_title_frame, text="", font=title_font)

    #- Save/Duplicate/Delete icons
    p_buttons_frame = tk.Frame(p_title_frame, borderwidth="0", relief="solid")
    p_rename_button = tk.Button(p_buttons_frame, image=button_icons["rename"], border=0, cursor="hand2")
    p_save_button = tk.Button(p_buttons_frame, image=button_icons["save"], border=0, cursor="hand2")
    p_duplicate_button = tk.Button(p_buttons_frame, image=button_icons["duplicate"], border=0, cursor="hand2")
    p_delete_button = tk.Button(p_buttons_frame, image=button_icons["delete"], border=0, cursor="hand2")
    p_confirm_button = tk.Button(p_buttons_frame, image=button_icons["confirm"], border=0, cursor="hand2")
    p_cancel_button = tk.Button(p_buttons_frame, image=button_icons["cancel"], border=0, cursor="hand2")

    #- Placement within frame
    p_title_entry_frame.grid(row=0, column=0, padx=(0, 0))
    p_new_entry.pack(padx=(4, 0))
    p_title_label.grid(row=0, column=0, padx=(0, 0))

    p_buttons_frame.grid(row=0, column=1, padx=(0, 0))
    p_rename_button.grid(row=0, column=0, padx=(button_padx_l, 0))
    p_save_button.grid(row=0, column=1, padx=(button_padx_s, 0))
    p_duplicate_button.grid(row=0, column=2, padx=(button_padx_s, 0))
    p_delete_button.grid(row=0, column=3, padx=(button_padx_s, 0))

    p_confirm_button.grid(row=0, column=0, padx=(button_padx_l, 0))
    p_cancel_button.grid(row=0, column=1, padx=(button_padx_s, 0))

    #- Conditional rendering of selected palette and corresponding buttons
    if not palette_is_selected:
        p_title_label.grid_remove()
        p_rename_button.grid_remove()
        p_duplicate_button.grid_remove()
        p_delete_button.grid_remove()
    else:
        p_title_entry_frame.grid_remove()
    p_confirm_button.grid_remove()
    p_cancel_button.grid_remove()

    #- Events
    p_rename_button["command"] = lambda: toggle_palette_title_and_buttons(is_rename=True)
    p_save_button["command"] = lambda: save_palette(is_rename=False)
    p_duplicate_button["command"] = lambda: duplicate_palette()
    p_delete_button["command"] = lambda: remove_palette()
    p_confirm_button["command"] = lambda: rename_palette()
    p_cancel_button["command"] = lambda: toggle_palette_title_and_buttons(is_rename=False)

    return row_index + 1


def make_sliders_widget(row_index, icons, font, length, val_label_width, padx_l, padx_s, pady_l, pady_s):
    global r_scale, r_val_label
    global b_scale, b_val_label
    global g_scale, g_val_label
    global bri_scale, bri_val_label
    
    ##+ Red slider

    #- Widgets
    r_label = tk.Label(root, image=icons["red"])
    r_scale = ttk.Scale(root, from_=0, to=255, orient='horizontal', length=length, value=initial_rgb["red"])
    r_val_label = tk.Label(root, width=val_label_width, text=initial_rgb["red"], anchor="e", font=font)

    #- Placement
    r_label.grid(row=row_index, column=0, padx=(padx_l, 0), pady=(0, 0))
    r_scale.grid(row=row_index, column=1, padx=(padx_s, 0), pady=(0, 0))
    r_val_label.grid(row=row_index, column=2, padx=(padx_s, padx_l), pady=(0, 0))

    #- Events
    r_scale["command"] = lambda val: color_slider_update(val, r_scale["value"], g_scale["value"], b_scale["value"], r_val_label, release=False)
    r_scale.bind("<ButtonRelease-1>", lambda _event: color_slider_update(r_scale["value"], r_scale["value"], g_scale["value"], b_scale["value"], r_val_label, release=True))

    row_index += 1


    ##+ Green slider

    #- Widgets
    g_label = tk.Label(root, image=icons["green"])
    g_scale = ttk.Scale(root, from_=0, to=255, orient='horizontal', length=length, value=initial_rgb["green"])
    g_val_label = tk.Label(root, width=val_label_width, text=initial_rgb["green"], anchor="e", font=font)
    
    #- Placement
    g_label.grid(row=row_index, column=0, padx=(padx_l, 0), pady=(pady_s, 0))
    g_scale.grid(row=row_index, column=1, padx=(padx_s, 0), pady=(pady_s, 0))
    g_val_label.grid(row=row_index, column=2, padx=(padx_s, padx_l), pady=(pady_s, 0))
    
    #- Events
    g_scale["command"] = lambda val: color_slider_update(val, r_scale["value"], g_scale["value"], b_scale["value"], g_val_label, False)
    g_scale.bind("<ButtonRelease-1>", lambda _event: color_slider_update(g_scale["value"], r_scale["value"], g_scale["value"], b_scale["value"], g_val_label, release=True))

    row_index += 1


    ##+ Blue slider

    #- Widgets
    b_label = tk.Label(root, image=icons["blue"])
    b_scale = ttk.Scale(root, from_=0, to=255, orient='horizontal', length=length, value=initial_rgb["blue"])
    b_val_label = tk.Label(root, width=val_label_width, text=initial_rgb["blue"], anchor="e", font=font)

    #- Placement    
    b_label.grid(row=row_index, column=0, padx=(padx_l, 0), pady=(pady_s, 0))
    b_scale.grid(row=row_index, column=1, padx=(padx_s, 0), pady=(pady_s, 0))
    b_val_label.grid(row=row_index, column=2, padx=(padx_s, padx_l), pady=(pady_s, 0))

    #- Events
    b_scale["command"] = lambda val: color_slider_update(val, r_scale["value"], g_scale["value"], b_scale["value"], b_val_label, False)
    b_scale.bind("<ButtonRelease-1>", lambda _event: color_slider_update(b_scale["value"], r_scale["value"], g_scale["value"], b_scale["value"], b_val_label, release=True))    

    row_index += 1


    ##+ Brightness slider

    #- Widgets
    bri_label = tk.Label(root, image=icons["brightness"])
    bri_scale = ttk.Scale(root, from_=1, to=255, orient='horizontal', length=length, value=initial_bri)
    bri_val_label = tk.Label(root, width=val_label_width, text=initial_bri, anchor="e", font=font)

    #- Placement
    bri_label.grid(row=row_index, column=0, padx=(padx_l, 0), pady=(pady_l, 0))
    bri_scale.grid(row=row_index, column=1, padx=(padx_s, 0), pady=(pady_l, 0))
    bri_val_label.grid(row=row_index, column=2, padx=(padx_s, padx_l), pady=(pady_l, 0))

    #- Events
    bri_scale["command"] = lambda val: bri_slider_update(val, bri_val_label, release=False)
    bri_scale.bind("<ButtonRelease-1>", lambda _event: bri_slider_update(bri_scale["value"], bri_val_label, release=True))

    row_index += 1
    
    return row_index


def make_on_off_button_widget(row_index, max_columns, icons, pady):
    global onoff_button
    
    #- Widgets
    onoff_state = "on" if light_info['state']['on'] else "off"
    onoff_button = tk.Button(root, image=icons[f"power_button_{onoff_state}"], border=0, cursor="hand2")

    #- Placement
    onoff_button.grid(row=row_index, column=0, pady=(pady, 0), columnspan=max_columns)

    #- Events    
    onoff_button["command"] = lambda: press_light_button(onoff_button, icons["power_button_on"], icons["power_button_off"])

    return row_index + 1


def make_palettes_widget(row_index, pady, max_rows, max_columns, 
                         box_size, box_padding,
                         text_label_size, font, max_font_size,
                         preview_size, preview_overlay_image):
    
    global palettes_frame

    palettes = get_all_palettes()
    palettes_count = len(palettes)

    cols_per_row = math.ceil(palettes_count / max_rows) if max_rows > 0 else 0
    rows = max_rows if palettes_count >= max_rows else palettes_count
    
    palettes_exist = rows > 0
    frame_size = 0

    #- If there are palettes
    if palettes_exist:
        frame_size = (box_size + box_padding) * rows

        #- Resize entire window according to the frame and an offset for the scrollbar
        height = w_base_height + (frame_size + pady + 17)
        resize_window(height)
        
    #- If there are no palettes
    else: 
        resize_window(w_base_height)
        
    palettes_frame = make_palettes_frame(row=row_index, column=0, columnspan=max_columns, padx=0, pady=(pady, 0), frame_size=frame_size)
    if not palettes_exist: delete_palettes_widget()

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
                    color_preview_image=colored_preview_image)
        

def make_palettes_frame(row, column, columnspan, padx, pady, frame_size):
    global palettes_outer_frame

    palettes_outer_frame = tk.Frame(root, borderwidth=1)
    palettes_outer_frame.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)

    p_canvas = tk.Canvas(palettes_outer_frame, borderwidth=0, height=frame_size)
    p_frame = tk.Frame(p_canvas)
    p_scrollbar = tk.Scrollbar(palettes_outer_frame, orient="horizontal", command=p_canvas.xview)
    p_canvas.config(xscrollcommand=p_scrollbar.set)

    p_scrollbar.pack(side="bottom", fill="x")
    p_canvas.pack(side="top", fill="both", expand=True)
    p_canvas.create_window((0, 0), window=p_frame, anchor="w")

    p_frame.bind("<Configure>", lambda _event, canvas=p_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    return p_frame


def delete_palettes_widget():
    global palettes_outer_frame
    palettes_outer_frame.destroy()


def make_palette(frame, row, column, padding, name, label_size, font, max_font_size, color_preview_image):
    #- Contents
    box_frame = tk.Frame(frame, borderwidth=0)
    box = tk.Label(box_frame, image=palette_box_icons["palette_box"], border=0, cursor="hand2")
    text_label = tk.Label(box_frame, text=name, font=font, background="white", cursor="hand2")
    image_label = tk.Label(box_frame, image=color_preview_image, background="white", cursor="hand2")
    image_label.image = color_preview_image

    #- Content placement
    box_frame.grid(row=row, column=column, padx=(0, padding), pady=(0, padding))
    box.grid(row=0, column=0, rowspan=2)
    text_label.grid(row=0, column=0, sticky="N", pady=(20, 0))
    image_label.grid(row=1, column=0, sticky="S", pady=(0, 20))

    #- Events
    func = lambda _event: select_palette(name=name, box=box)
    box.bind("<ButtonRelease-1>", func)
    text_label.bind("<ButtonRelease-1>", func)
    image_label.bind("<ButtonRelease-1>", func)

    #- If this palette was selected when the widget was being made, we should select ourselves
    global selected_palette_name
    if selected_palette_name == name:
        select_palette(name=name, box=box)

    approximate_font_size(text_label, label_size, font, max_font_size)


def select_palette(name, box):
    global selected_palette_box, selected_palette_name, is_startup
    
    if not get_light_is_on() and not is_startup:
        return

    #- Unclick this palette / Load paletteless profile
    if selected_palette_box == box:
        if name != None:
            box.configure(image=palette_box_icons["palette_box"])
            box.image = palette_box_icons["palette_box"]

        global palette_is_selected
        palette_is_selected = False
        selected_palette_box = None

        load_paletteless_profile()
        return
    
    #- Unclick other palette
    if selected_palette_box != None and not selected_palette_overwritten:
        selected_palette_box.configure(image=palette_box_icons["palette_box"])
        selected_palette_box.image = palette_box_icons["palette_box"]

    #- Click this palette
    box.configure(image=palette_box_icons["palette_box_pressed"])
    box.image = palette_box_icons["palette_box_pressed"]
    selected_palette_box = box
    selected_palette_name = name

    #- Load palette
    load_palette(name)


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


def get_pre_selected_palette_name():
    return get_data_file_dict()["selected_palette"]


def save_selected_palette():
    data = get_data_file_dict()
    data["selected_palette"] = selected_palette_name if not selected_palette_name == None else ""
    update_data_file(data)


def get_all_palettes():
    return get_data_file_dict()["saved_palettes"]


def load_paletteless_profile():
    global paletteless_profile, palette_is_selected, selected_palette_name, selected_palette_box

    palette_is_selected = False
    selected_palette_name = selected_palette_box = None

    xy = {
        "x": paletteless_profile.x,
        "y": paletteless_profile.y
    }

    update_palette_title_gui(name=None)
    update_sliders_gui(red=paletteless_profile.red, green=paletteless_profile.green, blue=paletteless_profile.blue, brightness=paletteless_profile.brightness)

    change_color(xy)
    change_brightness(paletteless_profile.brightness)


def load_palette(name):
    ##+ Save the current color profile if the old one was not a palette

    global palette_is_selected
    if not palette_is_selected:
        old_xy = get_xy_point()
        old_bri = get_brightness()
        red, green, blue = r_scale.get(), g_scale.get(), b_scale.get()

        global paletteless_profile
        paletteless_profile = palette_wrapper(x=old_xy[0],
                                              y=old_xy[1],
                                              brightness=old_bri,
                                              red=red,
                                              green=green,
                                              blue=blue,
                                              conversion_type="colormath_d65")
    

    ##+ Load the selected palette

    palette = get_all_palettes()[name]
    
    xy = {
        "x": palette["xy"][0], 
        "y": palette["xy"][1]
    }

    palette_is_selected = True

    update_palette_title_gui(name)
    update_sliders_gui(palette["red"], palette["green"], palette["blue"], palette["brightness"])

    change_color(xy)
    change_brightness(palette["brightness"])


def update_palette_title_gui(name):
    global palette_is_selected

    toggle_palette_title_and_buttons(is_rename=False)

    if palette_is_selected:
        p_title_label.config(text=name)
    

def toggle_palette_title_and_buttons(is_rename):
    global palette_is_selected, p_rename_button, p_save_button, p_duplicate_button, p_delete_button, p_confirm_button, p_cancel_button

    if palette_is_selected and not is_rename:
        p_title_entry_frame.grid_remove()

        p_title_label.grid()
        p_rename_button.grid()
        p_save_button.grid()
        p_duplicate_button.grid()
        p_delete_button.grid()

        p_confirm_button.grid_remove()
        p_cancel_button.grid_remove()
    else:
        p_title_label.grid_remove()
        p_rename_button.grid_remove()
        p_duplicate_button.grid_remove()
        p_delete_button.grid_remove()

        p_title_entry_frame.grid()

        if is_rename:
            p_save_button.grid_remove()

            p_confirm_button.grid()
            p_cancel_button.grid()

        else:
            p_confirm_button.grid_remove()
            p_cancel_button.grid_remove()


def update_sliders_gui(red, green, blue, brightness):
    r_scale.set(red)
    r_val_label.config(text=red)

    g_scale.set(green)
    g_val_label.config(text=green)

    b_scale.set(blue)
    b_val_label.config(text=blue)

    bri_scale.set(brightness)
    bri_val_label.config(text=brightness)


def update_palettes_gui():
    #- Delete the palettes frame
    delete_palettes_widget()

    #- Clear the title entry
    p_title_entry.set("")

    #- Build a new palettes frame
    root.event_generate("<<generate-palettes>>")


def rename_palette():
    #- The old name
    global selected_palette_name

    global p_title_entry
    if p_title_entry.get() != "":
        #- Remove old palette from the file
        remove_palette_from_file(selected_palette_name)
        
        #- Save the new palette
        save_palette(is_rename=True)

    #- Update the title and buttons
    toggle_palette_title_and_buttons(is_rename=False)


def save_palette(is_rename):
    global selected_palette_name

    name = p_title_entry.get() if is_rename or not palette_is_selected else selected_palette_name
    #- Cancel if no given name
    if name == "":
        return

    #- Add the palette to the file and get a copy of the added palette
    added_palette = add_current_palette_to_file(name)

    update_state_after_palette_save(name, added_palette, is_rename_or_duplicate=True if is_rename else False)


def duplicate_palette():    
    global selected_palette_name

    name = f"{selected_palette_name} (Copy)"

    #- Add the duplicated palette to the file and get a copy of the palette
    duplicated_palette = add_current_palette_to_file(name)

    update_state_after_palette_save(name, duplicated_palette, is_rename_or_duplicate=True)
    

def add_current_palette_to_file(name):
    #- Gather selected values
    red, green, blue = r_scale.get(), g_scale.get(), b_scale.get()
    brightness = get_brightness()    
    xy = colormath_rgb_to_xy(red, green, blue, target_illuminant="d65")
    
    #- Make the palette
    palette = palette_wrapper(x=xy["x"],
                              y=xy["y"],
                              brightness=brightness,
                              red=red,
                              green=green,
                              blue=blue,
                              conversion_type="colormath_d65")

    #- Format the palette to be saved
    palette_dict = palette.get_formatted_dict()
    
    #- Existing data
    data = get_data_file_dict()
    
    #- If the palette already exists, indicate that we are overwriting it
    global selected_palette_overwritten
    if name in data["saved_palettes"]:
        selected_palette_overwritten = True

    #- Add palette to data file
    data["saved_palettes"][name] = palette_dict
    update_data_file(data)

    return palette


def update_state_after_palette_save(name, new_palette_profile, is_rename_or_duplicate):
    global selected_palette_name, selected_palette_box, selected_palette_overwritten, paletteless_profile

    #- Update the paletteless profile
    paletteless_profile = new_palette_profile

    #- Indicate the new palette should be selected on reloading of palettes
    selected_palette_name = name

    #- If the saved palette was due to duplication or renaming, the previous box should be nulled as it no longer exists
    if is_rename_or_duplicate:
        selected_palette_box = None

    update_palettes_gui()

    #- Reset overwritten indication after palettes regenerated
    selected_palette_overwritten = False


def remove_palette():
    name = p_title_label["text"]

    #- Remove palette and save to data file
    remove_palette_from_file(name)

    #- Update sliders and title to the paletteless profile
    load_paletteless_profile()

    #- Update palettes in window
    update_palettes_gui()


def remove_palette_from_file(name):
    data = get_data_file_dict()
    data["saved_palettes"].pop(name)
    update_data_file(data)


def color_slider_update(new_value, red, green, blue, val_label, release):
    val_label["text"] = round(float(new_value))

    if not release and not update_is_allowed():
        return

    change_color(colormath_rgb_to_xy(red, green, blue, target_illuminant="d65"))


def bri_slider_update(new_value, val_label, release):
    rounded_value = round(float(new_value))
    
    #- Update label
    val_label["text"] = rounded_value

    if not release and not update_is_allowed:
        return
    
    change_brightness(rounded_value)



###* Lamp testing

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
    xy = get_xy_point()
    initial_rgb = huespec_xy_and_brightness_to_rgb(xy, initial_bri, RGB_D65_conversion=False)

    #- Check that the data json file is formatted correctly and fix accordingly
    verify_json_data_format()

    #- Set the current profile
    pre_selected_palette_name = get_pre_selected_palette_name()
    if not pre_selected_palette_name == "":
        selected_palette_name = pre_selected_palette_name

    paletteless_profile = palette_wrapper(x=xy[0],
                                            y=xy[1],
                                            brightness=initial_bri,
                                            red=initial_rgb["red"],
                                            green=initial_rgb["green"],
                                            blue=initial_rgb["blue"],
                                            conversion_type="colormath_d65")


    ##+ Build GUI
    create_gui()
