from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text, func, select
import model
from database import engine
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
import resend
from pydantic import BaseModel, EmailStr
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

model.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://wilsonprajnawira.my.id",
        "https://www.wilsonprajnawira.my.id"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/ping")
def ping():
    db = SessionLocal()
    try:
        count = db.execute(text("SELECT COUNT(*) FROM certificate")).scalar()
        return {"status": "ok", "certificates": count}
    finally:
        db.close()

@app.get("/project-list")
def get_project(db: Session = Depends(get_db)):
    projects = db.query(model.ProjectList).all()

    return projects

@app.get("/project/{project_id}")
def get_project_desc(project_id: int, db: Session = Depends(get_db)):
    project = db.query(model.Project).filter(model.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    count = select(func.count(model.Tech.project_id)).where(model.Tech.project_id == project_id)
    all_c = db.scalar(count)

    
    return {
        "id": project.id,
        "title": project.title,
        "desc": project.desc,
        "github": project.github,
        "key_feature": project.key_feature,
        "tech_used": [t.tech for t in project.tech],
        "img": [i.img_url for i in project.img],
        "total_tech": all_c
    }

@app.get("/certificate-list")
def get_certificate_list(db: Session = Depends(get_db)):
    certif = db.query(model.Certificate).all()

    return [
        {
            "id": c.id,
            "title": c.title,
            "by": c.by,
            "link": c.links,
            "img": c.img_url[0].img_url if c.img_url else None
        }

        for c in certif
    ]

@app.get("/skill-list")
def skill_list(db: Session = Depends(get_db)):
    skill = db.query(model.Skill).all()

    return [
        {
            "id": s.id,
            "title": s.title,
            "category": s.category,
            "level": s.level,
            "img": s.img_url[0].img_url if s.img_url else None
        }

        for s in skill
    ]


@app.get("/skill/{skill_id}")
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(model.Skill).filter(model.Skill.id == skill_id).first()

    return {
        "id": skill.id,
        "title": skill.title,
        "category": skill.category,
        "level": skill.level,
        "desc": skill.desc,
        "use_case": skill.use_case,
        "link": skill.link,
        "learning_difficulity": skill.learning_difficulity,
        "img": skill.img_url[0].img_url
    }


@app.get("/list-list")
def getlist_info(db: Session = Depends(get_db)):
    year = 1
    project = db.query(func.max(model.ProjectList.id)).scalar()
    certif = db.query(func.max(model.Certificate.id)).scalar()

    return {
        "year": year,
        "project": project,
        "certificate": certif

    }


resend.api_key = os.getenv("RESEND_API_KEY")
MAIL_FROM = os.getenv("MAIL_FROM", "onboarding@resend.dev")


class EmailRequest(BaseModel):
    to: list[EmailStr]
    subject: str
    html: str


@app.post("/send-email")
async def send_email(payload: EmailRequest):
    params: resend.Emails.SendParams = {
        "from": MAIL_FROM,
        "to": payload.to,
        "subject": payload.subject,
        "html": payload.html,
    }
    try:
        result = await asyncio.to_thread(resend.Emails.send, params)
        return {"status": "success", "id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))