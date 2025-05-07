import csv
import re
from evaluate_setting import find_setting, create_snap_file, export_file, get_snap_content, ChannelSetting
from csv import reader

def to_num(cell) -> int:
    try:
        return int(float(cell))
    except (ValueError, TypeError):
        return 0

snap_template_path: str = input("Enter the full path to the template .snap file: ")
snap_content: str = get_snap_content(snap_template_path)

file_path: str = input("Enter the full path of the csv: ")

scene_settings: list[list[ChannelSetting]] = []
scene_names: list[str] = []
with open(file_path, encoding='utf-8-sig', mode="r", newline="") as file:
    csv_reader: reader = csv.reader(file)

    i: int = 1
    for row in csv_reader:
        channel_settings: list = []
        scene_names.append(row[0])
        i += 1
        for cell in row[1:]:
            channel_setting: ChannelSetting = find_setting(to_num(cell))
            channel_settings.append(channel_setting)
        scene_settings.append(channel_settings)

delimiter: str = r'(:{"in":{"set":{"srcauto":)'
snap_contents: list[str] = re.split(delimiter, snap_content)

for i, scene_setting in enumerate(scene_settings):
    snap_file: str = create_snap_file(scene_setting, snap_contents)
    export_file(snap_file, scene_names[i])

print("thanks for using this application")
