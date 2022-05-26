from fastapi import Body, FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}

@app.get('/post')
async def post():
    return {"message": "This is your get reuqest for post"}

@app.post('/')
async def post_request(payload: dict = Body(...)):
    return {"message": f"This is the title of your post request : {payload['title']}"}

