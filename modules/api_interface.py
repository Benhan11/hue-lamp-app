import requests
import urllib3
import json
import time



###* Config

#- Disable unsafe request related warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#- Slider update rate-limiting
t0 = time.perf_counter()
allowed_updates_per_second = 5
t_update_interval = 1 / allowed_updates_per_second

#- The light
light_num = 10

#- HUE bridge username
f = open('credentials.json')
credentials_json = json.load(f)
username = credentials_json['username']
ip = credentials_json['ip']
f.close()

#- API-endpoint
URL = f"https://{ip}/api/{username}"

#- Light on-state
on_state = False

#- Data file path
data_file_path = 'data/data.json'



###* Requests

##+ Get

def get_light_info():
    r = requests.get(url=f"{URL}/lights/{light_num}", verify=False)
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
    r = requests.put(url=f"{URL}/lights/{light_num}/state", data=d, verify=False)
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



###* Utility

def update_is_allowed():
    global t0
    
    t1 = time.perf_counter()
    td = t1 - t0

    if td > t_update_interval:
        t0 = t1
        return True
    return False


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
        
