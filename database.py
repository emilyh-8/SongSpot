import json
import os

def add_song(db, songs, song_id, title, hashes):
    if song_id in songs:
        return db, songs
    songs[song_id] = title
    for h, t in hashes:
        db.setdefault(h, []).append([song_id, t])
    return db, songs

# Saving db and songs to disk
def save_db(db, filepath="database.json"):
    with open(filepath, "w") as new_file:
        json.dump(db, new_file)
def save_songs(songs, filepath="songs.json"):
    with open(filepath, "w") as new_file:
        json.dump(songs, new_file)
def load_db(filepath="database.json"):
    if (os.path.exists(filepath)):
        with open(filepath, "r") as new_file:
            return json.load(new_file)
    return {}
def load_songs(filepath="songs.json"):
    if (os.path.exists(filepath)):
        with open(filepath, "r") as new_file:
            return json.load(new_file)
    return {}
