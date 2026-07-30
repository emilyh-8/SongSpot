
import os
from fingerprint import fingerprint_file
from database import load_db, load_songs, save_db, save_songs, add_song

def main(folder):
    db = load_db()
    songs = load_songs()

    filenames = os.listdir(folder)

    for filename in filenames:
        title = os.path.splitext(filename)[0]

        if title in songs.values():
            print(f"Skipping {title} - already fingerprinted")
            continue
        
        filepath = os.path.join(folder, filename)
        song_id = str(len(songs) + 1)
        print(f"Fingerprinting: {title}...")
        hashes = fingerprint_file(filepath)
        db, songs = add_song(db, songs, song_id, title, hashes)
        print(f" -> {len(hashes)} fingerprints")

    save_db(db)
    save_songs(songs)
    print(f"Done. {len(songs)} songs, {len(db)} unique fingerprints.")

if __name__ == "__main__":
    main("songs")