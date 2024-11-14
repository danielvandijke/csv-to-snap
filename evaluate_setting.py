import re
from typing import List


def find_setting(point):
    ch_col, ch_led, ch_mute, ch_tags = '1', 'false', 'true', ''
    if point == '':
        ch_col = '1'
        ch_led = 'false'
        ch_mute = 'true'
        ch_tags = '""'
    elif point == '1.00':
        ch_col = '3'
        ch_led = 'true'
        ch_mute = 'false'
        ch_tags = '"#D3"'
    elif point == '2.00':
        ch_col = '10'
        ch_led = 'true'
        ch_mute = 'false'
        ch_tags = '"#D3"'
    elif point == '3.00':
        ch_col = '9'
        ch_led = 'true'
        ch_mute = 'false'
        ch_tags = '"#D3"'
    elif point == '4.00':
        ch_col = '5'
        ch_led = 'true'
        ch_mute = 'false'
        ch_tags = '"#D2"'
    return ch_col, ch_led, ch_mute, ch_tags


def change_settings(channel_setting: tuple, snap_channel: str):
    ch_col, ch_led, ch_mute, ch_tags = channel_setting[0], channel_setting[1], channel_setting[2], channel_setting[3]
    settings = re.split(r'([,:{}])', snap_channel)

    for i, setting in enumerate(settings):
        if setting not in {'"col"', '"led"', '"mute"', '"tags"'}:
            continue
        if setting == '"col"':
            settings[i + 2] = ch_col
        elif setting == '"led"':
            settings[i + 2] = ch_led
        elif setting == '"mute"':
            settings[i + 2] = ch_mute
        elif setting == '"tags"':
            settings[i + 2] = ch_tags

    return "".join(settings)


def create_snap_file(channel_settings: List, snap_contents: List):
    snap_file = ""
    snap_file += snap_contents[0]
    snap_idx = 1
    for channel_setting in channel_settings:
        snap_file += snap_contents[snap_idx]
        snap_idx += 1
        changed_settings = change_settings(channel_setting, snap_contents[snap_idx])
        snap_idx += 1
        snap_file += changed_settings
    for snap_content in snap_contents[snap_idx:]:
        snap_file += snap_content

    return snap_file


def get_snap_content(path):
    try:
        with open(path, 'r') as file:
            snap_content = file.read()
        return snap_content
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except IOError:
        print(f"Error: An error occurred while reading the file '{path}'")


def export_file(snap_content: str, file_name: str):
    file_name += ".snap"
    file_path = re.sub(r"[:]", ",", file_name)
    with open(file_path, "w") as file:
        file.write(snap_content)
