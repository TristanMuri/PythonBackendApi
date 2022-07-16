from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    id: int

my_posts = [{"title": "dum dum", "content": "stuff", "id": 1}, 
    {"title": "df", "content": "rabababda", "id": 3}]

def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/hello")
async def root():
    return {"message": "Hello World!"}

@app.get("/alternative")
async def alternative():
    return {"message": "This is different"}


@app.post("/posts")
def create_posts(new_Post: Post):
    print(new_Post)
    return {"data": new_Post.dict()}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}