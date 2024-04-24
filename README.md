# Hue lamp app

## Description
This Python app controls a HUE lamp through the HUE Bridge API, utilizing a Tkinter GUI. 

#### Features
* Toggle lamp on/off
* Change color and brigthness
* Palettes
    * Easy selection provided by an orderly menu
    * Save color and brightness
    * Update color and brightness
    * Rename
    * Make copy
    * Delete
    * Remember selection
* Additional settings in code
    * Change font
    * Change window dimensions
    * Toggle resizability


## Installation instructions
***Note*** This project is intended for personal use, anyone who wants to try this out 
for themselves will have to set up their own local HUE bridge API.

1. **Clone the repository**
```
git clone https://github.com/Benhan11/hue-lamp-app.git
```

2. **Create an authorized HUE Bridge API user and store it as a `credentials.json` file, [example](https://developers.meethue.com/develop/get-started-2/)**
The file should look like this:

```json
{
    "devicetype": "app_name#device_name",
    "username": "username",
    "ip": "192.168.x.x"
}
```

3. **Install dependencies**
```
pip install pillow==9.4.0
pip install requests==2.28.2
pip install urllib3==1.26.14
pip install colormath==3.0.0
```

## Usage
Set `light_num` to its corresponding HUE Bridge number in `modules/api_interface.py`

Run the executable `script.pyw`

## Dependencies
- pillow (v9.4.0)
- requests (v2.28.2)
- urllib3 (v1.26.14)
- colormath (v3.0.0)

## Icon attribution
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
