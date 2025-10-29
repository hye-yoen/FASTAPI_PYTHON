from fastapi import FastAPI, HTTPException, status, Query, Path, Header, Cookie, UploadFile, File, Form, Response, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict

app = FastAPI(title="FastAPI Minimal Step-by-Step")

@app.get("/health")
def health():
    return{"status" : "Helloworld"}

@app.get("/")
def root():
    return {"messsage" : "Fast API Main EndPoint"}

@app.get("/echo")
def echo(name : str = Query(..., min_length=1,description="이름")):
    return {"hello" : name}

@app.get("/items/{item_id}")
def read_item(
    item_id : int = Path(..., ge=1),
    q : Optional[str] = Query(None, max_length=50),
):
    return {"item_id" : item_id, "q" : q}

class ItemIn (BaseModel):                #사용자로부터 전달받는 내용 저장한는 DTO
                                        #BaseModel( JSON -> Python 변환 / 유효성 검증 )
    name : str=Field(..., min_length=1)
    price : float = Field(...,gt=0)
    tags : List[str] = []
    in_stock : bool = True

class ItemOut (BaseModel):               
    id : int                                        
    name : str=Field(..., min_length=1)
    price : float = Field(...,gt=0)
    tags : List[str] = []
    in_stock : bool = True

_next_id =1
def _gen_id() -> int : # 반환자료명 정수형 명시
    global _next_id
    val = _next_id
    _next_id += 1
    return val

# ':' = type hint 문법 
DB : Dict[int,ItemOut] ={}

@app.post("/items", response_model=ItemOut ,status_code= status.HTTP_201_CREATED)
def create_item(payload : ItemIn):
    new_id = _gen_id()
    item=ItemOut(id=new_id , name=payload.name,price=payload.price,tags=payload.tags,in_stock=payload.in_stock)
    DB[new_id] = item
    # print("ItemIn",ItemIn)
    return item

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content), "content_type": file.content_type}



def send_email(to: str):
    with open("notifications.log", "a", encoding="utf-8") as f:
        f.write(f"sent to: {to}\n")

@app.get("/notify")
def notify(bg: BackgroundTasks, email: str = Query(...)):
    bg.add_task(send_email, email)
    return {"queued": True, "to": email}





