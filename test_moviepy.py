from moviepy import ColorClip

try:
    print("Creating test video...")
    clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
    clip.write_videofile("test_video.mp4", fps=24)
    print("Test video created.")
except Exception as e:
    print(f"Error creating video: {e}")
