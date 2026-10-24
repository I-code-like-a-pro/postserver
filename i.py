from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()
import time

posts = [
    {"id": 1, "title": "Getting started with FastAPI", "content": "FastAPI is a modern Python framework for building APIs quickly.", "published": True, "rating": 5},
    {"id": 2, "title": "Why Pydantic matters", "content": "Pydantic validates request data so bad input never reaches your logic.", "published": True, "rating": 4},
    {"id": 3, "title": "Draft: async vs sync routes", "content": "Notes on when to use async def in FastAPI.", "published": False, "rating": None},
    {"id": 4, "title": "Path parameters explained", "content": "Type hints like id: int make FastAPI convert path values for you.", "published": True, "rating": 3},
    {"id": 5, "title": "Handling 404s properly", "content": "Raise HTTPException instead of returning None when a post is missing.", "published": True, "rating": None},
]
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected successfully')
        break
    except Exception as e:
        print('Connection failed')
        time.sleep(2)

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating:Optional[int] = None

def find(id: int):
    for post in posts:
        if post["id"] == id:
            return post          # singular
    raise HTTPException(status_code=404, detail=f"Post {id} not found")  # after the loop
def find_index(id):
    for i,p in enumerate(posts):
        if p['id'] == id:
            return i
    raise HTTPException(404, 'NOT FOUND')

def update_post_id(id:int,post:Post):
    post = post.dict()
    for i, p in enumerate(posts):
        if p['id'] == id:
            p['title'] = post['title']
            p['content'] = post['content']

    return p

    raise HTTPException(404, 'NOT FOUND')




@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM blog_posts""")
    posts = cursor.fetchall()
    print(posts)
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(new_post:Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,1000)
    posts.append(post_dict)
    return{f'data {post_dict}'}

@app.get('/posts/{id}')
def get_post_by_id(id:int, response:Response):
    post = find(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {'post details', post}
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index(id)
    posts.pop(index)
    return {'message': 'Post was deleted'}
@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    update_post_id(id, post)







