from PIL import Image, ImageTk



###* Palette data representation

class palette_wrapper: 
    def __init__(self, x, y, brightness, red, green, blue, conversion_type):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.red = red
        self.green = green
        self.blue = blue
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
