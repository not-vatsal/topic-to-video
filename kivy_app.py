import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
import threading
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import mainthread, Clock

class VideoGenUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.add_widget(Label(
            text="AI Video Generator",
            font_size='24sp', size_hint_y=None, height=50
        ))
        self.add_widget(Label(
            text="Enter a topic below to automatically research, script, and produce a video!",
            size_hint_y=None, height=30
        ))

        self.topic_input = TextInput(
            hint_text="e.g., The Future of Space Exploration",
            size_hint_y=None, height=50, multiline=False
        )
        self.add_widget(self.topic_input)

        # ── QA Agent toggle row ─────────────────────────────────────────────
        qa_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        qa_row.add_widget(Label(
            text="QA Agent (accuracy check — disable for fast demo):",
            size_hint_x=0.75, halign='left', valign='middle'
        ))
        self.qa_switch = Switch(active=True, size_hint_x=0.25)
        qa_row.add_widget(self.qa_switch)
        self.add_widget(qa_row)
        # ────────────────────────────────────────────────────────────────────

        self.gen_button = Button(
            text="Generate Video",
            size_hint_y=None, height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.gen_button.bind(on_press=self.generate_video)
        self.add_widget(self.gen_button)

        self.status_label = Label(text="Ready.", size_hint_y=None, height=50)
        self.add_widget(self.status_label)

        # Video player — hidden initially
        self._video_source = None
        self.video_player = VideoPlayer(options={'allow_stretch': True})
        self.video_player.size_hint_y = 0.001
        self.video_player.opacity = 0
        self.video_player.bind(state=self._on_video_state)
        self.add_widget(self.video_player)

    # ── Video state handler (replaces eos — not available on VideoPlayer) ────
    def _on_video_state(self, instance, value):
        """VideoPlayer.state goes to 'stop' when video ends. Rewind & pause."""
        if value == 'stop':
            Clock.schedule_once(self._rewind_video, 0.2)

    def _rewind_video(self, dt):
        try:
            self.video_player.position = 0
            self.video_player.state = 'pause'
        except Exception:
            pass
    # ────────────────────────────────────────────────────────────────────────

    def generate_video(self, instance):
        topic = self.topic_input.text.strip()
        if not topic:
            self.status_label.text = "⚠️ Please enter a valid topic."
            return

        use_qa = self.qa_switch.active
        mode_label = "Full mode (QA on)" if use_qa else "Fast demo mode (QA off)"
        self.status_label.text = (
            f"Generating: {topic} — {mode_label}\n"
            "Please wait, this may take a few minutes."
        )
        self.gen_button.disabled = True

        threading.Thread(
            target=self.run_generation, args=(topic, use_qa), daemon=True
        ).start()

    def run_generation(self, topic, use_qa: bool):
        import sys

        venv_python = os.path.join("venv", "Scripts", "python.exe")
        python_exec = venv_python if os.path.exists(venv_python) else sys.executable

        cmd = [python_exec, "main.py", topic]
        if not use_qa:
            cmd.append("--no-qa")

        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
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
            video_path = os.path.abspath(os.path.join("output", "final_video.mp4"))
            if os.path.exists(video_path):
                self._load_video(video_path)

    def _load_video(self, video_path: str):
        """Safely load and play the video without crashing on eos."""
        try:
            # Reset previous player state
            self.video_player.state = 'stop'
            self.video_player.source = ''
            # Small delay before loading new source
            Clock.schedule_once(lambda dt: self._do_load_video(video_path), 0.3)
        except Exception as e:
            print(f"[VideoPlayer] Load error: {e}")

    def _do_load_video(self, video_path: str):
        try:
            self.video_player.source = video_path
            self.video_player.size_hint_y = 1
            self.video_player.opacity = 1
            self.video_player.state = 'play'
        except Exception as e:
            print(f"[VideoPlayer] Play error: {e}")


class VideoGenApp(App):
    def build(self):
        self.title = 'AI Video Generator'
        return VideoGenUI()


if __name__ == '__main__':
    VideoGenApp().run()
