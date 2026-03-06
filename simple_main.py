import os
import sys
import json
from config import get_perplexity_client
from tools import PerplexitySearchTool, PPTXGeneratorTool, SlideToImageTool, TextToSpeechTool, VideoCompilerTool

def main():
    # Check if topic was provided as command-line argument
    if len(sys.argv) >= 2:
        topic = " ".join(sys.argv[1:])
    else:
        # Interactive mode - ask user for input
        topic = input("Enter the topic for video generation: ").strip()
        if not topic:
            print("Error: Topic cannot be empty!")
            sys.exit(1)
    
    print(f"Starting Video Generation for topic: {topic}")

    client = get_perplexity_client()
    
    # Tools
    search_tool = PerplexitySearchTool()
    pptx_tool = PPTXGeneratorTool()
    slide_to_image_tool = SlideToImageTool()
    tts_tool = TextToSpeechTool()
    video_tool = VideoCompilerTool()

    # --- Step 1: Research ---
    print("\n[Researcher Agent] Researching topic...")
    research_query = f"Research the topic '{topic}'. Find 5 key interesting sub-topics or sections suitable for a 5-slide presentation. Focus on factual, engaging content."
    research_results = search_tool.run(research_query)
    print(f"Research complete. Length: {len(research_results)} chars")

    # --- Step 2: Quality Assurance ---
    print("\n[QA Agent] Verifying facts and checking accuracy...")
    qa_prompt = f"""
    Review the following research for accuracy and credibility.
    
    Research:
    {research_results}
    
    Tasks:
    1. Identify key facts and claims
    2. Assess the credibility and accuracy of each claim
    3. Flag any potentially inaccurate or outdated information
    4. Provide an overall confidence score (0-100%)
    
    Output a brief summary:
    - Verified key facts
    - Any concerns or corrections needed
    - Overall confidence score
    
    Keep your response concise (under 500 words).
    """
    
    qa_messages = [
        {"role": "system", "content": "You are a fact-checking expert who verifies information accuracy."},
        {"role": "user", "content": qa_prompt}
    ]
    
    qa_response = client.chat.completions.create(
        model="sonar-pro",
        messages=qa_messages,
        temperature=0.1
    )
    qa_verification = qa_response.choices[0].message.content
    print(f"QA verification complete. Confidence assessment provided.")

    # --- Step 3: Scriptwriting ---
    print("\n[Scriptwriter Agent] Writing script with tables...")
    script_prompt = f"""
    Based on the following QA-verified research, create a JSON structure for a 5-slide presentation.
    Use tables when appropriate for comparisons, statistics, or structured data.
    
    Research:
    {research_results}
    
    QA Verification:
    {qa_verification}
    
    SLIDE TYPES:
    - "type": "bullets" - Standard bullet point slide
    - "type": "table" - Table-focused slide with minimal text
    - "type": "mixed" - Both bullets and a table side-by-side
    
    WHEN TO USE TABLES:
    - Comparisons (countries, products, features)
    - Statistics (population, revenue, metrics over time)
    - Timeline events with details
    - Before/after scenarios
    - Rankings or top lists
    
    The JSON MUST follow this EXACT format:
    {{
        "title": "Main Title",
        "slides": [
            {{
                "title": "Slide 1 Title",
                "type": "bullets",
                "bullets": ["Bullet 1", "Bullet 2", "Bullet 3"],
                "voiceover": "The full voiceover text for this slide (approx 2-3 sentences)."
            }},
            {{
                "title": "Comparison Table",
                "type": "table",
                "table": {{
                    "headers": ["Feature", "Option A", "Option B"],
                    "rows": [
                        ["Price", "$99", "$149"],
                        ["Speed", "Fast", "Very Fast"]
                    ]
                }},
                "voiceover": "Explaining the table data."
            }}
        ]
    }}
    
    IMPORTANT: At least 1-2 slides should have tables if the topic allows for comparisons or statistics.
    Do not include any markdown formatting like ```json ... ```, just return the raw JSON string.
    """
    
    messages = [
        {"role": "system", "content": "You are a skilled scriptwriter who outputs valid JSON."},
        {"role": "user", "content": script_prompt}
    ]
    
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
        temperature=0.1
    )
    script_response = response.choices[0].message.content
    print("Script generated.")

    # --- Step 3: Production ---
    print("\n[Producer Agent] Generating assets...")
    
    # 3.1 PPTX
    print("Generating PowerPoint...")
    ppt_result = pptx_tool.run(script_response)
    print(ppt_result)
    
    # 3.2 Images
    print("Exporting slides to images...")
    # Assuming the tool saves to output/presentation.pptx
    ppt_path = os.path.abspath("output/presentation.pptx")
    image_result = slide_to_image_tool.run(ppt_path)
    print(image_result)
    
    # 3.3 Audio
    print("Generating voiceovers...")
    audio_result = tts_tool.run(script_response)
    print(audio_result)
    
    # 3.4 Video
    print("Compiling video...")
    video_result = video_tool.run("start")
    print(video_result)

    print("\n\n########################")
    print("## Final Result ##")
    print("########################\n")
    print(f"Video generated at: {os.path.abspath('output/final_video.mp4')}")

if __name__ == "__main__":
    main()
