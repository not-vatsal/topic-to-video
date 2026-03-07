import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
import threading
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import mainthread

class VideoGenUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        self.add_widget(Label(text="🎬 AI Video Generator", font_size='24sp', size_hint_y=None, height=50))
        self.add_widget(Label(text="Enter a topic below to automatically research, script, and produce a video!", size_hint_y=None, height=30))
        
        self.topic_input = TextInput(hint_text="e.g., The Future of Space Exploration", size_hint_y=None, height=50, multiline=False)
        self.add_widget(self.topic_input)
        
        self.gen_button = Button(text="Generate Video", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        self.gen_button.bind(on_press=self.generate_video)
        self.add_widget(self.gen_button)
        
        self.status_label = Label(text="Ready.", size_hint_y=None, height=50)
        self.add_widget(self.status_label)

        self.video_player = VideoPlayer(options={'allow_stretch': True})
        self.video_player.size_hint_y = 0.001  # Hide initially
        self.video_player.opacity = 0
        self.add_widget(self.video_player)

    def generate_video(self, instance):
        topic = self.topic_input.text.strip()
        if not topic:
            self.status_label.text = "⚠️ Please enter a valid topic."
            return
            
        self.status_label.text = f"Generating video for: {topic}...\nPlease wait, this may take a few minutes."
        self.gen_button.disabled = True
        
        # Run generation in a separate thread to not block the UI
        threading.Thread(target=self.run_generation, args=(topic,), daemon=True).start()

    def run_generation(self, topic):
        import sys
        import os
        
        # Prefer the local virtual environment's Python, fallback to the current Python
        venv_python = os.path.join("venv", "Scripts", "python.exe")
        python_exec = venv_python if os.path.exists(venv_python) else sys.executable
        
        try:
            process = subprocess.run(
                [python_exec, "main.py", topic],
                capture_output=True,
                text=True,
                check=True
            )
            # Update UI from the main thread
            self.update_status("✅ Video generated successfully! Check output folder.")
        except subprocess.CalledProcessError as e:
            self.update_status("❌ Error during video generation. Check console logs.")
            print("Error stderr:", e.stderr)
            print("Error stdout:", e.stdout)
        except Exception as e:
            self.update_status(f"❌ Unexpected error: {str(e)}")

    @mainthread
    def update_status(self, message):
        self.status_label.text = message
        self.gen_button.disabled = False
        self.topic_input.text = ""
        
        if "✅" in message:
            import os
            video_path = os.path.abspath(os.path.join("output", "final_video.mp4"))
            if os.path.exists(video_path):
                self.video_player.source = video_path
                self.video_player.size_hint_y = 1  # Make visible
                self.video_player.opacity = 1
                self.video_player.state = 'play'

class VideoGenApp(App):
    def build(self):
        self.title = 'AI Video Generator'
        return VideoGenUI()

if __name__ == '__main__':
    VideoGenApp().run()
