
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str | None = None
    status: str = "PENDING"
    priority: str = "MEDIUM"
    due_date: date | None = None


# Data allowed when updating a task
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: date | None = None


# Data returned when viewing a task
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    due_date: date | None
    user_id: int
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

# Data required when creating a comment
class CommentCreate(BaseModel):
    content: str


# Data allowed when updating a comment
class CommentUpdate(BaseModel):
    content: str


# Data returned when viewing a comment
class CommentResponse(BaseModel):
    id: int
    content: str
    task_id: int
    user_id: int
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

# Data required when creating a user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Data returned when viewing a user
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

# Data allowed when updating a user
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


# Data required when logging in
class LoginRequest(BaseModel):
    email: str
    password: str


# Data returned after successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str