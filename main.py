from fastapi import Body, FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    body: str

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}

@app.get('/post')
async def post():
    return {"message": "This is your get reuqest for post"}

@app.post('/')
async def post_request(payload: Post):
    return {"message": f"This is the title of your post request : {payload.title}"}

