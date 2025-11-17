from pydantic import BaseModel

class StyleBase(BaseModel):
    name: str
    description: str

class StyleCreate(StyleBase):
    pass

class Style(StyleBase):
    id: int

    class Config:
        orm_mode = True


class PromptBase(BaseModel):
    text: str
    style_id: int

class PromptCreate(PromptBase):
    pass

class Prompt(PromptBase):
    id: int

    class Config:
        orm_mode = True
