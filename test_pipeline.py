import os
import json
from tools import PPTXGeneratorTool, SlideToImageTool, TextToSpeechTool, VideoCompilerTool

def test_pipeline():
    print("Starting Pipeline Test...")
    
    # Mock JSON script
    mock_script = {
        "title": "Test Presentation",
        "slides": [
            {
                "title": "Welcome",
                "bullets": ["This is a test slide", "Verifying the pipeline", "No API key needed for this test"],
                "voiceover": "Welcome to the test presentation. We are verifying that the video generation pipeline works correctly."
            },
            {
                "title": "Conclusion",
                "bullets": ["Test complete", "Assets generated", "Ready for real topics"],
                "voiceover": "The test is now complete. If you can see this video, your local environment is set up correctly."
            }
        ]
    }
    json_script = json.dumps(mock_script)

    # Initialize Tools
    pptx_tool = PPTXGeneratorTool()
    slide_to_image_tool = SlideToImageTool()
    tts_tool = TextToSpeechTool()
    video_tool = VideoCompilerTool()

    # 1. Generate PPTX
    print("\n1. Generating PowerPoint...")
    res = pptx_tool.run(json_script)
    print(res)
    if "Error" in res: return

    # 2. Convert to Images
    print("\n2. Exporting slides to images...")
    ppt_path = os.path.abspath("output/presentation.pptx")
    res = slide_to_image_tool.run(ppt_path)
    print(res)
    if "Error" in res: return

    # 3. Generate Audio
    print("\n3. Generating voiceovers...")
    res = tts_tool.run(json_script)
    print(res)
    if "Error" in res: return

    # 4. Compile Video
    print("\n4. Compiling video...")
    res = video_tool.run("start")
    print(res)
    if "Error" in res: return

    print("\nPipeline Test Successful!")
    print(f"Final video at: {os.path.abspath('output/final_video.mp4')}")

if __name__ == "__main__":
    test_pipeline()
