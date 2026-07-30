from fingerprint import fingerprint_file
from database import load_db, load_songs
from collections import defaultdict

def identify(filepath):
    db = load_db()
    songs = load_songs()

    clip_hashes = fingerprint_file(filepath)
    print(f"Clip has {len(clip_hashes)} fingerprints")

    matches = defaultdict(lambda: defaultdict(int))

    for h, clip_time in clip_hashes:
        if h in db:
            for song_id, song_time in db[h]:
                offset = song_time - clip_time
                matches[song_id][offset] += 1

    scores = {}
    for song_id, offsets in matches.items():
        best_offset_count = max(offsets.values())
        scores[song_id] = best_offset_count

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for song_id, score in ranked:
        title = songs[song_id]
        print(f"{title} (confidence: {score})")

identify("songs/ilove.mov")