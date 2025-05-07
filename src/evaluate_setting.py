import re
from typing import List

class ChannelSetting:
    def __init__(self, color: int, led: bool, mute: bool, tags: str):
        self.color: int = color
        self.led: bool = led
        self.mute: bool = mute
        self.tags: str = tags

def find_setting(point: int):
    if point == 0:
        return ChannelSetting(1, False, True, '""')
    if point == 1:
        return ChannelSetting(1, True, False, '"#D3"')
    if point == 2:
        return ChannelSetting(10, True, False, '"#D3"')
    if point == 3:
        return ChannelSetting(9, True, False, '"#D3"')
    if point == 4:
        return ChannelSetting(5, True, False, '"#D2"')
    return None

def change_settings(channel_setting: ChannelSetting, snap_channel: str) -> str:
    settings: list[str] = re.split(r'([,:{}])', snap_channel)

    for i, setting in enumerate(settings):
        if setting not in {'"col"', '"led"', '"mute"', '"tags"'}:
            continue
        if setting == '"col"':
            settings[i + 2] = str(channel_setting.color)
        elif setting == '"led"':
            settings[i + 2] = str(channel_setting.led).lower()
        elif setting == '"mute"':
            settings[i + 2] = str(channel_setting.mute).lower()
        elif setting == '"tags"':
            settings[i + 2] = channel_setting.tags

    return "".join(settings)


def create_snap_file(channel_settings: list[ChannelSetting], snap_contents: list[str]) -> str:
    snap_file: str = ""
    snap_file += snap_contents[0]
    snap_idx: int = 1
    for channel_setting in channel_settings:
        snap_file += snap_contents[snap_idx]
        snap_idx += 1
        changed_settings: str = change_settings(channel_setting, snap_contents[snap_idx])
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
