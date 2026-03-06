import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

def debug_video():
    try:
        slides_dir = os.path.abspath("output/slides")
        audio_dir = os.path.abspath("output/audio")
        output_video = os.path.abspath("output/debug_video.mp4")
        
        slides = sorted([os.path.join(slides_dir, f) for f in os.listdir(slides_dir) if f.endswith(".jpg")])
        audios = sorted([os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".mp3")])
        
        print(f"Found {len(slides)} slides and {len(audios)} audios.")
        
        if len(slides) != len(audios):
            print("Mismatch!")
            return

        clips = []
        for i, (slide_path, audio_path) in enumerate(zip(slides, audios)):
            print(f"Processing clip {i}: {slide_path} + {audio_path}")
            audio_clip = AudioFileClip(audio_path)
            print(f"  Audio duration: {audio_clip.duration}")
            slide_clip = ImageClip(slide_path).with_duration(audio_clip.duration)
            slide_clip = slide_clip.with_audio(audio_clip)
            clips.append(slide_clip)
        
        print("Concatenating clips...")
        final_clip = concatenate_videoclips(clips)
        print(f"Final duration: {final_clip.duration}")
        
        print(f"Writing to {output_video}...")
        final_clip.write_videofile(output_video, fps=24, codec="libx264", audio_codec="aac")
        print("Done.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_video()
