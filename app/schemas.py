from pydantic import BaseModel, EmailStr

# Base user schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

# For user creation (signup)
class UserCreate(UserBase):
    password: str

# Response schema (what we return to client)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# For login requests
class UserLogin(BaseModel):
    username: str
    password: str

class ChatMessage(BaseModel):
    user_id: str
    message: str
    email: EmailStr | None = None  # Only required at end


class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str


class AgentReply(BaseModel):
    session_id: str
    content: str
    user_id: int