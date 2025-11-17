from sqlalchemy.orm import Session
from models import Style, Prompt
from schemas import StyleCreate, PromptCreate


#------- STYLE CRUD OPERATIONS --------


def create_style(db: Session, style: StyleCreate):
    """Create a new style entry."""
    db_style = Style(name=style.name, description=style.description)
    db.add(db_style)
    db.commit()
    db.refresh(db_style)
    return db_style

def get_styles(db: Session):
    """Retrieve all styles."""
    return db.query(Style).all()

def get_style_by_id(db: Session, style_id: int):
    """Retrieve a style by its ID."""
    return db.query(Style).filter(Style.id == style_id).first()

def delete_style(db: Session, style_id: int):
    """Delete a style by ID."""
    style = db.query(Style).filter(Style.id == style_id).first()
    if style:
        db.delete(style)
        db.commit()
        return True
    return False

# PROMPT CRUD OPERATIONS


def create_prompt(db: Session, prompt: PromptCreate):
    """Create a new prompt entry."""
    db_prompt = Prompt(text=prompt.text, style_id=prompt.style_id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompts(db: Session):
    """Retrieve all prompts."""
    return db.query(Prompt).all()

def get_prompt_by_id(db: Session, prompt_id: int):
    """Retrieve a prompt by its ID."""
    return db.query(Prompt).filter(Prompt.id == prompt_id).first()

def delete_prompt(db: Session, prompt_id: int):
    """Delete a prompt by ID."""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if prompt:
        db.delete(prompt)
        db.commit()
        return True
    return False