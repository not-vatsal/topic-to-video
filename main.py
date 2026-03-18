import sys
import os
import json
import time
from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks
from tools import PPTXGeneratorTool, SlideToImageTool, TextToSpeechTool, VideoCompilerTool

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <topic> [--no-qa]")
        sys.exit(1)

    # Parse arguments — topic is everything before flags
    args = sys.argv[1:]
    use_qa = "--no-qa" not in args
    topic_parts = [a for a in args if not a.startswith("--")]
    topic = " ".join(topic_parts)

    print(f"Starting Video Generation for topic: {topic}")
    print(f"QA Agent: {'ENABLED' if use_qa else 'DISABLED (fast mode)'}")
    start_time = time.time()

    # Create Agents
    researcher, qa_agent, scriptwriter = create_agents(use_qa=use_qa)

    # Create Tasks
    tasks = create_tasks(researcher, qa_agent, scriptwriter, topic, use_qa=use_qa)

    # Build agents list (exclude None)
    agents_list = [a for a in [researcher, qa_agent, scriptwriter] if a is not None]

    # Instantiate Crew
    crew = Crew(
        agents=agents_list,
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
    script_json = str(result)
    print(script_json)

    # Execute Tools Manually
    print("\n## Starting Production Phase ##")

    try:
        # 1. Generate PPTX
        print("Generating PowerPoint...")
        pptx_tool = PPTXGeneratorTool()
        pptx_result = pptx_tool._run(script_json)
        print(pptx_result)

        # 2. Convert to Images
        print("Converting to Images...")
        image_tool = SlideToImageTool()
        image_result = image_tool._run("output/presentation.pptx")
        print(image_result)

        # 3. Generate Audio (Sarvam AI, parallel)
        print("Generating Audio via Sarvam AI...")
        tts_tool = TextToSpeechTool()
        tts_result = tts_tool._run(script_json)
        print(tts_result)

        # 4. Compile Video
        print("Compiling Video...")
        video_tool = VideoCompilerTool()
        video_result = video_tool._run("start")
        print(video_result)

        elapsed = time.time() - start_time
        print(f"\n########################")
        print(f"## Video Generation Complete in {elapsed/60:.1f} min ##")
        print(f"########################")

    except Exception as e:
        print(f"\nError during production phase: {e}")

if __name__ == "__main__":
    main()
