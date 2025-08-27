from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .models import Employee, ChatQuery, ChatResponse
from .rag import engine, load_employees

# Ensure employees loaded
EMPLOYEES = load_employees()

app = FastAPI(title="HR Resource Query Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "HR Resource Query Chatbot backend running."}

@app.get("/employees", response_model=List[Employee], tags=["employees"])
def get_employees(limit: Optional[int] = Query(None, description="Limit number of returned employees")):
    if limit is not None:
        return EMPLOYEES[:limit]
    return EMPLOYEES

@app.get("/employees/search", response_model=List[Employee], tags=["employees"])
def search_employees(
    skill: Optional[str] = Query(None),
    min_experience: Optional[int] = Query(None, alias="min_exp"),
    project: Optional[str] = Query(None),
    availability: Optional[str] = Query(None)
):
    results = []
    for emp in EMPLOYEES:
        if skill and not any(skill.lower() == s.lower() or skill.lower() in s.lower() for s in emp.get("skills", [])):
            continue
        if min_experience and emp.get("experience_years", 0) < min_experience:
            continue
        if project and not any(project.lower() == p.lower() or project.lower() in p.lower() for p in emp.get("projects", [])):
            continue
        if availability and emp.get("availability", "").lower() != availability.lower():
            continue
        results.append(emp)
    return results

@app.post("/chat", response_model=ChatResponse, tags=["chat"])
def chat(query: ChatQuery):
    # Use engine.search() which only consults employees.json
    candidates = engine.search(query.query)
    response_text = engine.generate_response(query.query, candidates)
    return ChatResponse(response=response_text, employees=candidates)
