import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.ai import assistant
from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ChatPublic,
    CnvMessageUserCreate,
    Conversation,
    ConversationBase,
    ConversationUpdate,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatPublic)
def chat_new_conversation(
    session: SessionDep, current_user: CurrentUser, chat_in: CnvMessageUserCreate
) -> Any:
    """
    Start a conversation.
    """
    if chat_in.role != "user":
        raise HTTPException(status_code=400, detail="Misconfigured chat role")
    if current_user.id is None:
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
    conversation = crud.create_conversation(
        session=session, conversation_in=ConversationBase(), owner_id=current_user.id
    )
    if not conversation or not conversation.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    question = crud.create_cnvmessage(
        session=session,
        cnv_in=chat_in,
        owner_id=current_user.id,
        conv_id=conversation.id,
    )
    assistant_message = assistant.generate_answer(
        session=session, owner_id=current_user.id, conv_id=conversation.id
    )
    summary = assistant.generate_summary(session=session, conv_id=conversation.id)
    crud.update_conversation(
        session=session,
        conversation_in=ConversationUpdate(id=conversation.id, summary=summary),
    )
    return ChatPublic(
        conversation_id=conversation.id,
        content=assistant_message.content,
        summary=summary,
        question_id=question.id,
        answer_id=assistant_message.id,
    )


@router.post("/{conversation_id}", response_model=ChatPublic)
def chat_continue_conversation(
    session: SessionDep,
    current_user: CurrentUser,
    chat_in: CnvMessageUserCreate,
    conversation_id: int,
) -> Any:
    """
    Continue a conversation.
    """
    conversation = session.get(Conversation, conversation_id)
    if not conversation or not conversation.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
    if chat_in.role != "user":
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
    question = crud.create_cnvmessage(
        session=session,
        cnv_in=chat_in,
        owner_id=current_user.id,
        conv_id=conversation.id,
    )
    assistant_message = assistant.generate_answer(
        session=session, owner_id=current_user.id, conv_id=conversation.id
    )
    return ChatPublic(
        conversation_id=conversation.id,
        content=assistant_message.content,
        question_id=question.id,
        answer_id=assistant_message.id,
    )
