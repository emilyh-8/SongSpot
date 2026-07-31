# TuneRecog — Audio Fingerprinting ("Shazam")

A from-scratch implementation of the algorithm behind "Shazam," identifying a song
from a short and/or noisy audio clip by matching acoustic "fingerprints"
against a database of known songs.

## Why This Project

From my background as a pianist, I wanted to understand how audio recognition
actually works, rather than calling an API. This project touches signal processing
(spectrograms, FFT), algorithm design (local-peak-pair hashing), and search
(inverted indices for quick lookup). This is all built from first, basic principles.

## How It Works

1. **Waveform** — Load the audio as a plain array of samples (air pressure
   over time) using `librosa` library.
2. **Spectrogram** — Convert the waveform into a 2D map of which frequencies
   are loud at which points in time, via a Short-Time Fourier Transform
   (`librosa.stft`), converted to decibels for a perceptually meaningful scale.
3. **Peak finding** — Find the loudest, most distinctive points in the
   spectrogram using `scipy.ndimage.maximum_filter`. These survive noise and
   compression better than average.
4. **Hashing** — Pair up peaks that are close together in time and hash each
   pair (`freq1, freq2, time_delta`) into a compact fingerprint. A single
   peak on its own isn't unique enough, as compared to a *pair* with a specific
   frequency/time relationship.
5. **Storage** — Fingerprints are stored in an inverted index: a JSON
   dictionary mapping `hash -> [[song_id, time_offset], ...]`, so any
   fingerprint can be looked up instantly, regardless of how many songs are
   in the database.
6. **Matching** — To identify a clip, fingerprint it the same way, then look
   up each fingerprint in the database. For every match, compute the time
   offset between where it occurred in the clip vs. in the original song. A
   real match produces a strong spike of hashes agreeing on the *same*
   offset; coincidental matches scatter randomly across many offsets.

## Note on Song Database

No audio files or pre-built fingerprint data are included in this repo to avoid 
distributing copyrighted audio and to keep the repo small. To try this yourself, 
add your own `.mp3` or `.wav` files to `songs/` and run `build_database.py` to 
generate the database locally.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   
pip install -r requirements.txt
```

## Usage

1. Add a collection of songs (`.mp3` or `.wav` or `.mov`) to the `songs/` folder to create the song database.
2. Build the fingerprint database:
   ```bash
   python3 build_database.py songs/
   ```
3. Trim a short clip (5–10 seconds) from one of those songs.
4. Identify it:
   ```bash
   python3 identify.py test_clip.wav
   ```

## Example Output

```
Clip has 46067 fingerprints
Top matches:
  chestpain (confidence: 10930)
  sorry (confidence: 20)
  sweetboy (confidence: 11)
```

The evident gap between the top score and the rest is the signal that
confirms a match.

## What I Learned

- Why pairing local peaks (instead of hashing single peaks) is what makes the
  fingerprint distinctive enough to be reliable. Single peaks collide
  across unrelated songs constantly, while a pair with a specific frequency/time
  relationship rarely does.
- Why matching only works if you check for a consistent *offset* across
  many hashes, rather than just counting total matching hashes. Random
  coincidental matches between unrelated songs scatter across offsets,
  while a real match concentrates on one.
- Why an inverted index (hash → songs) is the right data structure (instant lookup),
  instead of storing hashes per song (scanning every song in the database for every query).
- Re-running `build_database.py` without a duplicate check silently
  corrupted the database (song count kept growing on repeat runs). Fixed by
  checking whether a song's title was already in the database before
  re-fingerprinting it.
- Tested how clip length affects confidence score. While the gap between the correct and
  incorrect songs still remained apparent, trying a shorter clip resulted in far
  fewer total fingerprints, thus fewer peaks and hash pairs. Although this highlights
  a tradeoff in the algorithm, shorter clips are more realistic for a use case.

## Possible Extensions

- Record directly from the microphone instead of using a pre-saved clip
- Swap the JSON database for SQLite so it scales past a few hundred songs
- Add a simple web UI
- Measure accuracy/false-positive rate systematically across many test clips
- Speed up matching with a proper database instead of a Python dict lookup
- Query-by-humming -- recognizing a hummed or sung melody in addition to exact
  audio clips. This requires a different approach than fingerprinting, such as
  extracting pitch contour with `librosa.pyin`, as a hum's produced spectrogram 
  will not precisely match the audio.

## Tech

Python, librosa, NumPy, SciPy
