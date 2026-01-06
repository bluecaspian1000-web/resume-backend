from fastapi import FastAPI, Depends, WebSocket, Header, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, ProjectRequest
from schemas import RequestCreate
from auth import create_access_token, verify_token
from fastapi.middleware.cors import CORSMiddleware
from auth import create_access_token, verify_token


origins = [
    "*", 
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(engine)

online_users = 0


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- فرم درخواست پروژه ----
@app.post("/requests")
def create_request(data: RequestCreate, db: Session = Depends(get_db)):
    req = ProjectRequest(**data.dict())
    db.add(req)
    db.commit()
    return {"message": "Request submitted"}


# ---- لاگین ادمین ----

from pydantic import BaseModel

class LoginSchema(BaseModel):
    username: str
    password: str


@app.post("/admin/login")
def login(data: LoginSchema):
    if data.username == "admin" and data.password == "1234":
        return {"access_token": create_access_token({"sub": "admin"})}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/admin/requests")
def get_requests(token: str = Header(..., alias="token"), db: Session = Depends(get_db)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    requests = db.query(ProjectRequest).all()
    return requests


# ---- WebSocket کاربران آنلاین ----
@app.websocket("/ws/online")
async def websocket_endpoint(ws: WebSocket):
    global online_users
    await ws.accept()
    online_users += 1
    await ws.send_text(str(online_users))

    try:
        while True:
            await ws.receive_text()
    except:
        online_users -= 1
