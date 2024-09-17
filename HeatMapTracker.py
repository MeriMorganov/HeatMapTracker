import json
import os
from PlayerMatchData import PlayerMatchData


def load_heatmap_data_from_file(filename):
    base_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    file_path = os.path.join(base_dir, 'data', filename)

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return PlayerMatchData(**data)

heatmap_data = load_heatmap_data_from_file('playerMatchData_001.json')


print(heatmap_data.levelMap.width)