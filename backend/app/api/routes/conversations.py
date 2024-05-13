from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Conversation,
    ConversationDetailPublic,
    ConversationsPublic,
    Message,
)

router = APIRouter()


@router.get("/", response_model=ConversationsPublic)
def read_conversations(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve conversations.
    """
    count_statement = (
        select(func.count())
        .select_from(Conversation)
        .where(Conversation.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Conversation)
        .where(Conversation.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    conversations = session.exec(statement).all()

    return ConversationsPublic(data=conversations, count=count)


@router.get("/{id}", response_model=ConversationDetailPublic)
def read_conversation(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get conversation by ID.
    """
    conversation = session.get(Conversation, id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return conversation


@router.delete("/{id}")
def delete_conversation(
    session: SessionDep, current_user: CurrentUser, id: int
) -> Message:
    """
    Delete a conversation.
    """
    conversation = session.get(Conversation, id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for message in conversation.messages:
        session.delete(message)
    session.delete(conversation)
    session.commit()
    return Message(message="Conversation deleted successfully")
