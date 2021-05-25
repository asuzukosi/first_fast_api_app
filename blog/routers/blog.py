from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from .. import database
from .. import hashing
# schemas, database, hashing

from fastapi import HTTPException, status

router = APIRouter(tags=["Blog"], prefix="/blog")


@router.get("/", response_model=List[schemas.BlogShow])
def list(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{pk}/", status_code=status.HTTP_200_OK, response_model=schemas.BlogShow)
def details(pk: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == pk).first()
    if blog:
        return blog

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {pk} not found")


@router.put("/{pk}/", status_code=status.HTTP_202_ACCEPTED)
def update(pk: int, blog: schemas.Blog, db: Session = Depends(database.get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {pk} does not exist")

    blog.update({"title": blog.title, "body": blog.body})
    db.commit()
    return blog


@router.delete("/{pk}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(pk: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {pk} not found")
    return {
        "message": "Blog has been deleted"
    }
