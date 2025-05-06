from fastapi import FastAPI, HTTPException, Depends, status, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, insert
import json
from typing import List, Optional

from app.schemas import PostCreate, PostResponse, ModerationResponse, PostUpdate
from app.models import Post
from app.moderation import moderate_content
from app.database import get_db

router = APIRouter()

@router.post("/posts/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    """Create a new draft post"""
    new_post = Post(
        title=post.title,
        content=post.content,
        status="draft"
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.post("/posts/{post_id}/submit/", response_model=ModerationResponse)
async def submit_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Submit a post for review"""
    # Get the post
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status == "published":
        raise HTTPException(status_code=403, detail="Published posts cannot be modified")
    
    # Moderate the content
    status_result, reasons = await moderate_content(post.content)
    
    # Update the post status
    post.status = status_result
    if status_result == "flagged":
        post.flagged_reasons = json.dumps(reasons)
    else:
        post.flagged_reasons = None
    
    await db.commit()
    
    # Return the moderation result
    return ModerationResponse(status=status_result, reasons=reasons if status_result == "flagged" else None)

@router.get("/posts/", response_model=List[PostResponse])
async def list_posts(status: Optional[str] = Query(None), db: AsyncSession = Depends(get_db)):
    """
    List all posts, optionally filtered by status
    Status options: draft, flagged, approved, published
    """
    query = select(Post)
    if status:
        if status not in ["draft", "flagged", "approved", "published"]:
            raise HTTPException(status_code=400, detail="Invalid status filter")
        query = query.where(Post.status == status)
    
    result = await db.execute(query)
    posts = result.scalars().all()
    return posts

@router.patch("/posts/{post_id}/publish/", response_model=PostResponse)
async def publish_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Publish an approved post"""
    # Get the post
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Can only publish approved posts
    if post.status != "approved":
        raise HTTPException(
            status_code=403, 
            detail="Only approved posts can be published"
        )
    
    # Update the post status
    post.status = "published"
    await db.commit()
    await db.refresh(post)
    
    return post

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific post by ID"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

@router.patch("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: PostUpdate, db: AsyncSession = Depends(get_db)):
    """Update a draft post. Only draft posts can be updated."""
    # Get the post
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Only draft posts can be updated
    if post.status != "draft":
        raise HTTPException(
            status_code=403, 
            detail=f"Only draft posts can be updated. Current status: {post.status}"
        )
    
    # Update the post
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    
    await db.commit()
    await db.refresh(post)
    
    return post 