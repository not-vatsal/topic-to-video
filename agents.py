from crewai import Agent
from config import get_perplexity_llm
from tools import PerplexitySearchTool, PPTXGeneratorTool, SlideToImageTool, TextToSpeechTool, VideoCompilerTool

# Initialize LLM
llm = get_perplexity_llm()

# Tools
search_tool = PerplexitySearchTool()
pptx_tool = PPTXGeneratorTool()
slide_to_image_tool = SlideToImageTool()
tts_tool = TextToSpeechTool()
video_tool = VideoCompilerTool()

def create_agents():
    researcher = Agent(
        role='Topic Researcher',
        goal='Research the given topic thoroughly and provide structured, interesting facts.',
        backstory='You are an expert researcher who can find deep insights and organize them logically for presentations.',
        tools=[search_tool],
        llm=llm,
        verbose=True
    )
    
    qa_agent = Agent(
        role='Quality Assurance Specialist',
        goal='Verify the factual accuracy and credibility of research findings before presentation creation.',
        backstory='You are a meticulous fact-checker with expertise in validating information against reliable sources. You ensure all claims are accurate and properly sourced.',
        tools=[search_tool],
        llm=llm,
        verbose=True
    )

    scriptwriter = Agent(
        role='Presentation Scriptwriter',
        goal='Create a structured JSON script for a PowerPoint presentation with tables and bullets based on verified research.',
        backstory='You are a skilled scriptwriter who knows how to structure slides, use tables effectively for comparisons, and write engaging voiceovers. You MUST output valid JSON with proper slide types.',
        llm=llm,
        verbose=True
    )

    return researcher, qa_agent, scriptwriter
