from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostResponse(PostBase):
    id: int
    status: str
    flagged_reasons: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ModerationResponse(BaseModel):
    status: str
    reasons: Optional[List[str]] = None 