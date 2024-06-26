from PIL import Image, ImageTk
import json



###* Palette data representation

class palette_wrapper: 
    def __init__(self, x, y, brightness, red, green, blue, conversion_type):
        self.x = x
        self.y = y
        self.brightness = int(brightness)
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)
        self.conversion_type = conversion_type

    def get_formatted_dict(self):
        return self.make_formatted_dict(self.x,
                                        self.y,
                                        self.brightness,
                                        self.red,
                                        self.green,
                                        self.blue,
                                        self.conversion_type)
    
    @staticmethod
    def make_formatted_dict(x, y, brightness, red, green, blue, conversion_type):
        return {
            "xy": [
                x,
                y
            ],
            "brightness": int(brightness),
            "red": int(red),
            "green": int(green),
            "blue": int(blue),
            "conversion_type": conversion_type
        }



###* Helper functions

##+ Images

def get_resized_tk_images(path, image_names, size):
    resized_images = {}
    for image_name in image_names:
        img = Image.open(f"{path}{image_name}.png")
        img = img.resize((size, size), Image.LANCZOS)
        img_resized = ImageTk.PhotoImage(img)
        resized_images[image_name] = img_resized

    return resized_images


def get_colored_image(data, size, overlay_image):
    #- Get colors
    x = data["xy"][0]
    y = data["xy"][1]
    bri = data["brightness"]
    red, green, blue = data["red"], data["green"], data["blue"]
    
    #- Make a colored image
    image = Image.new('RGB', (size, size), (red, green, blue))

    #- Smooth corners with an overlay
    overlay_image = overlay_image.resize((size, size), Image.LANCZOS)
    image.paste(overlay_image, (0, 0), overlay_image)

    return ImageTk.PhotoImage(image=image)


##+ Data file structure

#- Data file path
data_file_path = 'data/data.json'


def make_data_file():
    with open(data_file_path, "w") as outfile:
            json.dump({}, outfile)


def get_data_file_dict():
    f = open(data_file_path, "r")
    data = json.load(f)
    return data


def update_data_file(data):
    with open(data_file_path, "w") as data_file:
        data_file.write(json.dumps(data, indent=4))


def verify_json_data_format():
    data_file_dict = None
    has_selected_palette = has_saved_palettes = False

    #- Check if the file exists or if the initial curcly brackets exist
    try:
        data_file_dict = get_data_file_dict()
    except:
        make_data_file()
        data_file_dict = get_data_file_dict()

    try:
        data_file_dict["selected_palette"]
        has_selected_palette = True
    except:
        has_selected_palette = False

    try:
        data_file_dict["saved_palettes"]
        has_saved_palettes = True
    except:
        has_saved_palettes = False

    if not has_selected_palette:
        data_file_dict.update({"selected_palette": ""})
    if not has_saved_palettes:
        data_file_dict.update({"saved_palettes": {}})

    update_data_file(data_file_dict)