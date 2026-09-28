import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import groq

from app.tools import YouTubeResearchTool
from app.analytics import process_youtube_dataset

# Load environment variables
load_dotenv()

# Instantiating FastAPI app (Uvicorn looks for this exact variable)
app = FastAPI(
    title="VERA API",
    description="Backend engine for Video Evidence & Resonance Analytics",
    version="1.0.0"
)

# --- 1. PYDANTIC SCHEMAS ---

class AnalysisRequest(BaseModel):
    user_input: str = Field(..., description="User's proposed channel topic or niche idea")
    selected_niche: Optional[str] = Field(None, description="Refined niche if initial query was too broad")

class VideoConcept(BaseModel):
    title_framework: str = Field(..., description="Proposed title structure")
    format: str = Field(..., description="Shorts or Long-form")
    target_subtopic: str = Field(..., description="Specific sub-area being targeted")
    rationale_from_data: str = Field(..., description="Data observation supporting this idea")

class StrategyResponse(BaseModel):
    status: str = Field(..., description="NEEDS_NICHE or SUCCESS")
    suggested_niches: Optional[List[str]] = Field(None, description="Suggested domains if input is vague")
    analyzed_sample_size: Optional[int] = 0
    median_views_in_sample: Optional[int] = 0
    strong_patterns: Optional[List[str]] = None
    weaker_patterns: Optional[List[str]] = None
    launch_ideas: Optional[List[VideoConcept]] = None
    data_disclaimers: Optional[List[str]] = None

# --- 2. ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "online", "message": "VERA Engine Backend operational!"}

@app.post("/api/v1/analyze", response_model=StrategyResponse)
async def analyze_market(req: AnalysisRequest):
    # Guardrail for broad queries
    if not req.selected_niche and len(req.user_input.strip().split()) < 3:
        return StrategyResponse(
            status="NEEDS_NICHE",
            suggested_niches=[
                f"{req.user_input} manufacturing process shorts",
                f"{req.user_input} restoration for beginners",
                f"{req.user_input} market breakdowns & reviews"
            ]
        )
    
    target_query = req.selected_niche if req.selected_niche else req.user_input

    try:
        # Fetch public metadata
        research_tool = YouTubeResearchTool()
        raw_videos = research_tool.fetch_niche_data(query=target_query, max_results=25)

        if not raw_videos:
            raise HTTPException(status_code=404, detail="No YouTube results found for query.")

        # Analytics
        summary, df = process_youtube_dataset(raw_videos)

        # Groq Client Setup
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY missing in .env file")

        groq_client = groq.Groq(api_key=groq_api_key)

        prompt = f"""
        You are VERA (Video Evidence & Resonance Analytics). Analyze this mathematical summary from a sample of YouTube videos:
        
        Niche Query: {target_query}
        Sample Size: {summary['sample_size']} videos
        Median Views in Sample: {summary['median_views']}
        Shorts Ratio in Sample: {summary['shorts_ratio']:.2f}
        Top 25% Quartile Titles: {summary['top_quartile_titles'][:5]}
        Bottom 25% Quartile Titles: {summary['bottom_quartile_titles'][:5]}

        STRICT RULES:
        1. Never state algorithmic causality (e.g., do NOT say "This video failed because of its thumbnail").
        2. Framework your title observations as correlations in the sample data.
        3. Formulate testable video concepts based on observed gaps.
        4. Return ONLY a JSON object strictly matching this schema structure:
        {json.dumps(StrategyResponse.model_json_schema())}
        """

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs strictly valid JSON matching the user's requested schema."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        raw_json_text = response.choices[0].message.content
        result = StrategyResponse.model_validate_json(raw_json_text)
        
        result.status = "SUCCESS"
        result.analyzed_sample_size = summary['sample_size']
        result.median_views_in_sample = summary['median_views']
        result.data_disclaimers = [
            "Data sampled from public YouTube search results.",
            "Private metrics (CTR, retention, impressions) are unobservable via YouTube API v3.",
            "All gaps are testable hypotheses, not guaranteed virality rules."
        ]

        return result

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal agent error: {str(e)}")