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
        
