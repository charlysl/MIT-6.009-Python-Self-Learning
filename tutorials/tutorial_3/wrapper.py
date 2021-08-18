import lab, json, traceback
from importlib import reload
reload(lab) # this forces the student code to be reloaded when page is refreshed

def next(input_data):
    print("wrapper.py: calling next_song with input_data:", input_data, flush=True)
    result = lab.next_song(input_data["likes"], input_data["dislikes"], music_genome)
    print("wrapper.py: next_song returning:", result, flush=True)
    return result

music_genome = []
def init():
    global music_genome
    music_genome = []
    with open('resources/music.json') as data_file:
        music_file = json.load(data_file)
        for track in music_file:
            music_genome.append(track["genes"])
    print("wrapper.py: after init, music_genome length:", len(music_genome), flush=True)

init()

