from crewai import Task

def create_tasks(researcher, qa_agent, scriptwriter, topic):
    research_task = Task(
        description=f"Research the topic '{topic}'. Find 3 key interesting sub-topics or sections suitable for a 3-slide presentation. Focus on factual, engaging content with statistics and comparisons where applicable.",
        expected_output="A detailed summary of 3 key points/sections about the topic with facts and data.",
        agent=researcher
    )
    
    qa_task = Task(
        description="""
        Review the research findings for accuracy and credibility.
        
        Tasks:
        1. Identify key facts and claims in the research
        2. Verify facts against reliable sources using the search tool
        3. Check for outdated or potentially inaccurate information
        4. Assign confidence scores to major claims (0-100%)
        5. Flag any corrections needed
        
        Output a verification summary:
        - List of verified key facts
        - Confidence scores for claims
        - Any concerns or corrections
        - Overall accuracy rating
        """,
        expected_output="QA-verified research with confidence scores and accuracy assessment.",
        agent=qa_agent,
        context=[research_task]
    )

    script_task = Task(
        description="""
        Based on the QA-verified research, create a JSON structure for a 3-slide presentation.
        Use tables when appropriate for comparisons, statistics, or structured data.
        
        SLIDE TYPES:
        - "type": "bullets" - Standard bullet point slide
        - "type": "table" - Table-focused slide
        - "type": "mixed" - Bullets and table side-by-side
        
        WHEN TO USE TABLES:
        - Comparisons (countries, products, features)
        - Statistics (population, revenue, metrics)
        - Timeline events
        - Rankings or top lists
        
        The JSON MUST follow this EXACT format:
        {
            "title": "Main Title",
            "slides": [
                {
                    "title": "Slide 1 Title",
                    "type": "bullets",
                    "bullets": ["Bullet 1", "Bullet 2", "Bullet 3"],
                    "voiceover": "The full voiceover text for this slide (approx 2-3 sentences)."
                },
                {
                    "title": "Comparison Table",
                    "type": "table",
                    "table": {
                        "headers": ["Feature", "Option A", "Option B"],
                        "rows": [
                            ["Price", "$99", "$149"],
                            ["Speed", "Fast", "Very Fast"]
                        ]
                    },
                    "voiceover": "Explaining the table."
                }
            ]
        }
        
        IMPORTANT: Use at least 1-2 tables if the topic allows for comparisons or statistics.
        Do not include markdown formatting, just return raw JSON string.
        """,
        expected_output="A valid JSON string with slide types and tables defining the presentation content.",
        agent=scriptwriter,
        context=[qa_task]
    )

    return [research_task, qa_task, script_task]
