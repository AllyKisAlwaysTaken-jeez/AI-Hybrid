from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import uuid

from agent.builder import build_portfolio_website
from competitor_scrapper import analyze_competitors
from ai_generator import generate_response
import recommendation_engine

app = FastAPI(title="AI Portfolio Assistant")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store site preview path (Render-safe directory = /tmp)
last_site = {"index_path": None, "details": None}

# Chat memory (per-session)
CONVERSATIONS: Dict[str, List[Dict[str, str]]] = {}


# ---------- MODELS ----------
class ClientRequest(BaseModel):
    industry: str
    style: str
    goals: str
    competitors: Optional[List[str]] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str


# ---------- CHAT ENDPOINT ----------
@app.post("/chat")
def chat(req: ChatRequest):
    session = req.session_id

    if session not in CONVERSATIONS:
        CONVERSATIONS[session] = [
            {"role": "system", "content": "You are a helpful, friendly portfolio-building assistant. Be conversational."}
        ]

    CONVERSATIONS[session].append({"role": "user", "content": req.message})

    full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in CONVERSATIONS[session]])

    reply = generate_response(full_prompt) or "I'm sorry — my response generator returned no output."

    CONVERSATIONS[session].append({"role": "assistant", "content": reply})

    return {"reply": reply, "session": session, "history": CONVERSATIONS[session]}


# ---------- PORTFOLIO ADVICE ----------
@app.post("/generate-portfolio-advice")
def generate_portfolio_advice(payload: ClientRequest):
    try:
        copy_advice = generate_response(
            f"Industry: {payload.industry}\n"
            f"Style: {payload.style}\n"
            f"Goals: {payload.goals}\n"
            "Give concise portfolio improvement advice in 3 sections."
        ) or "No advice returned."

        seo = recommendation_engine.keyword_suggestions(payload.industry) or {
            "recommended_keywords": ["portfolio", "professional"]
        }

        design = recommendation_engine.design_guidelines() or ["No design guidelines returned."]
        design = design[:5]

        return {
            "copywriting": copy_advice,
            "seo_tips": seo,
            "design_guidelines": design
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ---------- WEBSITE GENERATION ----------
@app.post("/generate-site")
def generate_site(payload: ClientRequest):
    try:
        competitors_joined = ", ".join(payload.competitors) if payload.competitors else ""

        index_path = build_portfolio_website(
            industry=payload.industry,
            style=payload.style,
            goals=payload.goals,
            project_info=competitors_joined,
            output_dir="/tmp"     # <-- render-safe
        )

        last_site["index_path"] = index_path
        last_site["details"] = payload.dict()

        return {"path": "/preview"}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ---------- PREVIEW ----------
@app.get("/preview", response_class=HTMLResponse)
def preview_site():
    if not last_site["index_path"]:
        raise HTTPException(status_code=404, detail="No site generated.")

    try:
        with open(last_site["index_path"], "r", encoding="utf-8") as f:
            html = f.read()
        return HTMLResponse(html)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- COMPETITOR ANALYSIS ----------
@app.post("/analyze-competitors")
def analyze(payload: ClientRequest):
    try:
        return {"analysis": analyze_competitors(payload.competitors or [])}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ---------- HOME PAGE ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
