from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

from agent.builder import build_portfolio_website
from competitor_scrapper import analyze_competitors
from ai_generator import generate_response
import recommendation_engine

# --- FastAPI Setup ---
app = FastAPI(title="AI Portfolio Assistant")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Memory for generated previews ---
last_site = {"index_path": None, "details": None}

# --- Memory for chat conversations ---
CONVERSATIONS: Dict[str, List[Dict[str, str]]] = {}

# --- Request Models ---
class ClientRequest(BaseModel):
    industry: str
    style: str
    goals: str
    competitors: Optional[List[str]] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str


# --- Chat Endpoint ---
@app.post("/chat")
def chat(req: ChatRequest):
    session = req.session_id
    if session not in CONVERSATIONS:
        CONVERSATIONS[session] = [
            {"role": "system", "content": "You are a friendly expert portfolio-building assistant."}
        ]
    CONVERSATIONS[session].append({"role": "user", "content": req.message})

    full_prompt = ""
    for msg in CONVERSATIONS[session]:
        full_prompt += f"{msg['role'].upper()}: {msg['content']}\n\n"

    reply = generate_response(full_prompt)
    CONVERSATIONS[session].append({"role": "assistant", "content": reply})

    return {"reply": reply, "history": CONVERSATIONS[session]}


# --- Portfolio Advice Endpoint ---
@app.post("/generate-portfolio-advice")
def generate_portfolio_advice(payload: ClientRequest):
    try:
        copy_advice = generate_response(
            f"Industry: {payload.industry}\n"
            f"Style: {payload.style}\n"
            f"Goals: {payload.goals}\n"
            "Give portfolio improvement advice in 3 short sections."
        ) or "No copywriting advice generated."

        seo = recommendation_engine.keyword_suggestions(payload.industry) or {"recommended_keywords": [], "meta_tags": []}
        design = recommendation_engine.design_guidelines()[:5] or []

        return {
            "copywriting": str(copy_advice),
            "seo_tips": seo,
            "design_guidelines": design,
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# --- Generate Portfolio Website ---
@app.post("/generate-site")
def generate_site(payload: ClientRequest):
    try:
        project_info = "; ".join(payload.competitors) if payload.competitors else None

        index_path = build_portfolio_website(
            industry=payload.industry,
            style=payload.style,
            goals=payload.goals,
            project_info=project_info
        )

        last_site["index_path"] = index_path
        last_site["details"] = {
            "industry": payload.industry,
            "style": payload.style,
            "goals": payload.goals
        }

        return {"path": index_path}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# --- Preview Generated Site ---
@app.get("/preview", response_class=HTMLResponse)
def preview_site():
    if not last_site["index_path"]:
        raise HTTPException(status_code=404, detail="No site generated yet.")
    try:
        with open(last_site["index_path"], "r", encoding="utf-8") as f:
            html = f.read()
        return HTMLResponse(html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Competitor Analysis ---
@app.post("/analyze-competitors")
def analyze(payload: ClientRequest):
    try:
        analysis = analyze_competitors(payload.competitors or [])
        return {"analysis": analysis}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# --- Home Page ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
