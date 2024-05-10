from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")
    user_conversations: list["Conversation"] = Relationship(back_populates="owner")
    user_messages: list["CnvMessage"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


# Shared properties
class ConversationBase(SQLModel):
    id: int | None = None


# Database model, database table inferred from class name
class Conversation(ConversationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    summary: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    modified_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    messages: list["CnvMessage"] = Relationship(back_populates="conversation")
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    owner: User = Relationship(back_populates="user_conversations")


class ConversationPublic(ConversationBase):
    id: int
    summary: str | None = None
    created_at: str
    modified_at: str


class ConversationDetailPublic(ConversationPublic):
    messages: list["CnvMessagePublic"]


class ConversationsPublic(SQLModel):
    data: list[ConversationPublic]
    count: int


class CnvMessageBase(SQLModel):
    content: str


class CnvMessageUserCreate(CnvMessageBase):
    role: str = "user"


class CnvMessageAssistantCreate(CnvMessageBase):
    role: str = "assistant"


class CnvMessageSystemCreate(CnvMessageBase):
    role: str = "system"


class CnvMessagePublic(CnvMessageBase):
    id: int
    role: str
    created_at: str


class CnvMessage(CnvMessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    role: str
    content: str
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    conversation: Conversation = Relationship(back_populates="messages")
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    owner: User = Relationship(back_populates="user_messages")


class ChatPublic(SQLModel):
    conversation_id: int
    content: str
