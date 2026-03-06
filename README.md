# Topic to Video Generator

A Python-based AI tool that takes a given topic and automatically researches, scripts, and produces a complete video using CrewAI, Perplexity AI, and MoviePy.

## Features
- **AI-Powered Research:** Uses Perplexity AI to deeply research the provided topic.
- **Automated Scripting:** Generates a full YouTube-style script with narration and visual cues.
- **Audio & Visual Generation:** Converts the script into an audio track, generates slides/images, and compiles them into a final video.
- **Multiple Interfaces:** Run via command-line (`main.py`) or visually via a Kivy User Interface (`kivy_app.py`).

## Requirements
- Python 3.10+
- A valid [Perplexity API](https://www.perplexity.ai/settings/api) Key
- A valid [OpenAI API](https://platform.openai.com/api-keys) Key (if configured)

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
   pip install kivy
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```env
   PERPLEXITY_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
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
