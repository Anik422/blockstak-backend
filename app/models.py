from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    
    news = relationship("News", back_populates="source")
    
    
class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    author = Column(String)
    url_to_image = Column(String)
    content = Column(Text)
    
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="news")


