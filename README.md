# Notes
* Hue lamps use CIE 1931 color space (Illuminant d65?)
* [Converting between RGB and XY according to HUE](https://github.com/johnciech/PhilipsHueSDK/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md) [(alternate)](https://github.com/benknight/hue-python-rgb-converter/blob/master/rgbxy/__init__.py)

# TODO
* Encapsulate global buttons in a structure
* Imperfect colors (Colormath d65 seems to be the best so far)
    * Different color options
    * Cutoff at certain green value? Example switch from huespec to colormath at green > 150
* Saving a palette must keep in mind which conversion model was used
* Palette name characters > x (and more than one word) break line
* Palettes could include the ones saved in the HUE app as well
* Focus red/blue or green icons (corresponding to what conversion model is being used)
* Rework xy-point tuple
* Clean boiler plate RGB-slider code


# Icons
* [Window bulb Icon](https://iconarchive.com/show/small-n-flat-icons-by-paomedia/light-bulb-icon.html)
* [Red/Green/Blue Icon](https://icons8.com/icon/FBrumXCNzSiq/c)
* [Saturation Icon](https://www.flaticon.com/free-icon/saturation_7902002?term=saturation&page=1&position=13&origin=tag&related_id=7902002)
* [Brightness Icon](https://www.flaticon.com/free-icon/sun_606795?term=brightness&page=1&position=4&origin=tag&related_id=606795)
* [On/Off bulb Icon (Modified by me)](https://www.flaticon.com/free-icon/lightbulb_3176369)
* [Save Icon](https://www.flaticon.com/free-icon/diskette_2874050?term=save&page=1&position=6&origin=search&related_id=2874050)
* [Delete Icon](https://www.flaticon.com/free-icon/delete_565491?term=delete&page=1&position=11&origin=search&related_id=565491)
* [Duplicate Icon](https://www.flaticon.com/free-icon/copy_5859288?term=duplicate&page=1&position=34&origin=search&related_id=5859288)
* [Rename](https://www.flaticon.com/free-icon/edit_3394447?term=rename&page=1&position=10&origin=search&related_id=3394447)
* [Confirm](https://www.flaticon.com/free-icon/check_9778609?term=confirm&page=1&position=87&origin=search&related_id=9778609)
* [Cancel (Modified by me)](https://www.flaticon.com/free-icon/check_9778609?term=confirm&page=1&position=87&origin=search&related_id=9778609)