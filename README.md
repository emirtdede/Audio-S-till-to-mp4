````markdown
# audio-still-to-mp4

A simple Python script that combines an **audio file + a still image** into a **YouTube-safe 1080p MP4 video**.  
It leverages FFmpeg, preserving aspect ratio with padding, encodes to **yuv420p**, and uses **+faststart** for smooth streaming.

---

## Features

- 1920×1080 canvas with **aspect ratio preserved + padding** (scale+pad filter)  
- Fixed **30 fps** frame rate  
- Video: `libx264`, `-tune stillimage`, `-profile high`, `-level 4.1`, `-pix_fmt yuv420p`  
- Audio: `AAC 192k`, `48 kHz`  
- **+faststart** for fast playback on streaming platforms  
- Validates input paths and provides clear error messages  
- No extra Python dependencies (only standard library + FFmpeg required)  

---

## Requirements

- **Python 3.8+**  
- **FFmpeg** must be installed and available in your system PATH  

Check if FFmpeg is installed:
```bash
ffmpeg -version
````

### FFmpeg Installation

* **Windows:** `winget install Gyan.FFmpeg` or `choco install ffmpeg`
* **macOS:** `brew install ffmpeg`
* **Debian/Ubuntu:** `sudo apt update && sudo apt install ffmpeg`
* **Fedora/RHEL:** `sudo dnf install ffmpeg`

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/audio-still-to-mp4.git
cd audio-still-to-mp4
```

(Optional) create a virtual environment:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

No additional Python packages are required.

---

## Usage

### 1) As a function

Inside `video_maker.py`, call:

```python
from video_maker import wav_img_to_mp4_youtube

wav_img_to_mp4_youtube("audio.wav", "cover.png", "output.mp4")
```

* `audio_path`: Input audio (wav/mp3/etc.)
* `image_path`: Input still image (png/jpg/etc.)
* `output_path`: Optional, defaults to `<audio_filename>_podcast.mp4`

---

### 2) Run directly

The script has an example block:

```bash
python video_maker.py
```

This expects `ses.wav` + `resim.png` and outputs `video.mp4`.

> Tip: if file paths include spaces or special characters, wrap them in quotes.

---

### 3) Optional CLI version

You can create a `cli.py` wrapper to pass arguments from the command line. Example:

```bash
python cli.py input.wav cover.png -o output.mp4
```

---

## Output Details

* **Scaling & padding filter:**

  ```
  scale=1920:1080:force_original_aspect_ratio=decrease,
  pad=1920:1080:(ow-iw)/2:(oh-ih)/2
  ```

  Ensures the image fits the 1080p canvas without distortion.
* **Compatibility:** `-pix_fmt yuv420p` ensures the MP4 works on YouTube, Instagram, Twitter, etc.
* **Streaming:** `-movflags +faststart` places the moov atom at the beginning of the file for faster web playback.

---

## Common Issues

* **"ERROR: ffmpeg not found."**
  FFmpeg is not installed or not in PATH. Install it and open a new terminal.

* **"Audio/Image file not found"**
  Check the file paths and extensions. Wrap paths with quotes if needed.

* **"FFmpeg returned error code"**
  Possible reasons: corrupted input, insufficient disk space, or codec issues. Run the FFmpeg command manually to inspect logs.

---

## Tips

* For **higher quality**, you may add `-crf 18` (but static images gain little).
* For **4K output**, change scale/pad to `3840x2160` and update the level.
* For **smaller audio size**, reduce bitrate (`-b:a 128k`).

---

## License

This project is licensed under the [MIT License](./LICENSE).

---

## Contributing

Pull requests and issues are welcome. Keep changes focused and minimal.

```

---

Would you like me to also prepare the **LICENSE** and **.gitignore** in the same copy-paste format so you can drop them into your repo together with this README?
```
