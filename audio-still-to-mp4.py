#!/usr/bin/env python3
import subprocess
from pathlib import Path
import sys
import shutil

def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        sys.exit("HATA: ffmpeg bulunamadı. ffmpeg kurun ve PATH'e ekleyin.")

def run(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"FFmpeg hata verdi (kod={e.returncode}). Komut:\n{' '.join(cmd)}")

def sanitize_paths(audio_path, image_path, output_path=None):
    audio = Path(audio_path).expanduser().resolve()
    image = Path(image_path).expanduser().resolve()
    if not audio.exists():
        sys.exit(f"Ses dosyası bulunamadı: {audio}")
    if not image.exists():
        sys.exit(f"Görsel dosyası bulunamadı: {image}")
    if output_path:
        output = Path(output_path).expanduser().resolve()
    else:
        output = audio.with_suffix("")  # ses dosyası adını baz al
        output = output.parent / f"{output.stem}_podcast.mp4"
    return audio, image, output

def wav_img_to_mp4_youtube(audio_path, image_path, output_path=None):
    audio, image, output = sanitize_paths(audio_path, image_path, output_path)

    # 1920x1080 tuval + orantıyı koru + padding ortala
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",                     # sabit görsel
        "-i", str(image),
        "-i", str(audio),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-profile:v", "high",
        "-level", "4.1",
        "-pix_fmt", "yuv420p",
        "-vf", vf,
        "-r", "30",                       # sabit fps
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        "-movflags", "+faststart",
        str(output)
    ]
    run(cmd)
    print(f"Tamamlandı (YouTube-safe): {output}")

if __name__ == "__main__":
    check_ffmpeg()
    # Kullanım:
    # wav_img_to_mp4_youtube("ses.wav", "kapak.jpg", "video.mp4")
    wav_img_to_mp4_youtube("ses.wav", "resim.png", "video.mp4")
