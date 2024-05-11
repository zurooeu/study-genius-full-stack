from sqlmodel import Session

from app import crud
from app.models import (
    CnvMessageAssistantCreate,
    CnvMessageUserCreate,
    Conversation,
    ConversationBase,
    User,
)
from app.tests.utils.user import create_random_user


def create_random_conversation(db: Session, user: User | None = None) -> Conversation:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    conversation_in = ConversationBase()
    return crud.create_conversation(
        session=db, conversation_in=conversation_in, owner_id=owner_id
    )


def create_random_conversation_with_random_messages(
    db: Session, user: User | None = None
) -> Conversation:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    conversation_in = ConversationBase()
    conversation = crud.create_conversation(
        session=db, conversation_in=conversation_in, owner_id=owner_id
    )
    user_message = CnvMessageUserCreate(content="hello_from_user")
    assert conversation is not None
    assert conversation.id is not None
    crud.create_cnvmessage(
        session=db, cnv_in=user_message, owner_id=owner_id, conv_id=conversation.id
    )
    assistant_message = CnvMessageAssistantCreate(content="hello_from_assistant")
    crud.create_cnvmessage(
        session=db, cnv_in=assistant_message, owner_id=owner_id, conv_id=conversation.id
    )
    return conversation
