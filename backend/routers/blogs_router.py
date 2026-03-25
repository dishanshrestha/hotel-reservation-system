from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from auth import get_current_admin
from database import get_db
from schemas.blogs import BlogCreateRequest, BlogUpdateRequest
from services.image_service import _as_public_image_path

router = APIRouter(prefix="/api")


def _serialize_blog(blog: models.Blog) -> dict[str, Any]:
    return {
        "id": blog.id,
        "title": blog.title,
        "excerpt": blog.excerpt,
        "content": blog.content,
        "image": _as_public_image_path(blog.image),
        "image_raw": blog.image,
        "category": blog.category,
        "author": blog.author,
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
    }


# Public
@router.get("/blogs")
def list_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()
    return {"count": len(blogs), "blogs": [_serialize_blog(b) for b in blogs]}


@router.get("/blogs/{blog_id}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.get(models.Blog, blog_id)
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return _serialize_blog(blog)


# Admin
@router.get("/admin/blogs")
def admin_list_blogs(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    blogs = db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()
    return {"count": len(blogs), "blogs": [_serialize_blog(b) for b in blogs]}


@router.post("/admin/blogs", status_code=status.HTTP_201_CREATED)
def admin_create_blog(
    payload: BlogCreateRequest,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    blog = models.Blog(
        title=payload.title,
        excerpt=payload.excerpt,
        content=payload.content,
        image=payload.image,
        category=payload.category,
        author=payload.author,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return _serialize_blog(blog)


@router.put("/admin/blogs/{blog_id}")
def admin_update_blog(
    blog_id: int,
    payload: BlogUpdateRequest,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    blog = db.get(models.Blog, blog_id)
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if payload.title is not None:
        blog.title = payload.title
    if payload.excerpt is not None:
        blog.excerpt = payload.excerpt
    if payload.content is not None:
        blog.content = payload.content
    if payload.image is not None:
        blog.image = payload.image
    if payload.category is not None:
        blog.category = payload.category
    if payload.author is not None:
        blog.author = payload.author

    db.add(blog)
    db.commit()
    db.refresh(blog)
    return _serialize_blog(blog)


@router.delete("/admin/blogs/{blog_id}")
def admin_delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    blog = db.get(models.Blog, blog_id)
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted"}
