from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    role: str = "learner"

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True
