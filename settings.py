import json

difficulty_list = ['EASY', 'MEDIUM', 'HARD']
sound_list = ['NO', 'LOW', 'MEDIUM', 'HIGH']
difficulty = 'EASY'
sound = 'LOW'


def get_diff_index(): return difficulty_list.index(difficulty)
def get_sound_index(): return sound_list.index(sound)

def save_settings(default=False):
    if default:
        data = {'difficulty': 'EASY',
                'sound': 'LOW'}
    else:
        data = {'difficulty': difficulty,
                'sound': sound}

    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)


try:
    read_file = open("data_file.json", "r")
    data = json.load(read_file)
    difficulty = data['difficulty']
    sound = data['sound']
except FileNotFoundError:
    save_settings(True)
else:
    read_file.close()




#save_settings()
