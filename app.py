from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
import jwt
import time
import os


# 加载 .env 文件
load_dotenv()

# 从环境变量中读取配置

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


app = FastAPI()

# ACCESS_KEY = "30b3d98a413f4e949b743fad9ed9abd2"
# SECRET_KEY = "bbaf266dfaa54e59aad3cf07f7e5f881"


TEXT2VIDEO_URL = "https://api.klingai.com/v1/videos/text2video"
IMAGE2VIDEO_URL = "https://api.klingai.com/v1/videos/image2video"


def generate_jwt(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 1800s有效期（半个小时）
        "nbf": int(time.time()) - 5  # 5s前生效
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token


class TextToVideoRequest(BaseModel):
    prompt: str


class ImageToVideoRequest(BaseModel):
    image_url: str
    prompt: str  # 添加 prompt 字段


'''
 --------------------                文本转视频接口                 --------------------
'''
@app.post("/create_text_to_video_task")
def create_text_to_video_task(request: TextToVideoRequest):
    token = generate_jwt(ACCESS_KEY, SECRET_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(TEXT2VIDEO_URL, json=request.dict(), headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.get("/get_text_to_video_task/{task_id}")
def get_text_to_video_task(task_id: str):
    token = generate_jwt(ACCESS_KEY, SECRET_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{TEXT2VIDEO_URL}/{task_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.get("/list_text_to_video_tasks")
def list_text_to_video_tasks(page_num: int = 1, page_size: int = 30):
    token = generate_jwt(ACCESS_KEY, SECRET_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{TEXT2VIDEO_URL}?pageNum={page_num}&pageSize={page_size}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
'''
 --------------------                   图片转视频接口                 --------------------
'''
@app.post("/create_image_to_video_task")
def create_image_to_video_task(request: ImageToVideoRequest):
    token = generate_jwt(ACCESS_KEY, SECRET_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    

    payload = {
        "image": request.image_url,
        "prompt": request.prompt
    }
    
    response = requests.post(IMAGE2VIDEO_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.get("/get_image_to_video_task/{task_id}")
def get_image_to_video_task(task_id: str):
    token = generate_jwt(ACCESS_KEY, SECRET_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{IMAGE2VIDEO_URL}/{task_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.get("/list_image_to_video_tasks")
def list_image_to_video_tasks(page_num: int = 1, page_size: int = 30):
    token = generate_jwt(ACCESS_KEY, SECRET_KEY)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{IMAGE2VIDEO_URL}?pageNum={page_num}&pageSize={page_size}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
