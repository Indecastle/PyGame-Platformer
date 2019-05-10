difficulty = 'EASY'
sound = 'LOW'

import json

try:
    read_file = open("data_file.json", "r")
    data = json.load(read_file)
    difficulty = data['difficulty']
    sound = data['sound']
except:
    read_file.close()
else:
    read_file.close()

def save_settings():
    data = {'difficulty' : difficulty,
            'sound' : sound}

    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

save_settings()
