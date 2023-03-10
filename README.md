# Notes
* Hue lamps use CIE 1931 color space (Illuminant d65?)
* [Converting between RGB and XY according to HUE](https://github.com/johnciech/PhilipsHueSDK/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md) [(alternate)](https://github.com/benknight/hue-python-rgb-converter/blob/master/rgbxy/__init__.py)

# TODO
* REVAMP GUI TO CLASS
* Imperfect colors (Colormath d65 seems to be the best so far)
    * Different color options
    * Cutoff at certain green value? Example switch from huespec to colormath at green > 150
* Saving a palette must keep in mind which conversion model was used
* Resize text to always fit palette box
    * At characters > x (and more than one word) break line
* Make the entire palette box clickable (prob bind command to button-1-down event)
    * Supress the button movement since it is the only part of the widget doing it
    * On hover change the mouse pointer
* Palettes could include the ones saved in the HUE app as well
* Focus red/blue or green icons (corresponding to what conversion model is being used)
* Rework xy-point tuple


# Icons
* [Window bulb Icon](https://iconarchive.com/show/small-n-flat-icons-by-paomedia/light-bulb-icon.html)
* [Red/Green/Blue Icon](https://icons8.com/icon/FBrumXCNzSiq/c)
* [Saturation Icon](https://www.flaticon.com/free-icon/saturation_7902002?term=saturation&page=1&position=13&origin=tag&related_id=7902002)
* [Brightness Icon](https://www.flaticon.com/free-icon/sun_606795?term=brightness&page=1&position=4&origin=tag&related_id=606795)
* [On/Off bulb Icon (Modified by me)](https://www.flaticon.com/free-icon/lightbulb_3176369)