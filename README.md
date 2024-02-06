# Desktop Hue lamp app
This application provides a neat application similar to the mobile app provided for managing Hue lamps.

### Features
* Toggle lamp on/off
* Change color and brigthness
* Palettes
    * Save color and brightness as a palette
    * Remember selected palette
    * Easy selection of palettes provided by an orderly menu
    * Rename palette
    * Update color and brightness
    * Make copy
    * Delete palette
    * Fast selection of palettes
* Additional settings in code
    * Change font
    * Change window dimensions
    * Toggle resizable

### Used Icons
* [Iconarchive](https://iconarchive.com)
    * [Window bulb Icon](https://iconarchive.com/show/small-n-flat-icons-by-paomedia/light-bulb-icon.html)
* [Icons8](https://icons8.com)
    * [Red/Green/Blue Icon (Modified)](https://icons8.com/icon/FBrumXCNzSiq/c)
* [Flaticon](https://www.flaticon.com)
    * [Saturation Icon](https://www.flaticon.com/free-icon/saturation_7902002?term=saturation&page=1&position=13&origin=tag&related_id=7902002)
    * [Brightness Icon](https://www.flaticon.com/free-icon/sun_606795?term=brightness&page=1&position=4&origin=tag&related_id=606795)
    * [On/Off bulb Icon (Modified)](https://www.flaticon.com/free-icon/lightbulb_3176369)
    * [Save Icon](https://www.flaticon.com/free-icon/diskette_2874050?term=save&page=1&position=6&origin=search&related_id=2874050)
    * [Delete Icon](https://www.flaticon.com/free-icon/bin_484611)
    * [Duplicate Icon](https://www.flaticon.com/free-icon/copy_5859288?term=duplicate&page=1&position=34&origin=search&related_id=5859288)
    * [Rename](https://www.flaticon.com/free-icon/edit_3394447?term=rename&page=1&position=10&origin=search&related_id=3394447)
    * [Confirm](https://www.flaticon.com/free-icon/check_9778609?term=confirm&page=1&position=87&origin=search&related_id=9778609)
    * [Cancel (Modified)](https://www.flaticon.com/free-icon/check_9778609?term=confirm&page=1&position=87&origin=search&related_id=9778609)



### Setup

#### credentials.json (in root)
{
    "devicetype": "app_name#device_name",
    "username": "username",     (generated from HUE api})
    "ip": "192.168.x.x"         (ip of the device running the app)
}