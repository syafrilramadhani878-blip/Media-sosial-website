from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
import uuid

class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=1000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_sent: bool = False

class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr 
    message: str = Field(..., min_length=1, max_length=1000)

class ContactResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None