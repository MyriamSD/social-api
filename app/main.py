from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title":"T1", "content": "T! content", "id": 0},
    {"title":"T2", "content": "T2 content", "id": 1}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get("/")
def read_root():
    return {"data": "Welcome, this is my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {id} not found')
    return {"one post": f'this:{post}'}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {'new post': post_dict}

@app.delete('/posts/{id}')
def delete_post(id: int):
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {id} not found')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {id} not found')
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data': post_dict}
