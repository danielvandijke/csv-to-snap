import csv
import re
from evaluate_setting import find_setting, create_snap_file, export_file, get_snap_content, ChannelSetting
from csv import reader

def to_num(cell) -> int:
    try:
        return int(float(cell))
    except (ValueError, TypeError):
        return 0

def str_to_bool(s: str) -> bool:
    return s.strip().lower() in ("true", "1", "yes", "on")

def get_channel_settings(cell_values: list[str]) -> list[ChannelSetting]:
    channel_settings: list[ChannelSetting] = []
    for cell_value in cell_values:
        channel_setting: ChannelSetting = setting_conversion[to_num(cell_value)]
        channel_settings.append(channel_setting)
    return channel_settings

def parse_settings(path) -> dict[int, ChannelSetting]:
    setting_conversion: dict[int, ChannelSetting] = {}
    with open(path, encoding='utf-8-sig', mode="r", newline="") as file:
        csv_reader: reader = csv.reader(file)
        for row in csv_reader:
            point = int(float(row[0]))
            configs = ChannelSetting(int(float(row[1])), str_to_bool(row[2]), str_to_bool(row[3]), row[4])
            setting_conversion[point] = configs
    return setting_conversion

snap_template_path: str = input("Enter the full path to the template .snap file: ")
snap_content: str = get_snap_content(snap_template_path)
file_path: str = input("Enter the full path of the csv: ")
settings_path: str = input("Enter the full path of the settings file: ")
setting_conversion: dict[int, ChannelSetting] = parse_settings(settings_path)
scene_settings: list[list[ChannelSetting]] = []
scene_names: list[str] = []


with open(file_path, encoding='utf-8-sig', mode="r", newline="") as file:
    csv_reader: reader = csv.reader(file)
    for row in csv_reader:
        scene_names.append(row[0])
        scene_settings.append(get_channel_settings(row[1:]))

delimiter: str = r'(:{"in":{"set":{"srcauto":)'
snap_contents: list[str] = re.split(delimiter, snap_content)

for i, scene_setting in enumerate(scene_settings):
    snap_file: str = create_snap_file(scene_setting, snap_contents)
    export_file(snap_file, scene_names[i])

print("thanks for using this application")
