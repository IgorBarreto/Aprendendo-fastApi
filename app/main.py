from random import randrange
from fastapi import FastAPI, status, HTTPException, Response
from PostDTO import PostDTO

from data_seed import posts_seed


app = FastAPI()


def find_post(id):
    for post in posts_seed:
        if post["id"] == id:
            return post
    return None


def find_index(id):
    for i, p in enumerate(posts_seed):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Bem vindo a minha API!"}


@app.get("/posts")
async def get_posts():
    return {"data": posts_seed, "message": "Post found"}


@app.post("/create-post", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: PostDTO):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 1000000)
    posts_seed.append(post_dict)
    return {"data": post_dict, "message": "Post created"}


@app.get("/posts/latest")
def get_latest_post():
    post = posts_seed[len(posts_seed) - 1]
    return {"data": post, "message": "Post found"}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )
    return {"data": post, "message": "Post found"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posst(id: int):
    index = find_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with{id} does not exists",
        )
    posts_seed.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: PostDTO):
    index = find_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with{id} does not exists",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    posts_seed[index] = post_dict
    return {
        "data": post_dict,
        "message": "Updated post",
    }
