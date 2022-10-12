from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'Bem vindo a minha API!'}

@app.post('/posts')
async def get_posts():
    return {'message':'Estes são seus posts'}
