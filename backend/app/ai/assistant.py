from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.exception import ApiDbException
from app.models import CnvMessage, CnvMessageAssistantCreate, Conversation


def generate_answer(*, session: Session, owner_id: int, conv_id: int) -> CnvMessage:
    conversation = session.get(Conversation, conv_id)
    if not conversation or conversation.id is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.id is None:
        raise ApiDbException("Conversation without id")
    assistant_msg = CnvMessageAssistantCreate(content="mock answer")
    return crud.create_cnvmessage(
        session=session,
        cnv_in=assistant_msg,
        owner_id=owner_id,
        conv_id=conversation.id,
    )
