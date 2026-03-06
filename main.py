import sys
import os
import json
from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks
from tools import PPTXGeneratorTool, SlideToImageTool, TextToSpeechTool, VideoCompilerTool

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <topic>")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    print(f"Starting Video Generation for topic: {topic}")

    # Create Agents
    researcher, qa_agent, scriptwriter = create_agents()

    # Create Tasks
    tasks = create_tasks(researcher, qa_agent, scriptwriter, topic)

    # Instantiate Crew
    crew = Crew(
        agents=[researcher, qa_agent, scriptwriter],
        tasks=tasks,
        verbose=True,
        process=Process.sequential
    )

    # Kickoff
    print("## Starting Research & Scripting Phase ##")
    result = crew.kickoff()
    
    print("\n\n########################")
    print("## Script Generated ##")
    print("########################\n")
    # result is likely a string (TaskOutput). We need strict string.
    script_json = str(result)
    print(script_json)

    # Execute Tools Manually
    print("\n## Starting Production Phase (Manual Execution) ##")
    
    try:
        # 1. Generate PPTX
        print("Generating PowerPoint...")
        pptx_tool = PPTXGeneratorTool()
        pptx_result = pptx_tool._run(script_json)
        print(pptx_result)
        
        # 2. Convert to Images
        print("Converting to Images...")
        image_tool = SlideToImageTool()
        # Use absolute path or relative? Tool handles saving to strict path
        image_result = image_tool._run("output/presentation.pptx")
        print(image_result)
        
        # 3. Generate Audio
        print("Generating Audio...")
        tts_tool = TextToSpeechTool()
        tts_result = tts_tool._run(script_json)
        print(tts_result)
        
        # 4. Compile Video
        print("Compiling Video...")
        video_tool = VideoCompilerTool()
        video_result = video_tool._run("start")
        print(video_result)
        
        print("\n########################")
        print("## Video Generation Complete ##")
        print("########################")
        
    except Exception as e:
        print(f"\nError during production phase: {e}")

if __name__ == "__main__":
    main()
