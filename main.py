from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import app.crud as crud
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Member(BaseModel):
    id: int | None = None
    name: str
    phone: str | None = None
    contributions: float | None = 0.0
    notes: str | None = ""

@app.get("/api/members")
def get_members():
    return crud.read_members()

@app.post("/api/members")
def add_member(m: Member):
    return crud.add_member(m.dict())

@app.put("/api/members/{member_id}")
def update_member(member_id: int, m: Member):
    updated = crud.update_member(member_id, m.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Member not found")
    return updated

@app.delete("/api/members/{member_id}")
def delete_member(member_id: int):
    ok = crud.delete_member(member_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"ok": True}

# Serve built frontend static files (from backend/static)
STATIC_DIR = Path(__file__).resolve().parent.parent / 'static'
INDEX = STATIC_DIR / 'index.html'

@app.get("/")
def root():
    if INDEX.exists():
        return HTMLResponse(INDEX.read_text(encoding='utf-8'))
    return {"status":"ok"}

@app.get("/api/_source/main.py")
def view_main_source():
    with open(__file__, 'r', encoding='utf-8') as f:
        return {"source": f.read()}
