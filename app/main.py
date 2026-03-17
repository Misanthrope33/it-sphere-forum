from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import Post
from .schemas import PostCreate, PostResponse

app = FastAPI(title="Портал-форум IT-сфера")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Добро пожаловать на портал-форум IT-сфера"}

@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        author=post.author,
        title=post.title,
        content=post.content
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@app.get("/posts/title/{title}", response_model=list[PostResponse])
def get_posts_by_title(title: str, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.title == title).all()