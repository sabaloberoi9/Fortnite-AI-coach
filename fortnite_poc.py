import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. The Pydantic Schema (Structured Data Blueprint)
class VODReportCard(BaseModel):
    executive_summary: str = Field(description="A cold, 3-sentence high-level assessment of the match pace, survival efficiency, and win-condition viability.")
    rotation_score: int = Field(description="Score from 1 to 10 evaluating map movement, dead-side vs congested-side positioning, and storm cycle anticipation.")
    resource_efficiency: int = Field(description="Score from 1 to 10 evaluating material allocation, shield economy, and utilization of environmental heals (Slurp Barrels).")
    strategic_mistakes: list[str] = Field(description="A list of specific, timestamped macro errors (e.g., unnecessary mid-game fights, late rotations) with the brutal consequence of each.")

# 2. Open-Source Auth Setup
user_key = "PASTE_YOUR_GEMINI_API_KEY_HERE"

if user_key == "PASTE_YOUR_GEMINI_API_KEY_HERE" or not user_key:
    print("[WARNING]: You must paste a valid Gemini API key into the 'user_key' variable to run this script.")
    client = None
else:
    client = genai.Client(api_key=user_key)

# 3. Execution Pipeline
if client:
    print("Uploading VOD to Google File API...")
    video_file = client.files.upload(file='sample_match.mp4')
    print(f"File uploaded successfully. URI: {video_file.uri}")

    while video_file.state.name == "PROCESSING":
        print("Server is chunking video frames... Waiting 10 seconds.")
        time.sleep(10)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed on the server side.")
        
    print("Processing complete. Enforcing Anti-Ego constraints and executing model...")
    
    coaching_prompt = (
        "Analyze this full match VOD. Track Storm Surge tag timing, dead-side rotation logic, "
        "and endgame layer selection. Identify exactly where the player failed."
    )

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[video_file, coaching_prompt],
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are 'The Silent Auditor', an elite, no-nonsense competitive Fortnite strategist. "
                "Your goal is optimization, not encouragement. Eliminate all fluff ('Good job', 'Nice try'). "
                "If the user deviates from optimal macro-play (e.g., taking an unnecessary mid-game 50/50, "
                "contesting height without a 500+ mat advantage, or burning inventory shields before map shields), "
                "you must flag it as a 'CRITICAL ERROR'. Ignore crosshair placement and mechanical speed entirely. "
                "Focus purely on rotation logic, Surge tags, and late-game refresh timing."
            ),
            response_mime_type="application/json",
            response_schema=VODReportCard,
            video_metadata=types.VideoMetadata(
                start_offset="60s" # Automatically trims lobby dead-air
            )
        )
    )

    print("\n================ THE SILENT AUDITOR: DASHBOARD ================")
    print(response.text)
    print("===============================================================")
