from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class PageContent(Base):
    __tablename__ = "page_content"
    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(50), nullable=False)  # 'home', 'about'
    content = Column(Text, nullable=False)
    __table_args__ = {'extend_existing': True}

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Style(Base):
    __tablename__ = "styles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    prompts = relationship("Prompt", back_populates="style", cascade="all, delete-orphan")

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    style_id = Column(Integer, ForeignKey("styles.id"), nullable=True)
    style = relationship("Style", back_populates="prompts")
