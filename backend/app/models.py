from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(
        String,
        CheckConstraint("status IN ('draft', 'flagged', 'approved', 'published')"),
        default="draft",
        nullable=False
    )
    flagged_reasons = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', status='{self.status}')>" 