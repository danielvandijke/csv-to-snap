import csv
import re
from evaluate_setting import find_setting, create_snap_file, export_file, get_snap_content

snap_template_path = input("Enter the full path to the template .snap file: ")
snap_content = get_snap_content(snap_template_path)

file_path = input("Enter the full path of the csv: ")

scene_settings = []
scene_names = []
with open(file_path, encoding='utf-8-sig', mode="r", newline="") as file:
    csv_reader = csv.reader(file)

    i = 1
    for row in csv_reader:
        channel_settings = []
        scene_names.append(row[0])
        i += 1
        for cell in row[1:]:
            setting = find_setting(cell)
            channel_settings.append(setting)
        scene_settings.append(channel_settings)

delimiter = r'(:{"in":{"set":{"srcauto":)'
snap_contents = re.split(delimiter, snap_content)

for i, scene_setting in enumerate(scene_settings):
    snap_file = create_snap_file(scene_setting, snap_contents)
    export_file(snap_file, scene_names[i])

print("thanks for using this application")
