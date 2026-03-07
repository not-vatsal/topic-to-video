# Topic to Video Generator

A Python-based AI tool that takes a given topic and automatically researches, scripts, and produces a complete video using CrewAI, Google Gemini, Serper API, and MoviePy.

## Features
- **AI-Powered Research:** Uses the Serper API to deeply research the provided topic on Google.
- **Automated Scripting:** Generates a full YouTube-style script with narration and visual cues powered by Google's Gemini-2.5-flash LLM.
- **Audio & Visual Generation:** Converts the script into an audio track, generates slides/images, and compiles them into a final video.
- **Multiple Interfaces:** Run via command-line (`main.py`) or visually via a Kivy User Interface (`kivy_app.py`).
- **Inline Video Playback:** The Kivy UI now features a built-in `VideoPlayer` to automatically preview your generated videos directly in the app.

## Requirements
- Python 3.10+
- A valid [Serper API](https://serper.dev/) Key (for Google Search)
- A valid [Google Gemini API](https://aistudio.google.com/app/apikey) Key

## Installation

1. Clone this repository.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   pip install kivy ffpyplayer
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```env
   SERPER_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   ```

## Usage

### Using the Kivy UI:
Run the graphical interface to easily generate videos:
```bash
python kivy_app.py
```

### Using the Command Line:
Run the script directly via terminal, providing the topic as an argument:
```bash
python main.py "The Future of Space Exploration"
```

The output presentation, audio, and final video will be saved in the `output/` directory.
